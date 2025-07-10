#!/usr/bin/env python3
"""
Test production chamber data to understand the 500 error
"""

import requests
import json
import time

def test_production_endpoints():
    """Test production API endpoints to understand chamber filtering"""
    
    base_url = "https://congressional-data-api-v3-1066017671167.us-central1.run.app/api/v1"
    
    endpoints_to_test = [
        # Working endpoints
        ("committees", {"limit": 5}),
        ("committees", {"chamber": "Senate", "limit": 5}),
        ("committees", {"chamber": "Joint", "limit": 5}),
        
        # Case sensitivity tests
        ("committees", {"chamber": "house", "limit": 5}),
        ("committees", {"chamber": "HOUSE", "limit": 5}),
        ("committees", {"chamber": "House", "limit": 5}),  # This should fail
        
        # Alternative API endpoints
        ("committees", {"chamber": "senate", "limit": 5}),
        ("committees", {"chamber": "SENATE", "limit": 5}),
        ("committees", {"chamber": "Senate", "limit": 5}),
        
        # Test joint variations
        ("committees", {"chamber": "joint", "limit": 5}),
        ("committees", {"chamber": "JOINT", "limit": 5}),
        ("committees", {"chamber": "Joint", "limit": 5}),
    ]
    
    print("🧪 Testing Production Chamber Filtering")
    print("=" * 50)
    
    for endpoint, params in endpoints_to_test:
        url = f"{base_url}/{endpoint}"
        
        try:
            start_time = time.time()
            response = requests.get(url, params=params, timeout=10)
            response_time = time.time() - start_time
            
            status_icon = "✅" if response.status_code == 200 else "❌"
            
            print(f"\n{status_icon} {endpoint}?{params}")
            print(f"   Status: {response.status_code}")
            print(f"   Time: {response_time:.3f}s")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"   Count: {len(data)} items")
                    if data:
                        # Show first committee
                        first_committee = data[0]
                        print(f"   Sample: {first_committee.get('name', 'N/A')} ({first_committee.get('chamber', 'N/A')})")
                    else:
                        print("   Sample: No data returned")
                except json.JSONDecodeError:
                    print("   Error: Invalid JSON")
            else:
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data.get('detail', 'Unknown error')}")
                except:
                    print(f"   Error: {response.text[:100]}...")
                    
        except requests.exceptions.RequestException as e:
            print(f"❌ {endpoint}?{params}")
            print(f"   Network Error: {e}")
    
    print("\n" + "=" * 50)
    print("🔍 Summary Analysis")
    print("=" * 50)
    
    # Test members endpoint for comparison
    print("\n📊 Testing Members Endpoint (for comparison):")
    members_url = f"{base_url}/members"
    
    try:
        response = requests.get(members_url, params={"chamber": "House", "limit": 3}, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Members endpoint with chamber=House: {len(data)} items")
            if data:
                print(f"   Sample: {data[0].get('first_name', 'N/A')} {data[0].get('last_name', 'N/A')} ({data[0].get('chamber', 'N/A')})")
        else:
            print(f"❌ Members endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Members endpoint error: {e}")
    
    # Test without chamber filter
    print("\n📊 Testing Committees Without Filter:")
    try:
        response = requests.get(f"{base_url}/committees", params={"limit": 10}, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Committees without filter: {len(data)} items")
            
            # Analyze chamber distribution
            chamber_counts = {}
            for committee in data:
                chamber = committee.get('chamber', 'Unknown')
                chamber_counts[chamber] = chamber_counts.get(chamber, 0) + 1
            
            print("   Chamber distribution:")
            for chamber, count in chamber_counts.items():
                print(f"     {chamber}: {count} committees")
        else:
            print(f"❌ Committees without filter failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Committees without filter error: {e}")

if __name__ == "__main__":
    test_production_endpoints()