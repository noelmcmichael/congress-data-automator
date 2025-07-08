#!/usr/bin/env python3
"""
Fixed database reconstruction with authoritative committee data
"""

import json
import psycopg2
from datetime import datetime
import os

class DatabaseReconstructor:
    """Reconstruct database with authoritative committee data."""
    
    def __init__(self, db_connection_string):
        self.db_connection_string = db_connection_string
        self.conn = None
        self.cursor = None
        
        # Name mapping for senators who use different names
        self.name_mapping = {
            'Dick Durbin': 'Richard Durbin',
            'Chuck Grassley': 'Charles Grassley',
            'Ted Cruz': 'Rafael Cruz',
            'Jim Risch': 'James Risch',
            'Mike Lee': 'Michael Lee',
            'Josh Hawley': 'Joshua Hawley',
            'Tom Cotton': 'Thomas Cotton',
            'JD Vance': 'James Vance',
            'Ben Cardin': 'Benjamin Cardin',
            'Ron Wyden': 'Ronald Wyden',
            'Mike Crapo': 'Michael Crapo'
        }
    
    def connect(self):
        """Connect to database."""
        try:
            self.conn = psycopg2.connect(self.db_connection_string)
            self.cursor = self.conn.cursor()
            print("✅ Database connection established")
            return True
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            return False
    
    def wipe_corrupted_data(self):
        """Remove all corrupted committee memberships."""
        try:
            # Get count before deletion
            self.cursor.execute("SELECT COUNT(*) FROM committee_memberships;")
            before_count = self.cursor.fetchone()[0]
            
            # Delete all committee memberships
            self.cursor.execute("DELETE FROM committee_memberships;")
            
            # Reset sequence
            self.cursor.execute("ALTER SEQUENCE committee_memberships_id_seq RESTART WITH 1;")
            
            self.conn.commit()
            print(f"✅ Wiped {before_count} corrupted committee memberships")
            return True
        except Exception as e:
            print(f"❌ Data wipe failed: {e}")
            self.conn.rollback()
            return False
    
    def find_committee_by_name(self, committee_name, chamber):
        """Find committee by name and chamber."""
        try:
            self.cursor.execute("""
                SELECT id, name FROM committees 
                WHERE name = %s AND chamber = %s
            """, (committee_name, chamber))
            
            result = self.cursor.fetchone()
            if result:
                return result[0]
                
            # Try partial match
            self.cursor.execute("""
                SELECT id, name FROM committees 
                WHERE name ILIKE %s AND chamber = %s
            """, (f"%{committee_name}%", chamber))
            
            result = self.cursor.fetchone()
            if result:
                return result[0]
                
            return None
            
        except Exception as e:
            print(f"❌ Committee lookup failed: {e}")
            return None
    
    def find_member_by_name(self, member_name, state=None):
        """Find member by name and optionally state."""
        try:
            # Check name mapping first
            if member_name in self.name_mapping:
                member_name = self.name_mapping[member_name]
            
            # Split name into parts
            name_parts = member_name.strip().split()
            if len(name_parts) < 2:
                return None
            
            first_name = name_parts[0]
            last_name = name_parts[-1]
            
            # Try to find member
            if state:
                self.cursor.execute("""
                    SELECT id, first_name, last_name, state, chamber 
                    FROM members 
                    WHERE first_name ILIKE %s AND last_name ILIKE %s AND state = %s
                """, (first_name, last_name, state))
            else:
                self.cursor.execute("""
                    SELECT id, first_name, last_name, state, chamber 
                    FROM members 
                    WHERE first_name ILIKE %s AND last_name ILIKE %s
                """, (first_name, last_name))
            
            result = self.cursor.fetchone()
            if result:
                return {
                    'id': result[0],
                    'first_name': result[1],
                    'last_name': result[2],
                    'state': result[3],
                    'chamber': result[4]
                }
            
            # Try last name only with state
            if state:
                self.cursor.execute("""
                    SELECT id, first_name, last_name, state, chamber 
                    FROM members 
                    WHERE last_name ILIKE %s AND state = %s
                """, (last_name, state))
                
                result = self.cursor.fetchone()
                if result:
                    return {
                        'id': result[0],
                        'first_name': result[1],
                        'last_name': result[2],
                        'state': result[3],
                        'chamber': result[4]
                    }
            
            return None
            
        except Exception as e:
            print(f"❌ Member lookup failed for {member_name}: {e}")
            return None
    
    def create_committee_membership(self, member_id, committee_id, position='member'):
        """Create committee membership relationship."""
        try:
            # Check if membership already exists
            self.cursor.execute("""
                SELECT id FROM committee_memberships 
                WHERE member_id = %s AND committee_id = %s
            """, (member_id, committee_id))
            
            if self.cursor.fetchone():
                return True  # Already exists
            
            # Create membership
            self.cursor.execute("""
                INSERT INTO committee_memberships (member_id, committee_id, position, is_current, created_at)
                VALUES (%s, %s, %s, true, NOW())
            """, (member_id, committee_id, position))
            
            return True
            
        except Exception as e:
            print(f"❌ Membership creation failed: {e}")
            return False
    
    def import_committee_data(self, committee_data, chamber):
        """Import committee data for specific chamber."""
        print(f"\n🏛️ Importing {chamber} committee data...")
        
        total_members_added = 0
        
        for committee in committee_data:
            committee_name = committee['name']
            members = committee.get('members', [])
            
            if not members:
                print(f"  ⚠️ Skipping {committee_name} (no members)")
                continue
                
            print(f"\n  📋 Processing {committee_name}...")
            
            # Find committee
            committee_id = self.find_committee_by_name(committee_name, chamber)
            if not committee_id:
                print(f"    ❌ Committee not found: {committee_name}")
                continue
            
            # Process members
            members_added = 0
            for member_data in members:
                member_name = member_data['name']
                state = member_data.get('state')
                role = member_data.get('role', 'member').lower()
                
                # Map role to position
                if role == 'chair':
                    position = 'chair'
                elif role == 'ranking member':
                    position = 'ranking_member'
                else:
                    position = 'member'
                
                # Find member in database
                member = self.find_member_by_name(member_name, state)
                if not member:
                    print(f"    ⚠️ Member not found: {member_name} ({state})")
                    continue
                
                # Verify chamber matches
                if member['chamber'] != chamber:
                    print(f"    ⚠️ Chamber mismatch: {member_name} is {member['chamber']}, not {chamber}")
                    continue
                
                # Create membership
                if self.create_committee_membership(member['id'], committee_id, position):
                    members_added += 1
                    print(f"    ✅ Added {member['first_name']} {member['last_name']} ({position})")
                else:
                    print(f"    ❌ Failed to add {member_name}")
            
            print(f"  📊 {committee_name}: {members_added}/{len(members)} members added")
            total_members_added += members_added
        
        self.conn.commit()
        print(f"\n✅ {chamber} import complete: {total_members_added} total members added")
        return total_members_added
    
    def run_reconstruction(self, data_file):
        """Run complete database reconstruction."""
        print("🚀 Starting FIXED database reconstruction...")
        print("=" * 50)
        
        # Connect to database
        if not self.connect():
            return False
        
        # Load authoritative data
        try:
            with open(data_file, 'r') as f:
                data = json.load(f)
            print(f"✅ Loaded authoritative data from {data_file}")
        except Exception as e:
            print(f"❌ Failed to load data file: {e}")
            return False
        
        # Wipe corrupted data
        if not self.wipe_corrupted_data():
            print("❌ Data wipe failed - aborting reconstruction")
            return False
        
        # Import authoritative data
        senate_count = self.import_committee_data(data['senate_committees'], 'Senate')
        house_count = self.import_committee_data(data['house_committees'], 'House')
        
        # Final verification
        self.cursor.execute("SELECT COUNT(*) FROM committee_memberships;")
        total_memberships = self.cursor.fetchone()[0]
        
        print("\n" + "=" * 50)
        print("🎉 FIXED DATABASE RECONSTRUCTION COMPLETE")
        print("=" * 50)
        print(f"📊 Total new memberships: {total_memberships}")
        print(f"🏛️ Senate memberships: {senate_count}")
        print(f"🏛️ House memberships: {house_count}")
        
        return True
    
    def close(self):
        """Close database connection."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

def main():
    """Main execution function."""
    # Database connection
    db_connection = "host=localhost port=5433 dbname=congress_data user=postgres password=mDf3S9ZnBpQqJvGsY1"
    
    # Find the latest data file
    data_files = [f for f in os.listdir('.') if f.startswith('authoritative_committee_data_')]
    if not data_files:
        print("❌ No authoritative data files found")
        return
    
    latest_file = sorted(data_files)[-1]
    print(f"📄 Using data file: {latest_file}")
    
    # Run reconstruction
    reconstructor = DatabaseReconstructor(db_connection)
    success = reconstructor.run_reconstruction(latest_file)
    reconstructor.close()
    
    if success:
        print("\n🎯 Next step: Run validation tests")
        print("   python3 validate_reconstruction.py")
    else:
        print("\n❌ Reconstruction failed - check errors above")

if __name__ == "__main__":
    main()