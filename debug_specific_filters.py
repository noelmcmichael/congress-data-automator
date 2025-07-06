#!/usr/bin/env python3
"""
Debug specific filter issues - Check what's happening with party/chamber filters
"""

import requests
import json
from typing import Dict, Any

API_BASE = "https://congressional-data-api-v2-1066017671167.us-central1.run.app"

def test_debug_endpoint(party: str = None) -> Dict[str, Any]:
    """Test the debug raw SQL endpoint"""
    endpoint = "/api/v1/debug-raw-sql"
    if party:
        endpoint += f"?party={party}"
    
    print(f"\n🔍 Testing debug endpoint: {endpoint}")
    
    try:
        response = requests.get(f"{API_BASE}{endpoint}", timeout=10)
        response.raise_for_status()
        
        data = response.json()
        print(f"✅ Status: {response.status_code}")
        print(f"✅ Response: {json.dumps(data, indent=2)}")
        
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")
        return {}

def test_members_endpoint(params: str = "") -> Dict[str, Any]:
    """Test the members endpoint with specific params"""
    endpoint = f"/api/v1/members{params}"
    
    print(f"\n🔍 Testing members endpoint: {endpoint}")
    
    try:
        response = requests.get(f"{API_BASE}{endpoint}", timeout=10)
        response.raise_for_status()
        
        data = response.json()
        total_results = len(data) if isinstance(data, list) else 0
        
        print(f"✅ Status: {response.status_code}")
        print(f"✅ Results: {total_results}")
        
        if isinstance(data, list) and len(data) > 0:
            # Show first few results
            for i, member in enumerate(data[:3]):
                print(f"   {i+1}. {member.get('first_name', '')} {member.get('last_name', '')} ({member.get('party', '')}) - {member.get('state', '')} - {member.get('chamber', '')}")
        
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")
        return []

def main():
    print("🔍 Debug Specific Filter Issues")
    print("=" * 50)
    
    # Test 1: Check raw SQL debug endpoint
    print("\n📋 STEP 1: Test Raw SQL Debug Endpoint")
    
    # Test without filter
    debug_all = test_debug_endpoint()
    
    # Test with Republican filter
    debug_republican = test_debug_endpoint("Republican")
    
    # Test with Democratic filter
    debug_democratic = test_debug_endpoint("Democratic")
    
    # Test 2: Check what the actual data looks like
    print("\n📋 STEP 2: Check Actual Member Data")
    
    # Get first page of members
    members_data = test_members_endpoint()
    
    if isinstance(members_data, list) and len(members_data) > 0:
        print("\n📊 Data Analysis:")
        
        # Analyze party distribution
        parties = {}
        chambers = {}
        states = {}
        
        for member in members_data:
            party = member.get('party', 'Unknown')
            chamber = member.get('chamber', 'Unknown')
            state = member.get('state', 'Unknown')
            
            parties[party] = parties.get(party, 0) + 1
            chambers[chamber] = chambers.get(chamber, 0) + 1
            states[state] = states.get(state, 0) + 1
        
        print(f"Party distribution: {parties}")
        print(f"Chamber distribution: {chambers}")
        print(f"State distribution (top 5): {dict(sorted(states.items(), key=lambda x: x[1], reverse=True)[:5])}")
        
        # Check for case sensitivity issues
        print(f"\nCase sensitivity check:")
        print(f"Parties found: {list(parties.keys())}")
        print(f"Chambers found: {list(chambers.keys())}")
    
    # Test 3: Test specific filter combinations
    print("\n📋 STEP 3: Test Filter Combinations")
    
    # Test party filters with different cases
    test_cases = [
        "?party=Republican",
        "?party=Democratic", 
        "?party=republican",
        "?party=democratic",
        "?chamber=House",
        "?chamber=Senate",
        "?chamber=house",
        "?chamber=senate",
        "?state=CA",
        "?state=ca",
        "?state=TX",
        "?state=NY"
    ]
    
    for test_case in test_cases:
        data = test_members_endpoint(test_case)
        print(f"   {test_case}: {len(data)} results")

if __name__ == "__main__":
    main()