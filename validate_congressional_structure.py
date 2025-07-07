#!/usr/bin/env python3
"""
Validate that the congressional structure matches real congressional data.
"""

import requests
import json
import logging
from collections import defaultdict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "https://congressional-data-api-v2-1066017671167.us-central1.run.app/api/v1"

def validate_congressional_structure():
    """Validate the congressional structure against real data."""
    
    logger.info("🏛️ VALIDATING CONGRESSIONAL STRUCTURE")
    logger.info("="*60)
    
    # Test 1: Validate major committees exist
    logger.info("1. Testing major committees presence...")
    
    major_house_committees = [
        "Committee on Agriculture",
        "Committee on Appropriations",
        "Committee on Armed Services",
        "Committee on the Budget",
        "Committee on Education and the Workforce",
        "Committee on Energy and Commerce",
        "Committee on Financial Services",
        "Committee on Foreign Affairs",
        "Committee on Homeland Security",
        "Committee on House Administration",
        "Committee on the Judiciary",
        "Committee on Natural Resources",
        "Committee on Oversight and Accountability",
        "Committee on Rules",
        "Committee on Science, Space, and Technology",
        "Committee on Small Business",
        "Committee on Transportation and Infrastructure",
        "Committee on Veterans' Affairs",
        "Committee on Ways and Means"
    ]
    
    major_senate_committees = [
        "Committee on Agriculture, Nutrition, and Forestry",
        "Committee on Appropriations",
        "Committee on Armed Services",
        "Committee on Banking, Housing, and Urban Affairs",
        "Committee on the Budget",
        "Committee on Commerce, Science, and Transportation",
        "Committee on Energy and Natural Resources",
        "Committee on Environment and Public Works",
        "Committee on Finance",
        "Committee on Foreign Relations",
        "Committee on Health, Education, Labor and Pensions",
        "Committee on Homeland Security and Governmental Affairs",
        "Committee on the Judiciary",
        "Committee on Rules and Administration",
        "Committee on Small Business and Entrepreneurship",
        "Committee on Veterans' Affairs"
    ]
    
    try:
        response = requests.get(f"{BASE_URL}/committees")
        if response.status_code == 200:
            all_committees = response.json()
            
            # Check House committees
            house_committees = [c for c in all_committees if c['chamber'] == 'House']
            found_house = 0
            
            logger.info("Major House committees:")
            for committee_name in major_house_committees:
                found = any(c['name'] == committee_name for c in house_committees)
                if found:
                    found_house += 1
                    logger.info(f"  ✅ {committee_name}")
                else:
                    logger.warning(f"  ❌ {committee_name}")
            
            # Check Senate committees
            senate_committees = [c for c in all_committees if c['chamber'] == 'Senate']
            found_senate = 0
            
            logger.info("\nMajor Senate committees:")
            for committee_name in major_senate_committees:
                found = any(c['name'] == committee_name for c in senate_committees)
                if found:
                    found_senate += 1
                    logger.info(f"  ✅ {committee_name}")
                else:
                    logger.warning(f"  ❌ {committee_name}")
            
            logger.info(f"\nCommittee Coverage:")
            logger.info(f"House: {found_house}/{len(major_house_committees)} ({found_house/len(major_house_committees)*100:.1f}%)")
            logger.info(f"Senate: {found_senate}/{len(major_senate_committees)} ({found_senate/len(major_senate_committees)*100:.1f}%)")
            
    except Exception as e:
        logger.error(f"❌ Error checking committees: {e}")
        return False
    
    # Test 2: Validate member distribution
    logger.info("\n2. Testing member distribution...")
    
    try:
        response = requests.get(f"{BASE_URL}/members")
        if response.status_code == 200:
            all_members = response.json()
            
            # Analyze by chamber
            house_members = [m for m in all_members if m['chamber'] == 'House']
            senate_members = [m for m in all_members if m['chamber'] == 'Senate']
            
            logger.info(f"Chamber distribution:")
            logger.info(f"  House: {len(house_members)} members")
            logger.info(f"  Senate: {len(senate_members)} members")
            logger.info(f"  Total: {len(all_members)} members")
            
            # Analyze by party
            party_count = defaultdict(int)
            for member in all_members:
                party_count[member['party']] += 1
            
            logger.info(f"\nParty distribution:")
            for party, count in party_count.items():
                logger.info(f"  {party}: {count} members")
            
            # Check if we have reasonable distribution
            if len(house_members) > 400 and len(senate_members) > 90:
                logger.info("✅ Member distribution looks realistic")
            else:
                logger.warning("⚠️  Member distribution seems low")
            
    except Exception as e:
        logger.error(f"❌ Error checking members: {e}")
        return False
    
    # Test 3: Validate relationship quality
    logger.info("\n3. Testing relationship quality...")
    
    try:
        # Sample members with committees
        test_members = [19, 24, 62, 63, 73]  # Known members with committees
        
        total_relationships = 0
        members_with_committees = 0
        
        for member_id in test_members:
            response = requests.get(f"{BASE_URL}/members/{member_id}/committees")
            if response.status_code == 200:
                committees = response.json()
                if committees:
                    members_with_committees += 1
                    total_relationships += len(committees)
        
        logger.info(f"Relationship quality:")
        logger.info(f"  Members with committees: {members_with_committees}/{len(test_members)}")
        logger.info(f"  Total relationships tested: {total_relationships}")
        logger.info(f"  Average committees per member: {total_relationships/len(test_members):.1f}")
        
        # Test committee member rosters
        major_committee_names = ["Committee on Appropriations", "Committee on Armed Services", "Committee on the Judiciary"]
        committees_with_members = 0
        
        for committee_name in major_committee_names:
            # Find the committee
            response = requests.get(f"{BASE_URL}/committees")
            if response.status_code == 200:
                committees = response.json()
                committee = next((c for c in committees if c['name'] == committee_name), None)
                if committee:
                    response = requests.get(f"{BASE_URL}/committees/{committee['id']}/members")
                    if response.status_code == 200:
                        members = response.json()
                        if members:
                            committees_with_members += 1
        
        logger.info(f"  Major committees with members: {committees_with_members}/{len(major_committee_names)}")
        
    except Exception as e:
        logger.error(f"❌ Error checking relationships: {e}")
        return False
    
    # Summary and success criteria
    logger.info("\n" + "="*60)
    logger.info("📊 CONGRESSIONAL STRUCTURE VALIDATION SUMMARY:")
    
    success_criteria = [
        found_house >= len(major_house_committees) * 0.8,  # 80% of House committees
        found_senate >= len(major_senate_committees) * 0.8,  # 80% of Senate committees
        len(all_members) >= 500,  # At least 500 members
        members_with_committees >= len(test_members) * 0.8,  # 80% of tested members have committees
        committees_with_members >= len(major_committee_names) * 0.8  # 80% of major committees have members
    ]
    
    passed_criteria = sum(success_criteria)
    
    logger.info(f"Success criteria met: {passed_criteria}/{len(success_criteria)}")
    
    if passed_criteria >= len(success_criteria) * 0.8:
        logger.info("🎉 CONGRESSIONAL STRUCTURE VALIDATION: SUCCESS!")
        logger.info("Database structure matches real congressional organization!")
        return True
    else:
        logger.error("❌ CONGRESSIONAL STRUCTURE VALIDATION: ISSUES FOUND")
        logger.error("Database structure needs improvement")
        return False

if __name__ == "__main__":
    validate_congressional_structure()