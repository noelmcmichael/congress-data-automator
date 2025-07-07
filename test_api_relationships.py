#!/usr/bin/env python3
"""
Test the API relationship endpoints with members who actually have committee assignments.
"""

import requests
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "https://congressional-data-api-v2-1066017671167.us-central1.run.app/api/v1"

def test_api_relationships():
    """Test the API relationship endpoints."""
    
    # Test members who have committee assignments (based on our debug)
    test_member_ids = [19, 24, 62, 63, 73, 95, 109, 111, 117]
    
    logger.info("🧪 TESTING API RELATIONSHIPS")
    logger.info("="*60)
    
    success_count = 0
    total_committees = 0
    
    for member_id in test_member_ids:
        try:
            # Test member details
            response = requests.get(f"{BASE_URL}/members/{member_id}")
            if response.status_code == 200:
                member_data = response.json()
                member_name = f"{member_data['first_name']} {member_data['last_name']}"
                
                # Test member committees
                response = requests.get(f"{BASE_URL}/members/{member_id}/committees")
                if response.status_code == 200:
                    committees = response.json()
                    committee_count = len(committees)
                    total_committees += committee_count
                    
                    if committee_count > 0:
                        success_count += 1
                        logger.info(f"✅ {member_name} ({member_data['party']}-{member_data['state']}): {committee_count} committees")
                        
                        for committee in committees:
                            committee_name = committee['committee']['name']
                            position = committee['position']
                            logger.info(f"   - {committee_name} ({position})")
                    else:
                        logger.warning(f"⚠️  {member_name}: No committees")
                else:
                    logger.error(f"❌ Failed to get committees for member {member_id}")
            else:
                logger.error(f"❌ Failed to get member {member_id}")
                
        except Exception as e:
            logger.error(f"❌ Error testing member {member_id}: {e}")
    
    logger.info("="*60)
    logger.info(f"📊 RESULTS:")
    logger.info(f"Members with committees: {success_count}/{len(test_member_ids)}")
    logger.info(f"Total committee assignments: {total_committees}")
    logger.info(f"Average committees per member: {total_committees / len(test_member_ids):.1f}")
    
    # Test committee member listings
    logger.info("\n🏛️ TESTING COMMITTEE MEMBER LISTINGS")
    logger.info("="*60)
    
    # Test major committees
    major_committees = [
        "Committee on Appropriations",
        "Committee on Armed Services", 
        "Committee on the Judiciary",
        "Committee on Foreign Affairs",
        "Committee on Energy and Commerce"
    ]
    
    committee_success = 0
    total_members = 0
    
    try:
        # Get all committees
        response = requests.get(f"{BASE_URL}/committees")
        if response.status_code == 200:
            all_committees = response.json()
            
            for committee_name in major_committees:
                # Find the committee
                committee = next((c for c in all_committees if c['name'] == committee_name), None)
                if committee:
                    committee_id = committee['id']
                    
                    # Get committee members
                    response = requests.get(f"{BASE_URL}/committees/{committee_id}/members")
                    if response.status_code == 200:
                        members = response.json()
                        member_count = len(members)
                        total_members += member_count
                        
                        if member_count > 0:
                            committee_success += 1
                            logger.info(f"✅ {committee_name}: {member_count} members")
                            
                            # Show first few members
                            for i, member in enumerate(members[:3]):
                                member_name = f"{member['member']['first_name']} {member['member']['last_name']}"
                                position = member['position']
                                logger.info(f"   - {member_name} ({position})")
                            
                            if len(members) > 3:
                                logger.info(f"   ... and {len(members) - 3} more members")
                        else:
                            logger.warning(f"⚠️  {committee_name}: No members")
                    else:
                        logger.error(f"❌ Failed to get members for {committee_name}")
                else:
                    logger.error(f"❌ Committee not found: {committee_name}")
    
    except Exception as e:
        logger.error(f"❌ Error testing committees: {e}")
    
    logger.info("="*60)
    logger.info(f"📊 COMMITTEE RESULTS:")
    logger.info(f"Committees with members: {committee_success}/{len(major_committees)}")
    logger.info(f"Total member assignments: {total_members}")
    
    # Overall success
    if success_count >= len(test_member_ids) * 0.8 and committee_success >= len(major_committees) * 0.8:
        logger.info("\n🎉 API RELATIONSHIP TEST: SUCCESS!")
        logger.info("Both member → committee and committee → member relationships working!")
        return True
    else:
        logger.error("\n❌ API RELATIONSHIP TEST: ISSUES FOUND")
        return False

if __name__ == "__main__":
    test_api_relationships()