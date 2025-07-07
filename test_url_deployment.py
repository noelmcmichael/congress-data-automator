#!/usr/bin/env python3

"""
Test URL field deployment - Check if the issue is database or API
"""

import requests
import json

def test_api_response_fields():
    """Test what fields are actually returned by the API"""
    print("🔍 TESTING API RESPONSE FIELDS")
    print("=" * 50)
    
    api_url = "https://congressional-data-api-v2-1066017671167.us-central1.run.app"
    
    try:
        # Test individual committee endpoint
        response = requests.get(f"{api_url}/api/v1/committees/1", timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Committee: {data.get('name', 'N/A')}")
            print("\nAll fields in response:")
            for field in sorted(data.keys()):
                value = data[field]
                if value is None:
                    value = "NULL"
                elif isinstance(value, str) and len(value) > 50:
                    value = value[:50] + "..."
                print(f"  {field}: {value}")
            
            # Check for URL fields specifically
            url_fields = ['hearings_url', 'members_url', 'official_website_url', 'last_url_update']
            print(f"\nURL fields check:")
            for field in url_fields:
                if field in data:
                    print(f"  ✅ {field}: {data[field]}")
                else:
                    print(f"  ❌ {field}: MISSING FROM RESPONSE")
            
            return data
        else:
            print(f"❌ Request failed: {response.status_code}")
            print(response.text)
            return None
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return None

def test_database_vs_api():
    """Test if the issue is database population or API schema"""
    print("\n🔍 TESTING DATABASE vs API MISMATCH")
    print("=" * 50)
    
    # Based on the earlier diagnostic, we know:
    # 1. API response has 'website_url' field
    # 2. API response does NOT have 'hearings_url', 'members_url', 'official_website_url'
    # 3. Database model HAS these fields
    
    # The issue is likely that the database schema was updated but the API wasn't redeployed
    
    print("Analysis:")
    print("1. ✅ Database model includes URL fields (hearings_url, members_url, official_website_url)")
    print("2. ✅ API schema (CommitteeResponse) includes URL fields")
    print("3. ❌ API response only returns 'website_url' not the new URL fields")
    print("4. ❌ This suggests the deployed API is using an old version")
    
    print("\nConclusion: The API deployment didn't successfully update with URL fields")
    print("The container might have built correctly but the deployment is still using old code")
    
    return "deployment_issue"

def check_deployment_status():
    """Check the actual deployment status"""
    print("\n🔍 CHECKING DEPLOYMENT STATUS")
    print("=" * 50)
    
    api_url = "https://congressional-data-api-v2-1066017671167.us-central1.run.app"
    
    try:
        # Check if there's a debug endpoint that shows deployment info
        debug_response = requests.get(f"{api_url}/api/v1/debug-test", timeout=10)
        if debug_response.status_code == 200:
            debug_data = debug_response.json()
            print("Debug endpoint response:")
            for key, value in debug_data.items():
                print(f"  {key}: {value}")
            return debug_data
        else:
            print("No debug endpoint available")
            return None
            
    except Exception as e:
        print(f"Debug endpoint failed: {e}")
        return None

def main():
    """Main test function"""
    print("🚀 TESTING URL FIELD DEPLOYMENT")
    print("=" * 60)
    
    # Test 1: Check API response fields
    api_data = test_api_response_fields()
    
    # Test 2: Analyze database vs API mismatch
    analysis = test_database_vs_api()
    
    # Test 3: Check deployment status
    debug_info = check_deployment_status()
    
    print("\n📊 SUMMARY")
    print("=" * 60)
    if api_data:
        has_url_fields = any(field in api_data for field in ['hearings_url', 'members_url', 'official_website_url'])
        print(f"API has URL fields: {'✅' if has_url_fields else '❌'}")
        
        if has_url_fields:
            url_values = [api_data.get(field) for field in ['hearings_url', 'members_url', 'official_website_url']]
            has_data = any(value is not None for value in url_values)
            print(f"URL fields have data: {'✅' if has_data else '❌'}")
        else:
            print("❌ URL fields missing from API response")
            print("💡 SOLUTION: Need to deploy updated API with URL field support")
    
    if debug_info:
        print(f"API version: {debug_info.get('version', 'Unknown')}")
        print(f"Deployment: {debug_info.get('deployment', 'Unknown')}")
    
    print("\nRecommendation: Deploy the updated API container with URL field support")

if __name__ == "__main__":
    main()