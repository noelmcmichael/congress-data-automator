#!/usr/bin/env python3
"""
Debug script to test production API filter functionality
Tests the broken filter system to document current behavior
"""

import requests
import json
from typing import Dict, Any, List

# Production API base URL
BASE_URL = "https://congressional-data-api-v2-1066017671167.us-central1.run.app"

def test_endpoint(endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Test an API endpoint with optional parameters"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        response = requests.get(url, params=params, timeout=30)
        print(f"\n{'='*60}")
        print(f"URL: {response.url}")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            # Extract key metrics
            total_count = data.get('total_count', 0)
            items = data.get('items', [])
            actual_count = len(items)
            
            print(f"Total Count: {total_count}")
            print(f"Items Returned: {actual_count}")
            
            # Show first few items for verification
            if items:
                print(f"\nFirst 3 items:")
                for i, item in enumerate(items[:3]):
                    if 'name' in item:
                        party = item.get('party', 'N/A')
                        state = item.get('state', 'N/A')
                        chamber = item.get('chamber', 'N/A')
                        print(f"  {i+1}. {item['name']} ({party}) - {state} {chamber}")
                    elif 'committee_name' in item:
                        chamber = item.get('chamber', 'N/A')
                        print(f"  {i+1}. {item['committee_name']} - {chamber}")
                    elif 'title' in item:
                        status = item.get('status', 'N/A')
                        date = item.get('date', 'N/A')
                        print(f"  {i+1}. {item['title']} - {status} {date}")
            
            return {
                'success': True,
                'total_count': total_count,
                'actual_count': actual_count,
                'data': data
            }
        else:
            print(f"Error: {response.text}")
            return {'success': False, 'error': response.text}
            
    except Exception as e:
        print(f"Exception: {str(e)}")
        return {'success': False, 'error': str(e)}

def main():
    """Test production API filter functionality"""
    
    print("🚨 TESTING PRODUCTION API FILTER FUNCTIONALITY")
    print(f"API Base URL: {BASE_URL}")
    
    # Test 1: Baseline - No filters
    print("\n" + "="*80)
    print("TEST 1: BASELINE - No Filters")
    baseline = test_endpoint("/api/v1/members")
    
    # Test 2: Party Filter - Republican
    print("\n" + "="*80)
    print("TEST 2: PARTY FILTER - Republicans")
    print("Expected: Should return only Republican members (276 total)")
    republican_test = test_endpoint("/api/v1/members", {"party": "Republican"})
    
    # Test 3: Party Filter - Democratic
    print("\n" + "="*80)
    print("TEST 3: PARTY FILTER - Democrats")
    print("Expected: Should return only Democratic members (262 total)")
    democratic_test = test_endpoint("/api/v1/members", {"party": "Democratic"})
    
    # Test 4: State Filter - California
    print("\n" + "="*80)
    print("TEST 4: STATE FILTER - California")
    print("Expected: Should return only CA members (45+ total)")
    ca_test = test_endpoint("/api/v1/members", {"state": "CA"})
    
    # Test 5: Chamber Filter - House
    print("\n" + "="*80)
    print("TEST 5: CHAMBER FILTER - House")
    print("Expected: Should return only House members (483 total)")
    house_test = test_endpoint("/api/v1/members", {"chamber": "House"})
    
    # Test 6: Combined Filters
    print("\n" + "="*80)
    print("TEST 6: COMBINED FILTERS - Democratic + California")
    print("Expected: Should return only Democratic members from CA")
    combined_test = test_endpoint("/api/v1/members", {
        "party": "Democratic", 
        "state": "CA"
    })
    
    # Test 7: Search functionality
    print("\n" + "="*80)
    print("TEST 7: SEARCH - Name contains 'John'")
    print("Expected: Should return members with 'John' in name")
    search_test = test_endpoint("/api/v1/members", {"search": "John"})
    
    # Analysis
    print("\n" + "="*80)
    print("ANALYSIS SUMMARY")
    print("="*80)
    
    if baseline['success'] and republican_test['success'] and democratic_test['success']:
        baseline_count = baseline['total_count']
        rep_count = republican_test['total_count']
        dem_count = democratic_test['total_count']
        
        print(f"Baseline (no filter): {baseline_count} members")
        print(f"Republican filter: {rep_count} members")
        print(f"Democratic filter: {dem_count} members")
        
        # Check if filters are working
        if rep_count == baseline_count and dem_count == baseline_count:
            print("\n🚨 CRITICAL ISSUE CONFIRMED: Filters are being IGNORED")
            print("All filter tests return identical results to baseline")
        elif rep_count + dem_count != baseline_count:
            print(f"\n⚠️ FILTER LOGIC ISSUE: Rep({rep_count}) + Dem({dem_count}) != Total({baseline_count})")
        else:
            print(f"\n✅ FILTERS WORKING: Rep({rep_count}) + Dem({dem_count}) = Total({baseline_count})")
    
    # Test committees endpoint as well
    print("\n" + "="*80)
    print("TESTING COMMITTEES ENDPOINT")
    committee_baseline = test_endpoint("/api/v1/committees")
    committee_house = test_endpoint("/api/v1/committees", {"chamber": "House"})
    
    if committee_baseline['success'] and committee_house['success']:
        if committee_baseline['total_count'] == committee_house['total_count']:
            print("🚨 COMMITTEE FILTERS ALSO BROKEN - Same count for filtered and unfiltered")
        else:
            print("✅ Committee filters appear to be working")

if __name__ == "__main__":
    main()