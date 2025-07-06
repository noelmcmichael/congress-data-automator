#!/usr/bin/env python3
"""
Test API routing to identify where the members endpoint is being handled
"""
import requests
import json

BASE_URL = "https://congressional-data-api-v2-1066017671167.us-central1.run.app"

def test_routing():
    """Test different endpoints to identify routing issues"""
    
    # Test various endpoints
    endpoints = [
        "/",
        "/health",
        "/api/v1/status",
        "/api/v1/debug-test",
        "/api/v1/members",
        "/docs",
        "/openapi.json"
    ]
    
    for endpoint in endpoints:
        print(f"\n=== Testing {endpoint} ===")
        url = f"{BASE_URL}{endpoint}"
        
        try:
            response = requests.get(url, timeout=10)
            print(f"Status: {response.status_code}")
            print(f"Headers: {dict(response.headers)}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"Response: {json.dumps(data, indent=2)}")
                except:
                    print(f"Text response: {response.text[:200]}...")
            else:
                print(f"Error: {response.text}")
        except Exception as e:
            print(f"Error: {e}")
    
    # Test specific members endpoint variations
    print(f"\n=== Testing Members Endpoint Variations ===")
    member_endpoints = [
        "/api/v1/members",
        "/api/v1/members/",
        "/api/v1/members?limit=5",
        "/api/v1/members?party=Republican&limit=3"
    ]
    
    for endpoint in member_endpoints:
        print(f"\n--- Testing {endpoint} ---")
        url = f"{BASE_URL}{endpoint}"
        
        try:
            response = requests.get(url, timeout=10)
            print(f"Status: {response.status_code}")
            print(f"URL: {response.url}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Result count: {len(data)}")
                if data:
                    print(f"First item keys: {list(data[0].keys())}")
                    if 'first_name' in data[0]:
                        print(f"First member: {data[0].get('first_name', '')} {data[0].get('last_name', '')}")
            else:
                print(f"Error: {response.text}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_routing()