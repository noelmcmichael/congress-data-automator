#!/usr/bin/env python3
"""
Test frontend integration by verifying the API endpoints that the frontend uses.
"""

import requests
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "https://congressional-data-api-v2-1066017671167.us-central1.run.app/api/v1"
FRONTEND_URL = "https://storage.googleapis.com/congressional-data-frontend/index.html"

def test_frontend_integration():
    """Test the frontend integration with the API."""
    
    logger.info("🌐 TESTING FRONTEND INTEGRATION")
    logger.info("="*60)
    
    # Test 1: Basic API endpoints that frontend uses
    logger.info("Testing basic API endpoints...")
    
    endpoints = [
        "/members",
        "/committees", 
        "/hearings",
        "/health"
    ]
    
    working_endpoints = 0
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}")
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    logger.info(f"✅ {endpoint}: {len(data)} items")
                elif isinstance(data, dict):
                    logger.info(f"✅ {endpoint}: {data}")
                else:
                    logger.info(f"✅ {endpoint}: OK")
                working_endpoints += 1
            else:
                logger.error(f"❌ {endpoint}: HTTP {response.status_code}")
        except Exception as e:
            logger.error(f"❌ {endpoint}: {e}")
    
    logger.info(f"Working endpoints: {working_endpoints}/{len(endpoints)}")
    
    # Test 2: Test frontend accessibility
    logger.info("\nTesting frontend accessibility...")
    try:
        response = requests.get(FRONTEND_URL)
        if response.status_code == 200:
            logger.info("✅ Frontend accessible")
            
            # Check for React app indicators
            content = response.text
            if "React App" in content and "root" in content:
                logger.info("✅ Frontend is React app")
            else:
                logger.warning("⚠️ Frontend content unexpected")
        else:
            logger.error(f"❌ Frontend not accessible: HTTP {response.status_code}")
    except Exception as e:
        logger.error(f"❌ Frontend error: {e}")
    
    # Test 3: Test specific relationship endpoints for frontend
    logger.info("\nTesting relationship endpoints for frontend...")
    
    # Get a sample member with committees
    test_member_id = 19  # We know this member has committees
    
    try:
        # Member details
        response = requests.get(f"{BASE_URL}/members/{test_member_id}")
        if response.status_code == 200:
            member_data = response.json()
            logger.info(f"✅ Member details: {member_data['first_name']} {member_data['last_name']}")
            
            # Member committees
            response = requests.get(f"{BASE_URL}/members/{test_member_id}/committees")
            if response.status_code == 200:
                committees = response.json()
                logger.info(f"✅ Member committees: {len(committees)} committees")
                
                # Test committee details
                if committees:
                    committee_id = committees[0]['committee']['id']
                    response = requests.get(f"{BASE_URL}/committees/{committee_id}")
                    if response.status_code == 200:
                        committee_data = response.json()
                        logger.info(f"✅ Committee details: {committee_data['name']}")
                        
                        # Test committee members
                        response = requests.get(f"{BASE_URL}/committees/{committee_id}/members")
                        if response.status_code == 200:
                            members = response.json()
                            logger.info(f"✅ Committee members: {len(members)} members")
                        else:
                            logger.error(f"❌ Committee members endpoint failed")
                    else:
                        logger.error(f"❌ Committee details endpoint failed")
            else:
                logger.error(f"❌ Member committees endpoint failed")
        else:
            logger.error(f"❌ Member details endpoint failed")
    except Exception as e:
        logger.error(f"❌ Relationship testing error: {e}")
    
    # Test 4: Test search functionality
    logger.info("\nTesting search functionality...")
    
    search_tests = [
        "/members?search=John",
        "/committees?search=Judiciary",
        "/members?party=Republican",
        "/members?chamber=House"
    ]
    
    working_search = 0
    
    for search_url in search_tests:
        try:
            response = requests.get(f"{BASE_URL}{search_url}")
            if response.status_code == 200:
                data = response.json()
                logger.info(f"✅ Search {search_url}: {len(data)} results")
                working_search += 1
            else:
                logger.error(f"❌ Search {search_url}: HTTP {response.status_code}")
        except Exception as e:
            logger.error(f"❌ Search {search_url}: {e}")
    
    logger.info(f"Working search endpoints: {working_search}/{len(search_tests)}")
    
    # Summary
    logger.info("\n" + "="*60)
    logger.info("📊 FRONTEND INTEGRATION TEST SUMMARY:")
    logger.info(f"Basic endpoints: {working_endpoints}/{len(endpoints)}")
    logger.info(f"Search endpoints: {working_search}/{len(search_tests)}")
    logger.info(f"Frontend URL: {FRONTEND_URL}")
    logger.info(f"API URL: {BASE_URL}")
    
    # Overall success
    if working_endpoints >= len(endpoints) * 0.8 and working_search >= len(search_tests) * 0.8:
        logger.info("\n🎉 FRONTEND INTEGRATION TEST: SUCCESS!")
        logger.info("Frontend should be able to display all relationship data correctly!")
        return True
    else:
        logger.error("\n❌ FRONTEND INTEGRATION TEST: ISSUES FOUND")
        return False

if __name__ == "__main__":
    test_frontend_integration()