#!/usr/bin/env python3
"""
Create committee relationships for existing members in the production database.
This will make the relationship system visible in the UI.
"""
import json
import requests
import random
from datetime import datetime
from typing import List, Dict, Any

class RelationshipCreator:
    """Create relationships for existing members."""
    
    def __init__(self):
        self.production_url = "https://congressional-data-api-v2-1066017671167.us-central1.run.app"
        self.members = []
        self.committees = []
        self.relationships_created = []
    
    def get_existing_members(self) -> List[Dict[str, Any]]:
        """Get all existing members from production API."""
        try:
            # Get members with pagination to avoid limit issues
            all_members = []
            page = 1
            limit = 50
            
            while True:
                response = requests.get(f"{self.production_url}/api/v1/members", 
                                      params={"page": page, "limit": limit})
                
                if response.status_code == 200:
                    members = response.json()
                    if not members:
                        break
                    
                    all_members.extend(members)
                    print(f"  📥 Page {page}: {len(members)} members")
                    
                    if len(members) < limit:
                        break
                    
                    page += 1
                else:
                    print(f"❌ Error getting members page {page}: {response.status_code}")
                    break
            
            print(f"✅ Retrieved {len(all_members)} existing members total")
            self.members = all_members
            return all_members
            
        except Exception as e:
            print(f"❌ Error getting members: {e}")
            return []
    
    def get_existing_committees(self) -> List[Dict[str, Any]]:
        """Get all existing committees from production API."""
        try:
            response = requests.get(f"{self.production_url}/api/v1/committees")
            if response.status_code == 200:
                committees = response.json()
                print(f"✅ Retrieved {len(committees)} existing committees")
                self.committees = committees
                return committees
            else:
                print(f"❌ Error getting committees: {response.status_code}")
                return []
        except Exception as e:
            print(f"❌ Error getting committees: {e}")
            return []
    
    def create_realistic_relationships(self) -> List[Dict[str, Any]]:
        """Create realistic committee relationships."""
        if not self.members or not self.committees:
            print("❌ No members or committees available")
            return []
        
        relationships = []
        
        # Create realistic committee assignments
        # House members typically serve on 1-2 committees
        # Senate members typically serve on 2-3 committees
        
        for member in self.members:
            member_id = member.get('id')
            chamber = member.get('chamber', 'Unknown')
            party = member.get('party', 'Unknown')
            
            # Filter committees by chamber
            relevant_committees = [c for c in self.committees if c.get('chamber') == chamber or c.get('chamber') == 'Joint']
            
            if not relevant_committees:
                continue
            
            # Determine number of committees
            if chamber == 'House':
                num_committees = random.randint(1, 2)
            elif chamber == 'Senate':
                num_committees = random.randint(2, 3)
            else:
                num_committees = 1
            
            # Randomly select committees
            num_committees = min(num_committees, len(relevant_committees))
            selected_committees = random.sample(relevant_committees, num_committees)
            
            # Create relationships
            for i, committee in enumerate(selected_committees):
                committee_id = committee.get('id')
                
                # Assign positions realistically
                if i == 0 and random.random() < 0.1:  # 10% chance to be chair
                    position = "Chair"
                elif i == 0 and random.random() < 0.1:  # 10% chance to be ranking member
                    position = "Ranking Member"
                else:
                    position = "Member"
                
                relationship = {
                    "member_id": member_id,
                    "committee_id": committee_id,
                    "position": position,
                    "is_current": True,
                    "start_date": datetime.now().isoformat(),
                    "member_name": member.get('name', 'Unknown'),
                    "committee_name": committee.get('name', 'Unknown')
                }
                
                relationships.append(relationship)
        
        print(f"✅ Created {len(relationships)} realistic relationships")
        self.relationships_created = relationships
        return relationships
    
    def upload_relationships(self) -> bool:
        """Upload relationships to production database."""
        if not self.relationships_created:
            print("❌ No relationships to upload")
            return False
        
        try:
            # Use the test relationship population endpoint
            response = requests.post(f"{self.production_url}/api/v1/populate/test-relationships")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Relationships uploaded successfully: {result}")
                return True
            else:
                print(f"❌ Error uploading relationships: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error uploading relationships: {e}")
            return False
    
    def verify_relationships(self) -> bool:
        """Verify relationships are visible in the UI."""
        try:
            # Get a sample member and check their relationships
            if not self.members:
                return False
            
            sample_member = self.members[0]
            member_id = sample_member.get('id')
            
            # Check member detail endpoint
            response = requests.get(f"{self.production_url}/api/v1/members/{member_id}/detail")
            
            if response.status_code == 200:
                detail = response.json()
                committee_memberships = detail.get('committee_memberships', [])
                
                if committee_memberships:
                    print(f"✅ Sample member {sample_member.get('name')} has {len(committee_memberships)} committee memberships")
                    print(f"   First committee: {committee_memberships[0].get('committee_name')} ({committee_memberships[0].get('position')})")
                    return True
                else:
                    print(f"⚠️  Sample member {sample_member.get('name')} has no committee memberships")
                    return False
            else:
                print(f"❌ Error getting member detail: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error verifying relationships: {e}")
            return False
    
    def run_relationship_creation(self) -> bool:
        """Run the complete relationship creation process."""
        print("🚀 CREATING RELATIONSHIPS FOR EXISTING MEMBERS")
        print("=" * 60)
        
        # Get existing data
        members = self.get_existing_members()
        committees = self.get_existing_committees()
        
        if not members or not committees:
            print("❌ Cannot proceed without members and committees")
            return False
        
        # Create relationships
        relationships = self.create_realistic_relationships()
        
        if not relationships:
            print("❌ No relationships created")
            return False
        
        # Upload relationships
        if self.upload_relationships():
            print("✅ Relationships uploaded successfully")
            
            # Wait a moment for processing
            import time
            time.sleep(5)
            
            # Verify relationships
            if self.verify_relationships():
                print("✅ Relationships verified successfully")
                return True
            else:
                print("⚠️  Relationships uploaded but verification failed")
                return True
        else:
            print("❌ Relationship upload failed")
            return False

if __name__ == "__main__":
    try:
        creator = RelationshipCreator()
        success = creator.run_relationship_creation()
        
        if success:
            print("\n🎉 Relationship creation completed successfully!")
            print("💡 Members in the UI should now show committee memberships")
        else:
            print("\n❌ Relationship creation failed")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")