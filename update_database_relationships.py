#!/usr/bin/env python3
"""
Update database with committee relationships
This script will update the production database with committee membership data
"""

import json
import requests
from datetime import datetime
from typing import List, Dict, Optional
import os

class DatabaseRelationshipUpdater:
    def __init__(self, relationships_file: str):
        self.relationships_file = relationships_file
        self.production_api_url = "https://congressional-data-api-v3-1066017671167.us-central1.run.app/api/v1"
        self.relationships = []
        
    def load_relationships(self) -> bool:
        """Load relationships from JSON file"""
        try:
            with open(self.relationships_file, 'r') as f:
                data = json.load(f)
                self.relationships = data.get('relationships', [])
                print(f"📥 Loaded {len(self.relationships)} relationships from {self.relationships_file}")
                return True
        except Exception as e:
            print(f"❌ Error loading relationships: {e}")
            return False
    
    def create_member_committee_json(self) -> Dict:
        """Create JSON structure for updating member committee assignments"""
        print("🔄 Creating member committee JSON structure...")
        
        # Group relationships by member
        member_committees = {}
        
        for rel in self.relationships:
            member_id = rel['member_id']
            if member_id not in member_committees:
                member_committees[member_id] = {
                    'member_id': member_id,
                    'member_name': rel['member_name'],
                    'member_state': rel['member_state'],
                    'committees': []
                }
            
            member_committees[member_id]['committees'].append({
                'id': rel['committee_id'],
                'name': rel['committee_name'],
                'role': rel.get('role', 'Member')
            })
        
        print(f"✅ Created committee assignments for {len(member_committees)} members")
        
        # Show some examples
        print("📋 Sample assignments:")
        for member_id, data in list(member_committees.items())[:3]:
            print(f"  - {data['member_name']} ({data['member_state']}): {len(data['committees'])} committees")
            for committee in data['committees']:
                print(f"    • {committee['name']}")
        
        return member_committees
    
    def create_committee_member_json(self) -> Dict:
        """Create JSON structure for updating committee member listings"""
        print("🔄 Creating committee member JSON structure...")
        
        # Group relationships by committee
        committee_members = {}
        
        for rel in self.relationships:
            committee_id = rel['committee_id']
            if committee_id not in committee_members:
                committee_members[committee_id] = {
                    'committee_id': committee_id,
                    'committee_name': rel['committee_name'],
                    'members': []
                }
            
            committee_members[committee_id]['members'].append({
                'id': rel['member_id'],
                'name': rel['member_name'],
                'state': rel['member_state'],
                'role': rel.get('role', 'Member')
            })
        
        print(f"✅ Created member listings for {len(committee_members)} committees")
        
        # Show some examples
        print("📋 Sample committee rosters:")
        for committee_id, data in list(committee_members.items())[:3]:
            print(f"  - {data['committee_name']}: {len(data['members'])} members")
            for member in data['members'][:3]:
                print(f"    • {member['name']} ({member['state']})")
        
        return committee_members
    
    def create_sql_update_script(self, member_committees: Dict) -> str:
        """Create SQL script to update member committees"""
        print("🔄 Creating SQL update script...")
        
        sql_statements = []
        
        # Add column if it doesn't exist (safe to run multiple times)
        sql_statements.append("-- Add committees column to members table if not exists")
        sql_statements.append("ALTER TABLE members ADD COLUMN IF NOT EXISTS committees JSONB DEFAULT '[]'::jsonb;")
        sql_statements.append("")
        
        # Update statements for each member
        sql_statements.append("-- Update member committee assignments")
        
        for member_id, data in member_committees.items():
            committees_json = json.dumps(data['committees'])
            
            # Escape single quotes in JSON
            committees_json = committees_json.replace("'", "''")
            
            sql_statements.append(f"-- Update {data['member_name']} ({data['member_state']})")
            sql_statements.append(f"UPDATE members SET committees = '{committees_json}'::jsonb WHERE id = {member_id};")
            sql_statements.append("")
        
        # Create index for better performance
        sql_statements.append("-- Create index for committee queries")
        sql_statements.append("CREATE INDEX IF NOT EXISTS idx_members_committees ON members USING gin(committees);")
        sql_statements.append("")
        
        sql_script = "\n".join(sql_statements)
        
        print(f"✅ Created SQL script with {len(member_committees)} member updates")
        
        return sql_script
    
    def test_api_integration(self) -> bool:
        """Test if we can integrate with the API to update relationships"""
        print("🔍 Testing API integration...")
        
        # Test getting a single member to see current structure
        try:
            response = requests.get(f"{self.production_api_url}/members?limit=1")
            if response.status_code == 200:
                data = response.json()
                if data:
                    member = data[0] if isinstance(data, list) else data.get('members', [{}])[0]
                    print(f"📋 Current member structure: {list(member.keys())}")
                    
                    # Check if committees field exists
                    if 'committees' in member:
                        print(f"✅ Member already has committees field: {member.get('committees')}")
                    else:
                        print("❌ Member does not have committees field - need to add it")
                    
                    return True
                else:
                    print("❌ No member data returned")
                    return False
            else:
                print(f"❌ API request failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error testing API: {e}")
            return False
    
    def generate_update_files(self) -> Dict:
        """Generate all update files and scripts"""
        print("📁 Generating update files...")
        
        # Create member committees structure
        member_committees = self.create_member_committee_json()
        
        # Create committee members structure
        committee_members = self.create_committee_member_json()
        
        # Create SQL script
        sql_script = self.create_sql_update_script(member_committees)
        
        # Generate timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save files
        files_created = {}
        
        # Member committees JSON
        member_committees_file = f"member_committees_update_{timestamp}.json"
        with open(member_committees_file, 'w') as f:
            json.dump(member_committees, f, indent=2)
        files_created['member_committees'] = member_committees_file
        
        # Committee members JSON
        committee_members_file = f"committee_members_update_{timestamp}.json"
        with open(committee_members_file, 'w') as f:
            json.dump(committee_members, f, indent=2)
        files_created['committee_members'] = committee_members_file
        
        # SQL script
        sql_file = f"database_committee_update_{timestamp}.sql"
        with open(sql_file, 'w') as f:
            f.write(sql_script)
        files_created['sql_script'] = sql_file
        
        # Summary report
        summary = {
            'timestamp': datetime.now().isoformat(),
            'relationships_file': self.relationships_file,
            'total_relationships': len(self.relationships),
            'unique_members': len(member_committees),
            'unique_committees': len(committee_members),
            'files_created': files_created,
            'next_steps': [
                'Review generated SQL script',
                'Test SQL script in staging environment',
                'Execute SQL script in production database',
                'Verify API returns committee data',
                'Test relationship queries'
            ]
        }
        
        summary_file = f"database_update_summary_{timestamp}.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        files_created['summary'] = summary_file
        
        return files_created
    
    def run_database_update_preparation(self) -> Dict:
        """Run complete database update preparation"""
        print("🚀 Starting Database Update Preparation")
        print("=" * 60)
        
        # Step 1: Load relationships
        if not self.load_relationships():
            return {'error': 'Failed to load relationships'}
        
        # Step 2: Test API integration
        if not self.test_api_integration():
            print("⚠️  Warning: API integration test failed, but continuing...")
        
        # Step 3: Generate update files
        files_created = self.generate_update_files()
        
        # Step 4: Final report
        print(f"\n📊 UPDATE PREPARATION COMPLETE")
        print(f"Relationships processed: {len(self.relationships)}")
        print(f"Files created: {len(files_created)}")
        print(f"\n📁 Generated files:")
        for file_type, filename in files_created.items():
            print(f"  - {file_type}: {filename}")
        
        return {
            'success': True,
            'relationships_processed': len(self.relationships),
            'files_created': files_created,
            'next_steps': [
                'Review database_committee_update_*.sql script',
                'Test in staging environment first',
                'Execute in production when ready',
                'Verify API includes committee data',
                'Test committee relationship queries'
            ]
        }

def main():
    """Main function to prepare database updates"""
    
    # Find the most recent relationships file
    import glob
    relationship_files = glob.glob("manual_senate_assignments_*.json")
    
    if not relationship_files:
        print("❌ No relationship files found. Run manual_committee_assignment.py first.")
        return
    
    # Use the most recent file
    latest_file = max(relationship_files, key=os.path.getctime)
    print(f"📁 Using relationships file: {latest_file}")
    
    try:
        updater = DatabaseRelationshipUpdater(latest_file)
        
        # Run preparation
        results = updater.run_database_update_preparation()
        
        if results.get('success'):
            print("\n✅ DATABASE UPDATE PREPARATION SUCCESSFUL")
            print("\n🎯 NEXT STEPS:")
            for step in results['next_steps']:
                print(f"  - {step}")
        else:
            print(f"\n❌ Error: {results.get('error')}")
            
    except Exception as e:
        print(f"❌ Fatal error: {e}")

if __name__ == "__main__":
    main()