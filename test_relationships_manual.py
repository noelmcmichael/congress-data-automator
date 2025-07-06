#!/usr/bin/env python3
"""
Manual test script to populate relationship data for testing.
"""
import os
import sys
import asyncio
import random
from datetime import datetime

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.member import Member
from app.models.committee import Committee, CommitteeMembership

async def create_test_relationships():
    """Create some test relationships for demonstration."""
    
    # Get database session
    db_gen = get_db()
    db: Session = next(db_gen)
    
    try:
        # Get some members and committees
        members = db.query(Member).limit(10).all()
        committees = db.query(Committee).limit(5).all()
        
        print(f"Found {len(members)} members and {len(committees)} committees")
        
        # Create some test relationships
        relationships_created = 0
        
        for i, member in enumerate(members):
            # Assign each member to 1-3 random committees
            num_committees = random.randint(1, min(3, len(committees)))
            assigned_committees = random.sample(committees, num_committees)
            
            for j, committee in enumerate(assigned_committees):
                # Check if relationship already exists
                existing = db.query(CommitteeMembership).filter(
                    CommitteeMembership.member_id == member.id,
                    CommitteeMembership.committee_id == committee.id
                ).first()
                
                if not existing:
                    # Determine position
                    if j == 0 and i < 2:  # First 2 members get chair positions
                        position = "Chair"
                    elif j == 0 and i < 4:  # Next 2 get ranking member
                        position = "Ranking Member"
                    else:
                        position = "Member"
                    
                    # Create membership
                    membership = CommitteeMembership(
                        member_id=member.id,
                        committee_id=committee.id,
                        position=position,
                        is_current=True,
                        start_date=datetime.now()
                    )
                    
                    db.add(membership)
                    relationships_created += 1
                    
                    print(f"Created: {member.first_name} {member.last_name} -> {committee.name} ({position})")
        
        # Commit changes
        db.commit()
        print(f"\n✅ Created {relationships_created} test relationships")
        
        # Test the relationships
        print("\n🔍 Testing relationships:")
        for member in members[:3]:
            memberships = db.query(CommitteeMembership).filter(
                CommitteeMembership.member_id == member.id
            ).all()
            
            print(f"{member.first_name} {member.last_name}: {len(memberships)} committees")
            for membership in memberships:
                print(f"  - {membership.committee.name} ({membership.position})")
        
        return relationships_created
        
    except Exception as e:
        print(f"❌ Error creating test relationships: {e}")
        db.rollback()
        return 0
    finally:
        db.close()

async def test_api_endpoints():
    """Test the API endpoints with the new relationship data."""
    import requests
    
    base_url = "https://congressional-data-api-v2-1066017671167.us-central1.run.app"
    
    print("\n🧪 Testing API endpoints:")
    
    # Get a member and test detail endpoint
    members_response = requests.get(f"{base_url}/api/v1/members?limit=1")
    members = members_response.json()
    
    if members:
        member_id = members[0]['id']
        
        # Test member detail
        detail_response = requests.get(f"{base_url}/api/v1/members/{member_id}/detail")
        if detail_response.status_code == 200:
            detail = detail_response.json()
            print(f"✅ {detail['member']['first_name']} {detail['member']['last_name']}")
            print(f"   Committees: {len(detail['committee_memberships'])}")
            print(f"   Statistics: {detail['statistics']}")
            
            for membership in detail['committee_memberships']:
                print(f"   - {membership['committee']['name']} ({membership['position']})")
        else:
            print(f"❌ Member detail failed: {detail_response.status_code}")
    
    # Test committee detail
    committees_response = requests.get(f"{base_url}/api/v1/committees?limit=1")
    committees = committees_response.json()
    
    if committees:
        committee_id = committees[0]['id']
        
        detail_response = requests.get(f"{base_url}/api/v1/committees/{committee_id}/detail")
        if detail_response.status_code == 200:
            detail = detail_response.json()
            print(f"\n✅ Committee: {detail['committee']['name']}")
            print(f"   Members: {len(detail['memberships'])}")
            print(f"   Statistics: {detail['statistics']}")
            
            for membership in detail['memberships']:
                print(f"   - {membership['member']['first_name']} {membership['member']['last_name']} ({membership['position']})")
        else:
            print(f"❌ Committee detail failed: {detail_response.status_code}")

async def main():
    """Main function to run the test."""
    print("🔧 Creating test relationship data...")
    
    relationships_created = await create_test_relationships()
    
    if relationships_created > 0:
        print(f"\n⏳ Waiting for deployment to reflect changes...")
        import time
        time.sleep(10)
        
        await test_api_endpoints()
        
        print("\n🎉 Test completed!")
        print("Next steps:")
        print("1. Implement frontend detail pages")
        print("2. Fix automated relationship data collection")
        print("3. Add committee hierarchy support")
        print("4. Create relationship visualizations")
    else:
        print("❌ No relationships created - check database connectivity")

if __name__ == "__main__":
    asyncio.run(main())