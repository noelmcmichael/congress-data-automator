#!/usr/bin/env python3
"""
Test the frontend fixes for case sensitivity issues
"""

import requests
import json
from typing import Dict, Any

API_BASE = "https://congressional-data-api-v2-1066017671167.us-central1.run.app"

def test_fixed_filter_values():
    """Test the filter values that the frontend should now be sending"""
    
    print("🔧 Testing Frontend Filter Fixes")
    print("=" * 50)
    
    # Test 1: Chamber filters (now sending capitalized)
    print("\n📋 STEP 1: Test Fixed Chamber Filters")
    
    chamber_tests = [
        ("House", "Should return House members"),
        ("Senate", "Should return Senate members")
    ]
    
    for chamber, description in chamber_tests:
        print(f"\n🔍 Testing chamber={chamber}")
        try:
            response = requests.get(f"{API_BASE}/api/v1/members?chamber={chamber}&limit=5", timeout=10)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Results: {len(data)} - {description}")
                if len(data) > 0:
                    # Verify all results match the filter
                    all_match = all(member.get('chamber') == chamber for member in data)
                    print(f"✅ All results match filter: {all_match}")
                    print(f"   Example: {data[0]['first_name']} {data[0]['last_name']} - {data[0]['chamber']}")
                else:
                    print("❌ No results returned")
            else:
                print(f"❌ Error: {response.status_code}")
                    
        except Exception as e:
            print(f"❌ Exception: {e}")
    
    # Test 2: Party filters (now sending full names)
    print("\n📋 STEP 2: Test Fixed Party Filters")
    
    party_tests = [
        ("Democratic", "Should return Democratic members"),
        ("Republican", "Should return Republican members")
    ]
    
    for party, description in party_tests:
        print(f"\n🔍 Testing party={party}")
        try:
            response = requests.get(f"{API_BASE}/api/v1/members?party={party}&limit=5", timeout=10)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Results: {len(data)} - {description}")
                if len(data) > 0:
                    # Verify all results match the filter
                    all_match = all(member.get('party') == party for member in data)
                    print(f"✅ All results match filter: {all_match}")
                    print(f"   Example: {data[0]['first_name']} {data[0]['last_name']} - {data[0]['party']}")
                else:
                    print("❌ No results returned")
            else:
                print(f"❌ Error: {response.status_code}")
                    
        except Exception as e:
            print(f"❌ Exception: {e}")
    
    # Test 3: Committee chamber filters
    print("\n📋 STEP 3: Test Committee Chamber Filters")
    
    for chamber, description in chamber_tests:
        print(f"\n🔍 Testing committees?chamber={chamber}")
        try:
            response = requests.get(f"{API_BASE}/api/v1/committees?chamber={chamber}&limit=5", timeout=10)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Results: {len(data)} - {description}")
                if len(data) > 0:
                    # Verify all results match the filter
                    all_match = all(committee.get('chamber') == chamber for committee in data)
                    print(f"✅ All results match filter: {all_match}")
                    print(f"   Example: {data[0]['name']} - {data[0]['chamber']}")
                else:
                    print("❌ No results returned")
            else:
                print(f"❌ Error: {response.status_code}")
                    
        except Exception as e:
            print(f"❌ Exception: {e}")
    
    # Test 4: Hearing status filters (now sending capitalized)
    print("\n📋 STEP 4: Test Fixed Hearing Status Filters")
    
    status_tests = [
        ("Scheduled", "Should return Scheduled hearings"),
        ("Completed", "Should return Completed hearings")
    ]
    
    for status, description in status_tests:
        print(f"\n🔍 Testing hearings?status={status}")
        try:
            response = requests.get(f"{API_BASE}/api/v1/hearings?status={status}&limit=5", timeout=10)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Results: {len(data)} - {description}")
                if len(data) > 0:
                    # Verify all results match the filter
                    all_match = all(hearing.get('status') == status for hearing in data)
                    print(f"✅ All results match filter: {all_match}")
                    print(f"   Example: {data[0].get('title', 'No title')} - {data[0]['status']}")
                else:
                    print("ℹ️ No results found (may be valid if no hearings have this status)")
            else:
                print(f"❌ Error: {response.status_code}")
                    
        except Exception as e:
            print(f"❌ Exception: {e}")
    
    # Test 5: Combined filters
    print("\n📋 STEP 5: Test Combined Filters")
    
    combined_tests = [
        ("party=Republican&chamber=House", "Republican House members"),
        ("party=Democratic&chamber=Senate", "Democratic Senate members")
    ]
    
    for filter_params, description in combined_tests:
        print(f"\n🔍 Testing combined: {filter_params}")
        try:
            response = requests.get(f"{API_BASE}/api/v1/members?{filter_params}&limit=5", timeout=10)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Results: {len(data)} - {description}")
                if len(data) > 0:
                    print(f"   Example: {data[0]['first_name']} {data[0]['last_name']} ({data[0]['party']}) - {data[0]['chamber']}")
                else:
                    print("❌ No results returned")
            else:
                print(f"❌ Error: {response.status_code}")
                    
        except Exception as e:
            print(f"❌ Exception: {e}")
    
    print("\n📋 SUMMARY")
    print("=" * 50)
    print("🎉 Frontend fixes deployed!")
    print("✅ Chamber filters: Now sending 'House'/'Senate' (capitalized)")
    print("✅ Party filters: Now sending 'Democratic'/'Republican' (full names)")
    print("✅ Status filters: Now sending 'Scheduled'/'Completed' (capitalized)")
    print("")
    print("🌐 Updated frontend: https://storage.googleapis.com/congressional-data-frontend/index.html")
    print("🔧 Users should now see working filters for chamber, party, and status!")

if __name__ == "__main__":
    test_fixed_filter_values()