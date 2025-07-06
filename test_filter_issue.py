#!/usr/bin/env python3
"""
Simple test script to demonstrate the critical filter issue
"""

import requests
import json

BASE_URL = "https://congressional-data-api-v2-1066017671167.us-central1.run.app"

def test_filters():
    print("🚨 DEMONSTRATING CRITICAL FILTER ISSUE")
    print("="*60)
    
    # Test 1: No filter
    response1 = requests.get(f"{BASE_URL}/api/v1/members")
    data1 = response1.json()
    print(f"No filter - Total members: {len(data1)}")
    print(f"First member: {data1[0]['first_name']} {data1[0]['last_name']} ({data1[0]['party']})")
    
    # Test 2: Republican filter
    response2 = requests.get(f"{BASE_URL}/api/v1/members?party=Republican")
    data2 = response2.json()
    print(f"\nRepublican filter - Total members: {len(data2)}")
    print(f"First member: {data2[0]['first_name']} {data2[0]['last_name']} ({data2[0]['party']})")
    
    # Test 3: Democratic filter  
    response3 = requests.get(f"{BASE_URL}/api/v1/members?party=Democratic")
    data3 = response3.json()
    print(f"\nDemocratic filter - Total members: {len(data3)}")
    print(f"First member: {data3[0]['first_name']} {data3[0]['last_name']} ({data3[0]['party']})")
    
    # Analysis
    print("\n" + "="*60)
    print("ANALYSIS:")
    
    if len(data1) == len(data2) == len(data3):
        print("🚨 CRITICAL: All queries return SAME NUMBER of results")
        print("🚨 CRITICAL: Filters are being COMPLETELY IGNORED")
    
    if data1[0]['id'] == data2[0]['id'] == data3[0]['id']:
        print("🚨 CRITICAL: All queries return SAME FIRST MEMBER")
        print("🚨 CRITICAL: Same exact ordering regardless of filter")
    
    # Count actual parties in "Republican" filter results
    parties_in_rep_filter = {}
    for member in data2[:10]:  # Check first 10
        party = member['party']
        parties_in_rep_filter[party] = parties_in_rep_filter.get(party, 0) + 1
    
    print(f"\nParties found in 'Republican' filter (first 10 members):")
    for party, count in parties_in_rep_filter.items():
        print(f"  {party}: {count}")
    
    if 'Democratic' in parties_in_rep_filter:
        print("🚨 CRITICAL: Democratic members found in Republican filter!")

if __name__ == "__main__":
    test_filters()