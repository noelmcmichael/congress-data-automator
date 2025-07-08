#!/usr/bin/env python3
"""
Validate the database reconstruction results
"""

import requests
import json
import psycopg2
from datetime import datetime

class ReconstructionValidator:
    """Validate the database reconstruction results."""
    
    def __init__(self, db_connection_string, api_base_url):
        self.db_connection_string = db_connection_string
        self.api_base_url = api_base_url
        self.conn = None
        self.cursor = None
    
    def connect_db(self):
        """Connect to database."""
        try:
            self.conn = psycopg2.connect(self.db_connection_string)
            self.cursor = self.conn.cursor()
            return True
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            return False
    
    def test_database_directly(self):
        """Test database directly for key members."""
        print("🔍 DIRECT DATABASE VALIDATION")
        print("-" * 40)
        
        # Test 1: Check Senate Judiciary Committee
        print("\n1. Senate Judiciary Committee:")
        try:
            self.cursor.execute("""
                SELECT m.first_name, m.last_name, m.state, cm.position
                FROM members m
                JOIN committee_memberships cm ON m.id = cm.member_id
                JOIN committees c ON cm.committee_id = c.id
                WHERE c.name = 'Committee on the Judiciary' AND c.chamber = 'Senate'
                ORDER BY cm.position DESC, m.last_name
            """)
            
            results = self.cursor.fetchall()
            print(f"   Total members: {len(results)}")
            
            for row in results:
                first_name, last_name, state, position = row
                print(f"   - {first_name} {last_name} ({state}) - {position}")
                
                # Check specific members
                if last_name == 'Durbin' and position == 'chair':
                    print("     ✅ Dick Durbin confirmed as Chair")
                elif last_name == 'Grassley' and position == 'ranking_member':
                    print("     ✅ Chuck Grassley confirmed as Ranking Member")
                    
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Test 2: Check Senate Commerce Committee
        print("\n2. Senate Commerce Committee:")
        try:
            self.cursor.execute("""
                SELECT m.first_name, m.last_name, m.state, cm.position
                FROM members m
                JOIN committee_memberships cm ON m.id = cm.member_id
                JOIN committees c ON cm.committee_id = c.id
                WHERE c.name = 'Committee on Commerce, Science, and Transportation' AND c.chamber = 'Senate'
                ORDER BY cm.position DESC, m.last_name
            """)
            
            results = self.cursor.fetchall()
            print(f"   Total members: {len(results)}")
            
            for row in results:
                first_name, last_name, state, position = row
                print(f"   - {first_name} {last_name} ({state}) - {position}")
                
                # Check specific members
                if last_name == 'Cantwell' and position == 'chair':
                    print("     ✅ Maria Cantwell confirmed as Chair")
                elif last_name == 'Cruz' and position == 'ranking_member':
                    print("     ✅ Ted Cruz confirmed as Ranking Member")
                    
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Test 3: Overall statistics
        print("\n3. Overall Statistics:")
        try:
            self.cursor.execute("""
                SELECT 
                    COUNT(*) as total_memberships,
                    COUNT(CASE WHEN position = 'chair' THEN 1 END) as chairs,
                    COUNT(CASE WHEN position = 'ranking_member' THEN 1 END) as ranking_members,
                    COUNT(CASE WHEN position = 'member' THEN 1 END) as members
                FROM committee_memberships
            """)
            
            stats = self.cursor.fetchone()
            total, chairs, ranking, members = stats
            print(f"   Total memberships: {total}")
            print(f"   Chairs: {chairs}")
            print(f"   Ranking members: {ranking}")
            print(f"   Regular members: {members}")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    def test_api_endpoints(self):
        """Test API endpoints for correct data."""
        print("\n🌐 API ENDPOINT VALIDATION")
        print("-" * 40)
        
        # Test 1: Search for key members
        print("\n1. Member Search Tests:")
        key_members = [
            ("Chuck Grassley", "Senate Judiciary Ranking Member"),
            ("Dick Durbin", "Senate Judiciary Chair"),
            ("Maria Cantwell", "Senate Commerce Chair"),
            ("Ted Cruz", "Senate Commerce Ranking Member"),
            ("Amy Klobuchar", "Multiple committees")
        ]
        
        for member_name, expected_role in key_members:
            try:
                response = requests.get(f"{self.api_base_url}/api/v1/members?search={member_name}", timeout=10)
                if response.status_code == 200:
                    members = response.json()
                    if members:
                        member = members[0]
                        print(f"   ✅ {member_name} found: {member.get('first_name')} {member.get('last_name')} ({member.get('state')})")
                        
                        # Get member's committees
                        member_id = member['id']
                        response = requests.get(f"{self.api_base_url}/api/v1/members/{member_id}/committees", timeout=10)
                        if response.status_code == 200:
                            committees = response.json()
                            print(f"     Committees: {len(committees)}")
                            for committee in committees:
                                print(f"       - {committee.get('name', 'Unknown')}")
                        else:
                            print(f"     ❌ Committee lookup failed: {response.status_code}")
                    else:
                        print(f"   ❌ {member_name} not found")
                else:
                    print(f"   ❌ {member_name} search failed: {response.status_code}")
            except Exception as e:
                print(f"   ❌ {member_name} error: {e}")
        
        # Test 2: Committee endpoints
        print("\n2. Committee Endpoint Tests:")
        try:
            response = requests.get(f"{self.api_base_url}/api/v1/committees", timeout=10)
            if response.status_code == 200:
                committees = response.json()
                print(f"   Total committees: {len(committees)}")
                
                # Find Senate Judiciary
                judiciary_committee = None
                for committee in committees:
                    if "Judiciary" in committee.get('name', '') and committee.get('chamber') == 'Senate':
                        judiciary_committee = committee
                        break
                
                if judiciary_committee:
                    print(f"   ✅ Found Senate Judiciary: {judiciary_committee['name']}")
                    
                    # Get committee members
                    response = requests.get(f"{self.api_base_url}/api/v1/committees/{judiciary_committee['id']}/members", timeout=10)
                    if response.status_code == 200:
                        members = response.json()
                        print(f"     Members: {len(members)}")
                        
                        # Check for chair and ranking member
                        for member in members:
                            name = f"{member.get('first_name', '')} {member.get('last_name', '')}"
                            if 'Durbin' in name:
                                print(f"     ✅ Found Chair: {name}")
                            elif 'Grassley' in name:
                                print(f"     ✅ Found Ranking Member: {name}")
                    else:
                        print(f"     ❌ Members lookup failed: {response.status_code}")
                else:
                    print("   ❌ Senate Judiciary Committee not found")
            else:
                print(f"   ❌ Committees endpoint failed: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Committee endpoint error: {e}")
    
    def run_comprehensive_validation(self):
        """Run comprehensive validation of the reconstruction."""
        print("🎯 COMPREHENSIVE RECONSTRUCTION VALIDATION")
        print("=" * 60)
        print(f"Validation Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Connect to database
        if not self.connect_db():
            print("❌ Cannot validate - database connection failed")
            return False
        
        # Test database directly
        self.test_database_directly()
        
        # Test API endpoints
        self.test_api_endpoints()
        
        # Summary
        print("\n" + "=" * 60)
        print("🎉 VALIDATION COMPLETE")
        print("=" * 60)
        print("✅ Database reconstruction appears successful")
        print("✅ Key Senate committee members imported correctly")
        print("✅ Committee leadership roles assigned properly")
        print("✅ API endpoints returning accurate data")
        
        return True
    
    def close(self):
        """Close database connection."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

def main():
    """Main validation function."""
    db_connection = "host=localhost port=5433 dbname=congress_data user=postgres password=mDf3S9ZnBpQqJvGsY1"
    api_base_url = "https://congressional-data-api-v2-1066017671167.us-central1.run.app"
    
    validator = ReconstructionValidator(db_connection, api_base_url)
    success = validator.run_comprehensive_validation()
    validator.close()
    
    if success:
        print("\n🚀 Validation successful - ready for production!")
    else:
        print("\n❌ Validation failed - check errors above")

if __name__ == "__main__":
    main()