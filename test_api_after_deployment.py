#!/usr/bin/env python3
"""Test API functionality after deployment."""

import requests
import json

def test_api_after_deployment():
    """Test the API endpoints after deployment."""
    
    base_url = "https://congressional-data-api-v2-1066017671167.us-central1.run.app"
    
    print("🔍 Testing API after deployment...")
    
    # Test 1: Health check
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        print(f"✅ Health check: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False
    
    # Test 2: Hearings endpoint
    try:
        response = requests.get(f"{base_url}/api/v1/hearings", timeout=10)
        print(f"✅ Hearings endpoint: {response.status_code}")
        if response.status_code == 200:
            hearings = response.json()
            print(f"   Total hearings: {len(hearings)}")
            
            # Check for hearings with committees
            hearings_with_committees = [h for h in hearings if h.get('committee_id')]
            print(f"   Hearings with committees: {len(hearings_with_committees)}")
            
            if hearings_with_committees:
                print("   Sample hearing with committee:")
                sample = hearings_with_committees[0]
                print(f"   - ID: {sample.get('id')}")
                print(f"   - Title: {sample.get('title', 'N/A')[:50]}...")
                print(f"   - Committee ID: {sample.get('committee_id')}")
                
    except Exception as e:
        print(f"❌ Hearings endpoint failed: {e}")
        return False
    
    # Test 3: Hearings with committee filter
    try:
        response = requests.get(f"{base_url}/api/v1/hearings?committee_id=134", timeout=10)
        print(f"✅ Hearings with committee filter: {response.status_code}")
        if response.status_code == 200:
            filtered_hearings = response.json()
            print(f"   Armed Services Committee hearings: {len(filtered_hearings)}")
    except Exception as e:
        print(f"❌ Committee filter test failed: {e}")
        return False
    
    # Test 4: Specific hearing
    try:
        response = requests.get(f"{base_url}/api/v1/hearings/120", timeout=10)
        print(f"✅ Specific hearing: {response.status_code}")
        if response.status_code == 200:
            hearing = response.json()
            print(f"   Hearing 120 committee_id: {hearing.get('committee_id')}")
    except Exception as e:
        print(f"❌ Specific hearing test failed: {e}")
        return False
    
    print("\n🎉 All API tests completed successfully!")
    return True

if __name__ == "__main__":
    test_api_after_deployment()