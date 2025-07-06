#!/usr/bin/env python3
"""
Test script to verify the current production API fix status
"""

import requests
import json
from typing import Dict, Any

API_BASE = "https://congressional-data-api-v2-1066017671167.us-central1.run.app"

def test_endpoint(endpoint: str, description: str) -> Dict[str, Any]:
    """Test a single endpoint and return results"""
    print(f"\n🔍 Testing: {description}")
    print(f"URL: {API_BASE}{endpoint}")
    
    try:
        response = requests.get(f"{API_BASE}{endpoint}", timeout=10)
        response.raise_for_status()
        
        data = response.json()
        total_results = len(data) if isinstance(data, list) else data.get('total', 0)
        
        print(f"✅ Status: {response.status_code}")
        print(f"✅ Results: {total_results}")
        
        if isinstance(data, list) and len(data) > 0:
            first_item = data[0]
            if 'party' in first_item:
                print(f"✅ First result party: {first_item.get('party', 'N/A')}")
            if 'state' in first_item:
                print(f"✅ First result state: {first_item.get('state', 'N/A')}")
            if 'chamber' in first_item:
                print(f"✅ First result chamber: {first_item.get('chamber', 'N/A')}")
        
        return {
            'success': True,
            'status_code': response.status_code,
            'total_results': total_results,
            'data': data
        }
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")
        return {
            'success': False,
            'error': str(e),
            'total_results': 0
        }

def analyze_filter_results(base_results: int, filtered_results: int, filter_name: str, filter_value: str) -> bool:
    """Analyze if filter results make sense"""
    print(f"\n📊 Filter Analysis: {filter_name}={filter_value}")
    print(f"Base results: {base_results}")
    print(f"Filtered results: {filtered_results}")
    
    if filtered_results == base_results:
        print("❌ FILTER NOT WORKING - Same number of results")
        return False
    elif filtered_results == 0:
        print("⚠️ FILTER MAY BE TOO RESTRICTIVE - No results")
        return False
    elif filtered_results < base_results:
        print("✅ FILTER WORKING - Reduced results as expected")
        return True
    else:
        print("❌ FILTER ERROR - More results than base")
        return False

def main():
    print("🚀 Congressional Data API Filter Fix Verification")
    print("=" * 60)
    
    # Step 1: Test basic endpoint
    print("\n📋 STEP 1: Basic Endpoint Test")
    base_test = test_endpoint("/api/v1/members", "All Members (no filters)")
    base_count = base_test['total_results']
    
    if not base_test['success']:
        print("❌ Basic endpoint failed - stopping tests")
        return
    
    print(f"\n✅ Base endpoint working: {base_count} total members")
    
    # Step 2: Test party filters
    print("\n📋 STEP 2: Party Filter Tests")
    
    # Test Republican filter
    republican_test = test_endpoint("/api/v1/members?party=Republican", "Republican Members")
    republican_working = analyze_filter_results(base_count, republican_test['total_results'], 
                                               "party", "Republican")
    
    # Test Democratic filter
    democratic_test = test_endpoint("/api/v1/members?party=Democratic", "Democratic Members")
    democratic_working = analyze_filter_results(base_count, democratic_test['total_results'], 
                                               "party", "Democratic")
    
    # Step 3: Test state filters
    print("\n📋 STEP 3: State Filter Tests")
    
    # Test California filter
    ca_test = test_endpoint("/api/v1/members?state=CA", "California Members")
    ca_working = analyze_filter_results(base_count, ca_test['total_results'], 
                                       "state", "CA")
    
    # Test New York filter
    ny_test = test_endpoint("/api/v1/members?state=NY", "New York Members")
    ny_working = analyze_filter_results(base_count, ny_test['total_results'], 
                                       "state", "NY")
    
    # Step 4: Test chamber filters
    print("\n📋 STEP 4: Chamber Filter Tests")
    
    # Test House filter
    house_test = test_endpoint("/api/v1/members?chamber=House", "House Members")
    house_working = analyze_filter_results(base_count, house_test['total_results'], 
                                          "chamber", "House")
    
    # Test Senate filter
    senate_test = test_endpoint("/api/v1/members?chamber=Senate", "Senate Members")
    senate_working = analyze_filter_results(base_count, senate_test['total_results'], 
                                           "chamber", "Senate")
    
    # Step 5: Test combined filters
    print("\n📋 STEP 5: Combined Filter Tests")
    
    # Test party + state
    combined_test = test_endpoint("/api/v1/members?party=Democratic&state=CA", 
                                 "Democratic California Members")
    combined_working = analyze_filter_results(base_count, combined_test['total_results'], 
                                            "party+state", "Democratic+CA")
    
    # Step 6: Summary
    print("\n📋 STEP 6: Test Summary")
    print("=" * 60)
    
    tests = [
        ("Party (Republican)", republican_working),
        ("Party (Democratic)", democratic_working),
        ("State (CA)", ca_working),
        ("State (NY)", ny_working),
        ("Chamber (House)", house_working),
        ("Chamber (Senate)", senate_working),
        ("Combined (Dem+CA)", combined_working)
    ]
    
    passing_tests = sum(1 for _, working in tests if working)
    total_tests = len(tests)
    
    print(f"Tests Passing: {passing_tests}/{total_tests}")
    
    if passing_tests == total_tests:
        print("🎉 ALL TESTS PASSING - Filter fix is working!")
        print("✅ Production API is ready for full use")
    elif passing_tests > 0:
        print("⚠️ PARTIAL SUCCESS - Some filters working")
        print("🔧 Additional debugging needed")
    else:
        print("❌ ALL TESTS FAILING - Filter fix not working")
        print("🚨 Immediate action required")
    
    print("\n🔍 For detailed debugging, check:")
    print("- Cloud Run logs for any errors")
    print("- Database connectivity")
    print("- SQLAlchemy query generation")

if __name__ == "__main__":
    main()