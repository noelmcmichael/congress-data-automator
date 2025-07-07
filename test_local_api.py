#!/usr/bin/env python3

"""
Test Local API with URL Fields
Test the API locally to see if URL fields work
"""

import sys
import os
sys.path.append('/Users/noelmcmichael/Workspace/congress_data_automator/backend')

import uvicorn
from fastapi.testclient import TestClient
from app.main import app

def test_local_api():
    """Test the API locally"""
    
    print("🔄 TESTING LOCAL API WITH URL FIELDS")
    print("=" * 60)
    
    client = TestClient(app)
    
    # Test health endpoint
    response = client.get("/health")
    print(f"Health endpoint: {response.status_code}")
    
    # Test committees endpoint
    response = client.get("/api/v1/committees")
    if response.status_code == 200:
        data = response.json()
        print(f"Committees endpoint: {response.status_code}")
        print(f"Total committees: {len(data)}")
        
        if data and len(data) > 0:
            first_committee = data[0]
            print(f"\nFirst committee: {first_committee.get('name')}")
            print(f"Fields available: {list(first_committee.keys())}")
            
            # Check for URL fields
            url_fields = ['hearings_url', 'members_url', 'official_website_url', 'last_url_update']
            for field in url_fields:
                if field in first_committee:
                    value = first_committee[field]
                    print(f"  {field}: {value}")
                else:
                    print(f"  {field}: ❌ MISSING")
    else:
        print(f"Committees endpoint failed: {response.status_code}")
        print(f"Error: {response.text}")

if __name__ == "__main__":
    test_local_api()