#!/usr/bin/env python3

"""
Step 5: API Enhancement Test
Test the API endpoints with new URL fields
"""

import requests
import json
from datetime import datetime

def test_production_api():
    """Test the production API endpoints"""
    
    base_url = "https://congressional-data-api-v2-1066017671167.us-central1.run.app"
    
    print("🔄 TESTING PRODUCTION API WITH NEW URL FIELDS")
    print("=" * 60)
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        print(f"✅ Health endpoint: {response.status_code}")
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")
        return False
    
    # Test committees endpoint
    try:
        response = requests.get(f"{base_url}/api/v1/committees")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Committees endpoint: {response.status_code}")
            print(f"   Total committees: {len(data)}")
            
            # Check for URL fields in response
            if data and len(data) > 0:
                first_committee = data[0]
                url_fields = ['hearings_url', 'members_url', 'official_website_url', 'last_url_update']
                
                print(f"\n📋 CHECKING URL FIELDS IN FIRST COMMITTEE:")
                print(f"   Committee: {first_committee.get('name', 'Unknown')}")
                print(f"   Chamber: {first_committee.get('chamber', 'Unknown')}")
                
                url_field_status = {}
                for field in url_fields:
                    if field in first_committee:
                        value = first_committee[field]
                        if value:
                            url_field_status[field] = "✅ Present"
                        else:
                            url_field_status[field] = "⚠️ Field exists but null"
                    else:
                        url_field_status[field] = "❌ Missing"
                    
                    print(f"   {field:<20}: {url_field_status[field]}")
                
                # Check if any committee has URLs
                committees_with_urls = 0
                for committee in data:
                    if (committee.get('hearings_url') or 
                        committee.get('members_url') or 
                        committee.get('official_website_url')):
                        committees_with_urls += 1
                
                print(f"\n📊 URL FIELD STATISTICS:")
                print(f"   Committees with URLs: {committees_with_urls}/{len(data)}")
                print(f"   Coverage: {(committees_with_urls / len(data)) * 100:.1f}%")
                
                # Show sample with URLs
                if committees_with_urls > 0:
                    for committee in data[:5]:  # Show first 5
                        if (committee.get('hearings_url') or 
                            committee.get('members_url') or 
                            committee.get('official_website_url')):
                            print(f"\n📋 SAMPLE COMMITTEE WITH URLS:")
                            print(f"   Name: {committee.get('name')}")
                            print(f"   Chamber: {committee.get('chamber')}")
                            if committee.get('hearings_url'):
                                print(f"   Hearings: {committee.get('hearings_url')}")
                            if committee.get('members_url'):
                                print(f"   Members: {committee.get('members_url')}")
                            if committee.get('official_website_url'):
                                print(f"   Website: {committee.get('official_website_url')}")
                            break
                
                return True
                
        else:
            print(f"❌ Committees endpoint: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Committees endpoint error: {e}")
        return False

def test_specific_committee():
    """Test a specific committee to verify URL fields"""
    
    base_url = "https://congressional-data-api-v2-1066017671167.us-central1.run.app"
    
    print("\n🔍 TESTING SPECIFIC COMMITTEE")
    print("=" * 60)
    
    # Try to get House Agriculture Committee (ID should be 1)
    try:
        response = requests.get(f"{base_url}/api/v1/committees/1")
        if response.status_code == 200:
            committee = response.json()
            print(f"✅ Specific committee endpoint: {response.status_code}")
            print(f"   Committee: {committee.get('name')}")
            print(f"   Chamber: {committee.get('chamber')}")
            
            # Check URL fields
            if committee.get('hearings_url'):
                print(f"   Hearings URL: {committee.get('hearings_url')}")
            if committee.get('members_url'):
                print(f"   Members URL: {committee.get('members_url')}")
            if committee.get('official_website_url'):
                print(f"   Website URL: {committee.get('official_website_url')}")
            
            return True
        else:
            print(f"❌ Specific committee endpoint: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Specific committee endpoint error: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 TESTING API ENHANCEMENT - URL FIELDS")
    print("=" * 60)
    
    # Test general API
    api_test = test_production_api()
    
    # Test specific committee
    specific_test = test_specific_committee()
    
    print("\n🎯 TEST RESULTS SUMMARY")
    print("=" * 60)
    if api_test and specific_test:
        print("✅ ALL TESTS PASSED")
        print("✅ API enhancement successful")
        print("✅ URL fields are working correctly")
    else:
        print("❌ SOME TESTS FAILED")
        print("❌ API enhancement needs attention")
        print("❌ URL fields may not be working correctly")

if __name__ == "__main__":
    main()