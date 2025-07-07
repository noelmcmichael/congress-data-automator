#!/usr/bin/env python3
"""
Check what congress numbers are available in the API
"""

import requests
import time

def check_congress_api():
    """Check different congress numbers to see which are available"""
    
    api_key = 'NcMVmULsduvTXfEIXhKgAb1uWDDFdzOcPI57jpRG'
    base_url = "https://api.congress.gov/v3"
    
    print("🔍 CHECKING CONGRESS.GOV API AVAILABILITY")
    
    # Check recent congress numbers
    congress_numbers = [119, 118, 117, 116, 115]
    
    for congress_num in congress_numbers:
        print(f"\n📋 Testing Congress {congress_num}:")
        
        # Check members endpoint
        members_url = f"{base_url}/member/congress/{congress_num}"
        params = {
            'api_key': api_key,
            'format': 'json',
            'limit': 5
        }
        
        try:
            response = requests.get(members_url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                member_count = data.get('pagination', {}).get('count', 0)
                print(f"   ✅ Members endpoint: {member_count} members")
                
                # Check senate specifically
                senate_url = f"{base_url}/member/congress/{congress_num}/senate"
                response = requests.get(senate_url, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    senate_count = data.get('pagination', {}).get('count', 0)
                    print(f"   ✅ Senate endpoint: {senate_count} senators")
                    
                    # Show first few senators
                    senators = data.get('members', [])[:3]
                    for senator in senators:
                        name = senator.get('name', {})
                        first_name = name.get('first', '')
                        last_name = name.get('last', '')
                        party = senator.get('partyName', '')
                        state = senator.get('state', '')
                        print(f"      - {first_name} {last_name} ({party}-{state})")
                else:
                    print(f"   ❌ Senate endpoint: {response.status_code}")
                    
                # Check house specifically
                house_url = f"{base_url}/member/congress/{congress_num}/house"
                response = requests.get(house_url, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    house_count = data.get('pagination', {}).get('count', 0)
                    print(f"   ✅ House endpoint: {house_count} representatives")
                else:
                    print(f"   ❌ House endpoint: {response.status_code}")
                    
            else:
                print(f"   ❌ Members endpoint: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            
        time.sleep(1)  # Rate limiting
    
    # Try to get current congress info
    print(f"\n📊 CHECKING CURRENT CONGRESS INFO:")
    
    congress_url = f"{base_url}/congress"
    params = {
        'api_key': api_key,
        'format': 'json',
        'limit': 5
    }
    
    try:
        response = requests.get(congress_url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            congresses = data.get('congresses', [])
            
            print(f"   Available congresses:")
            for congress in congresses[:5]:
                congress_num = congress.get('number', '')
                start_year = congress.get('startYear', '')
                end_year = congress.get('endYear', '')
                name = congress.get('name', '')
                print(f"      {congress_num}: {name} ({start_year}-{end_year})")
        else:
            print(f"   ❌ Congress info endpoint: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    check_congress_api()