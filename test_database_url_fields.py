#!/usr/bin/env python3
"""
Test script to check database URL field status
"""

import os
import sys
import requests
import json

def test_api_committee_schema():
    """Test what fields are actually returned by the API"""
    print("=== TESTING API COMMITTEE SCHEMA ===")
    
    # Test a main committee endpoint
    url = "https://congressional-data-api-v2-1066017671167.us-central1.run.app/api/v1/committees?search=Appropriations&chamber=House&limit=1"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data:
                committee = data[0]
                print(f"Committee ID: {committee.get('id')}")
                print(f"Committee Name: {committee.get('name')}")
                print(f"Fields in response:")
                for key, value in committee.items():
                    print(f"  {key}: {value}")
                
                # Check specifically for URL fields
                url_fields = ['hearings_url', 'members_url', 'official_website_url', 'website_url', 'website', 'last_url_update']
                print(f"\nURL Fields Status:")
                for field in url_fields:
                    if field in committee:
                        print(f"  ✅ {field}: {committee[field]}")
                    else:
                        print(f"  ❌ {field}: MISSING")
            else:
                print("No committees found")
        else:
            print(f"API request failed: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Error testing API: {e}")

def test_multiple_committees():
    """Test multiple committees to see if any have URL data"""
    print("\n=== TESTING MULTIPLE COMMITTEES FOR URL DATA ===")
    
    # Test several main committees
    test_committees = [
        ("Appropriations", "House"),
        ("Judiciary", "Senate"),
        ("Armed Services", "House"),
        ("Finance", "Senate")
    ]
    
    for name, chamber in test_committees:
        url = f"https://congressional-data-api-v2-1066017671167.us-central1.run.app/api/v1/committees?search={name}&chamber={chamber}&limit=1"
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if data:
                    committee = data[0]
                    print(f"\n{chamber} {name} (ID: {committee.get('id')}):")
                    
                    # Check URL fields
                    url_fields = ['hearings_url', 'members_url', 'official_website_url', 'website_url', 'website']
                    has_any_urls = False
                    for field in url_fields:
                        if field in committee and committee[field] is not None:
                            print(f"  ✅ {field}: {committee[field]}")
                            has_any_urls = True
                    
                    if not has_any_urls:
                        print(f"  ❌ No URL fields populated")
        except Exception as e:
            print(f"Error testing {chamber} {name}: {e}")

def check_database_schema():
    """Check if database has URL fields by testing specific committee endpoint"""
    print("\n=== TESTING INDIVIDUAL COMMITTEE ENDPOINT ===")
    
    # Test specific committee endpoint 
    url = "https://congressional-data-api-v2-1066017671167.us-central1.run.app/api/v1/committees/7"  # House Appropriations
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            committee = response.json()
            print(f"Committee: {committee.get('name')}")
            print(f"All fields returned:")
            for key, value in committee.items():
                print(f"  {key}: {value}")
        else:
            print(f"API request failed: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Testing database URL fields status...")
    
    test_api_committee_schema()
    test_multiple_committees()
    check_database_schema()
    
    print("\n=== SUMMARY ===")
    print("This test shows what fields are actually available in the current API")
    print("If URL fields are missing, it indicates the enhanced schema is not deployed")