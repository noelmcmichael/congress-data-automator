#!/usr/bin/env python3
"""
Debug frontend filter issues - specifically chamber filter problems
"""

import requests
import json
from typing import Dict, Any

API_BASE = "https://congressional-data-api-v2-1066017671167.us-central1.run.app"

def test_problematic_filters():
    """Test the specific filters that are causing frontend issues"""
    
    print("🔍 Debug Frontend Filter Issues")
    print("=" * 50)
    
    # Test 1: Chamber filters that are problematic
    print("\n📋 STEP 1: Test Chamber Filters")
    
    chamber_tests = [
        "House",
        "Senate", 
        "house",
        "senate",
        "HOUSE",
        "SENATE"
    ]
    
    for chamber in chamber_tests:
        print(f"\n🔍 Testing chamber={chamber}")
        try:
            response = requests.get(f"{API_BASE}/api/v1/members?chamber={chamber}&limit=5", timeout=10)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Results: {len(data)}")
                if len(data) > 0:
                    print(f"First result: {data[0]['first_name']} {data[0]['last_name']} - {data[0]['chamber']}")
                else:
                    print("No results returned")
            else:
                print(f"Error: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"Error details: {error_data}")
                except:
                    print(f"Error text: {response.text}")
                    
        except Exception as e:
            print(f"Exception: {e}")
    
    # Test 2: Test what happens with invalid filters
    print("\n📋 STEP 2: Test Invalid Filters")
    
    invalid_tests = [
        "?chamber=InvalidChamber",
        "?party=InvalidParty", 
        "?state=InvalidState",
        "?chamber=&party=Republican",  # Empty chamber
        "?chamber=House&party=",       # Empty party
    ]
    
    for test_case in invalid_tests:
        print(f"\n🔍 Testing {test_case}")
        try:
            response = requests.get(f"{API_BASE}/api/v1/members{test_case}", timeout=10)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Results: {len(data)}")
            else:
                print(f"Error: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"Error details: {error_data}")
                except:
                    print(f"Error text: {response.text}")
                    
        except Exception as e:
            print(f"Exception: {e}")
    
    # Test 3: Test committees endpoint with chamber filter
    print("\n📋 STEP 3: Test Committees Endpoint")
    
    committees_tests = [
        "",  # No filter
        "?chamber=House",
        "?chamber=Senate",
        "?chamber=house",
        "?chamber=senate"
    ]
    
    for test_case in committees_tests:
        print(f"\n🔍 Testing committees{test_case}")
        try:
            response = requests.get(f"{API_BASE}/api/v1/committees{test_case}", timeout=10)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Results: {len(data)}")
                if len(data) > 0:
                    print(f"First result: {data[0]['name']} - {data[0]['chamber']}")
            else:
                print(f"Error: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"Error details: {error_data}")
                except:
                    print(f"Error text: {response.text}")
                    
        except Exception as e:
            print(f"Exception: {e}")
    
    # Test 4: Test hearings endpoint
    print("\n📋 STEP 4: Test Hearings Endpoint")
    
    hearings_tests = [
        "",  # No filter
        "?status=scheduled",
        "?status=completed",
        "?search=hearing"
    ]
    
    for test_case in hearings_tests:
        print(f"\n🔍 Testing hearings{test_case}")
        try:
            response = requests.get(f"{API_BASE}/api/v1/hearings{test_case}", timeout=10)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Results: {len(data)}")
                if len(data) > 0:
                    print(f"First result: {data[0]['title']}")
            else:
                print(f"Error: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"Error details: {error_data}")
                except:
                    print(f"Error text: {response.text}")
                    
        except Exception as e:
            print(f"Exception: {e}")

if __name__ == "__main__":
    test_problematic_filters()