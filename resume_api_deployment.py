#!/usr/bin/env python3

"""
Resume API Deployment - Simplified approach to get URL fields working
"""

import requests
import json
import subprocess
import time

def test_current_api():
    """Test the current API to see what's working"""
    print("🔍 TESTING CURRENT API STATUS")
    print("=" * 50)
    
    api_url = "https://congressional-data-api-v2-1066017671167.us-central1.run.app"
    
    try:
        # Test health endpoint
        health_response = requests.get(f"{api_url}/health", timeout=10)
        print(f"✅ Health check: {health_response.status_code}")
        
        # Test committee endpoint
        committee_response = requests.get(f"{api_url}/api/v1/committees/1", timeout=10)
        print(f"✅ Committee endpoint: {committee_response.status_code}")
        
        if committee_response.status_code == 200:
            data = committee_response.json()
            print(f"Committee name: {data.get('name', 'N/A')}")
            print(f"Hearings URL: {data.get('hearings_url', 'NULL')}")
            print(f"Members URL: {data.get('members_url', 'NULL')}")
            print(f"Official URL: {data.get('official_website_url', 'NULL')}")
            
            # Check if URL fields exist in response
            has_url_fields = any(key in data for key in ['hearings_url', 'members_url', 'official_website_url'])
            print(f"Has URL fields: {'✅' if has_url_fields else '❌'}")
            
            return has_url_fields
        else:
            print(f"❌ Committee endpoint failed: {committee_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

def check_database_directly():
    """Check if database has URL data by testing a simple query"""
    print("\n🔍 CHECKING DATABASE VIA API")
    print("=" * 50)
    
    api_url = "https://congressional-data-api-v2-1066017671167.us-central1.run.app"
    
    try:
        # Get all committees and check if any have URL data
        committees_response = requests.get(f"{api_url}/api/v1/committees", timeout=10)
        
        if committees_response.status_code == 200:
            committees = committees_response.json()
            print(f"Total committees: {len(committees)}")
            
            # Check first few committees for URL fields
            url_count = 0
            for committee in committees[:5]:
                if committee.get('hearings_url') or committee.get('members_url') or committee.get('official_website_url'):
                    url_count += 1
                    print(f"✅ {committee.get('name', 'N/A')} has URL data")
                else:
                    print(f"❌ {committee.get('name', 'N/A')} missing URL data")
            
            print(f"Committees with URL data: {url_count}/5")
            return url_count > 0
        else:
            print(f"❌ Failed to get committees: {committees_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Database check failed: {e}")
        return False

def simple_fix_approach():
    """Simple approach to fix URL fields"""
    print("\n🔧 SIMPLE FIX APPROACH")
    print("=" * 50)
    
    # Instead of complex deployment, let's check what we actually need
    api_url = "https://congressional-data-api-v2-1066017671167.us-central1.run.app"
    
    try:
        # Test committee endpoint schema
        response = requests.get(f"{api_url}/api/v1/committees/1", timeout=10)
        if response.status_code == 200:
            data = response.json()
            fields = list(data.keys())
            print(f"Current API response fields: {fields}")
            
            # Check what fields are missing
            required_fields = ['hearings_url', 'members_url', 'official_website_url', 'last_url_update']
            missing_fields = [field for field in required_fields if field not in fields]
            
            if missing_fields:
                print(f"❌ Missing fields: {missing_fields}")
                print("The API schema doesn't include URL fields yet")
                return False
            else:
                print("✅ All URL fields are present in API schema")
                print("The issue is that the database values are NULL")
                return True
                
    except Exception as e:
        print(f"❌ Schema check failed: {e}")
        return False

def main():
    """Main function to resume API deployment"""
    print("🚀 RESUMING API DEPLOYMENT - SIMPLIFIED APPROACH")
    print("=" * 60)
    
    # Step 1: Test current API
    api_working = test_current_api()
    
    # Step 2: Check database via API
    db_has_data = check_database_directly()
    
    # Step 3: Simple fix approach
    schema_ready = simple_fix_approach()
    
    print("\n📊 DIAGNOSTIC SUMMARY")
    print("=" * 60)
    print(f"API Working: {'✅' if api_working else '❌'}")
    print(f"Database Has Data: {'✅' if db_has_data else '❌'}")
    print(f"Schema Ready: {'✅' if schema_ready else '❌'}")
    
    if api_working and not db_has_data and not schema_ready:
        print("\n💡 RECOMMENDATION: API is working but URL fields are missing from schema")
        print("This suggests the deployed API doesn't have the URL field enhancement yet")
        print("Need to deploy the updated API with URL field support")
        return "schema_update_needed"
    elif api_working and schema_ready and not db_has_data:
        print("\n💡 RECOMMENDATION: API has URL fields but database values are NULL")
        print("Need to populate database with URL data")
        return "database_population_needed"
    elif api_working and db_has_data and schema_ready:
        print("\n🎉 SUCCESS: Everything is working!")
        print("Phase 2C: API Enhancement - COMPLETE")
        return "complete"
    else:
        print("\n🔍 RECOMMENDATION: Need further investigation")
        return "investigation_needed"

if __name__ == "__main__":
    result = main()
    print(f"\nResult: {result}")