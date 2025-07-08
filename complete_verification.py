#!/usr/bin/env python3
"""Complete verification of deployment."""

import requests
import json

def complete_verification():
    """Complete verification of the deployment."""
    
    print("🔍 Complete Deployment Verification")
    print("=" * 50)
    
    base_url = "https://congressional-data-api-v2-1066017671167.us-central1.run.app"
    
    # Test 1: Get all hearings (with large limit to get real count)
    print("\n1. Testing hearings coverage...")
    response = requests.get(f"{base_url}/api/v1/hearings?limit=500")
    if response.status_code == 200:
        hearings = response.json()
        total_hearings = len(hearings)
        hearings_with_committees = [h for h in hearings if h.get('committee_id')]
        coverage = (len(hearings_with_committees) / total_hearings) * 100 if total_hearings > 0 else 0
        
        print(f"   Total hearings: {total_hearings}")
        print(f"   Hearings with committees: {len(hearings_with_committees)}")
        print(f"   Coverage: {coverage:.1f}%")
        
        # Show sample committee assignments
        print("\n   Sample committee assignments:")
        for i, h in enumerate(hearings_with_committees[:5]):
            print(f"   - Hearing {h['id']}: Committee {h['committee_id']}")
    
    # Test 2: Committee filtering
    print("\n2. Testing committee filtering...")
    response = requests.get(f"{base_url}/api/v1/hearings?committee_id=134")
    if response.status_code == 200:
        armed_services = response.json()
        print(f"   Armed Services hearings: {len(armed_services)}")
    
    # Test 3: Specific hearing validation
    print("\n3. Testing specific hearing assignments...")
    test_hearings = [120, 121, 122, 123, 124]  # First 5 from our updates
    for hearing_id in test_hearings:
        response = requests.get(f"{base_url}/api/v1/hearings/{hearing_id}")
        if response.status_code == 200:
            hearing = response.json()
            committee_id = hearing.get('committee_id')
            title = hearing.get('title', 'N/A')[:40]
            print(f"   Hearing {hearing_id}: Committee {committee_id} - {title}...")
    
    # Test 4: API health and performance
    print("\n4. Testing API health...")
    response = requests.get(f"{base_url}/health")
    if response.status_code == 200:
        health = response.json()
        print(f"   API Status: {health.get('status')}")
        print(f"   Timestamp: {health.get('timestamp')}")
    
    print("\n🎉 Verification Complete!")

if __name__ == "__main__":
    complete_verification()