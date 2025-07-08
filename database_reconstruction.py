#!/usr/bin/env python3
"""
Database reconstruction with authoritative committee data
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
    
    def backup_current_state(self):
        """Create backup of current committee memberships."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_table = f"committee_memberships_emergency_backup_{timestamp}"
            
            self.cursor.execute(f"""
                CREATE TABLE {backup_table} AS 
                SELECT * FROM committee_memberships;
            """)
            
            self.cursor.execute(f"SELECT COUNT(*) FROM {backup_table};")
            count = self.cursor.fetchone()[0]
            
            self.conn.commit()
            print(f"✅ Backup created: {backup_table} ({count} records)")
            return backup_table
        except Exception as e:
            print(f"❌ Backup failed: {e}")
            return None
    
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
    
    def find_or_create_committee(self, committee_name, chamber):
        """Find existing committee or create new one."""
        try:
            # First try to find existing committee
            self.cursor.execute("""
                SELECT id FROM committees 
                WHERE name = %s AND chamber = %s
            """, (committee_name, chamber))
            
            result = self.cursor.fetchone()
            if result:
                return result[0]
            
            # Create new committee
            self.cursor.execute("""
                INSERT INTO committees (name, chamber, committee_type, created_at)
                VALUES (%s, %s, 'standing', NOW())
                RETURNING id
            """, (committee_name, chamber))
            
            committee_id = self.cursor.fetchone()[0]
            self.conn.commit()
            print(f"  ✅ Created committee: {committee_name} (ID: {committee_id})")
            return committee_id
            
        except Exception as e:
            print(f"❌ Committee creation failed: {e}")
            self.conn.rollback()
            return None
    
    def find_member_by_name(self, member_name, state=None):
        """Find member by name and optionally state."""
        try:
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
            return None
            
        except Exception as e:
            print(f"❌ Member lookup failed for {member_name}: {e}")
            return None
    
    def create_committee_membership(self, member_id, committee_id, role='member'):
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
                INSERT INTO committee_memberships (member_id, committee_id, role, created_at)
                VALUES (%s, %s, %s, NOW())
            """, (member_id, committee_id, role))
            
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
            
            print(f"\n  📋 Processing {committee_name}...")
            
            # Find or create committee
            committee_id = self.find_or_create_committee(committee_name, chamber)
            if not committee_id:
                print(f"    ❌ Failed to create committee: {committee_name}")
                continue
            
            # Process members
            members_added = 0
            for member_data in members:
                member_name = member_data['name']
                state = member_data.get('state')
                role = member_data.get('role', 'member').lower()
                
                # Find member in database
                member = self.find_member_by_name(member_name, state)
                if not member:
                    print(f"    ⚠️ Member not found: {member_name} ({state})")
                    continue
                
                # Verify chamber matches
                if member['chamber'].lower() != chamber.lower():
                    print(f"    ⚠️ Chamber mismatch: {member_name} is {member['chamber']}, not {chamber}")
                    continue
                
                # Create membership
                if self.create_committee_membership(member['id'], committee_id, role):
                    members_added += 1
                    print(f"    ✅ Added {member_name} ({role})")
                else:
                    print(f"    ❌ Failed to add {member_name}")
            
            print(f"  📊 {committee_name}: {members_added}/{len(members)} members added")
            total_members_added += members_added
        
        self.conn.commit()
        print(f"\n✅ {chamber} import complete: {total_members_added} total members added")
        return total_members_added
    
    def run_reconstruction(self, data_file):
        """Run complete database reconstruction."""
        print("🚀 Starting database reconstruction...")
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
        
        # Backup current state
        backup_table = self.backup_current_state()
        if not backup_table:
            print("❌ Backup failed - aborting reconstruction")
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
        print("🎉 DATABASE RECONSTRUCTION COMPLETE")
        print("=" * 50)
        print(f"📊 Total new memberships: {total_memberships}")
        print(f"🏛️ Senate memberships: {senate_count}")
        print(f"🏛️ House memberships: {house_count}")
        print(f"💾 Backup table: {backup_table}")
        
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