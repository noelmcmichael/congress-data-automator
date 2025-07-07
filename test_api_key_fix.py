#!/usr/bin/env python3
"""
Test script to verify the API key fix works locally and then deploy.
"""

import os
import sys
import requests
import json

def test_api_key_locally():
    """Test the API key locally to make sure it works."""
    print("🔍 Testing Congress.gov API key locally...")
    
    api_key = "NcMVmULsduvTXfEIXhKgAb1uWDDFdzOcPI57jpRG"
    
    # Test the API directly
    url = "https://api.congress.gov/v3/member"
    headers = {
        "X-API-Key": api_key
    }
    params = {
        "limit": 10,
        "chamber": "house",
        "currentMember": "true"
    }
    
    try:
        print(f"Testing API call: {url}")
        response = requests.get(url, headers=headers, params=params, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            member_count = len(data.get("members", []))
            print(f"✅ API key works! Retrieved {member_count} members")
            print(f"✅ Rate limit info: {response.headers.get('x-ratelimit-remaining', 'Unknown')}")
            return True
        else:
            print(f"❌ API key test failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ API key test error: {e}")
        return False

def test_existing_service():
    """Test the existing service to see current state."""
    print("\n🔍 Testing existing service state...")
    
    # Test the current service
    base_url = "https://congressional-data-api-v2-1066017671167.us-central1.run.app"
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health", timeout=30)
        if response.status_code == 200:
            print("✅ Health endpoint working")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")
    
    # Test status endpoint
    try:
        response = requests.get(f"{base_url}/api/v1/status", timeout=30)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status endpoint working: {data.get('api_status', 'Unknown')}")
        else:
            print(f"❌ Status endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Status endpoint error: {e}")
    
    # Test Congress API
    try:
        response = requests.get(f"{base_url}/api/v1/test/congress-api", timeout=60)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Congress API test working: {data.get('api_connection', 'Unknown')}")
            return True
        else:
            print(f"❌ Congress API test failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Congress API test error: {e}")
        return False

def update_existing_service():
    """Update the existing service instead of creating a new one."""
    print("\n🔧 Updating existing service with API key...")
    
    import subprocess
    
    # Use the existing working service and just update the environment
    cmd = f"""gcloud run services update congressional-data-api-v2 \\
        --region=us-central1 \\
        --project=chefgavin \\
        --update-env-vars CONGRESS_API_KEY="NcMVmULsduvTXfEIXhKgAb1uWDDFdzOcPI57jpRG" \\
        --quiet"""
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Service updated successfully")
            return True
        else:
            print(f"❌ Service update failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Service update error: {e}")
        return False

def main():
    """Main function."""
    print("🚀 Congressional Data API - API Key Fix Test")
    print("=" * 50)
    
    # Step 1: Test API key locally
    if not test_api_key_locally():
        print("❌ Local API key test failed - stopping")
        return False
    
    # Step 2: Test existing service
    current_working = test_existing_service()
    
    # Step 3: Update existing service if needed
    if not current_working:
        print("\n🔧 Current service has API issues - updating...")
        if update_existing_service():
            print("✅ Service updated - waiting for deployment...")
            import time
            time.sleep(30)
            
            # Test again
            if test_existing_service():
                print("🎉 API key fix successful!")
                return True
            else:
                print("❌ API key fix failed")
                return False
        else:
            print("❌ Failed to update service")
            return False
    else:
        print("✅ Service already working correctly!")
        return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)