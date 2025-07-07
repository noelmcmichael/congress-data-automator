#!/usr/bin/env python3
"""
Debug API response structure
"""

import requests
import json

def debug_api_response():
    """Debug the API response structure"""
    
    api_key = 'NcMVmULsduvTXfEIXhKgAb1uWDDFdzOcPI57jpRG'
    base_url = "https://api.congress.gov/v3"
    
    print("🔍 DEBUGGING API RESPONSE STRUCTURE")
    
    # Check members endpoint for 119th Congress
    members_url = f"{base_url}/member/congress/119"
    params = {
        'api_key': api_key,
        'format': 'json',
        'limit': 3
    }
    
    try:
        response = requests.get(members_url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"📊 Raw API Response Structure:")
            print(f"   Status: {response.status_code}")
            print(f"   Response keys: {list(data.keys())}")
            
            if 'members' in data:
                members = data['members']
                print(f"   Members count: {len(members)}")
                
                if members:
                    print(f"\n📋 First Member Structure:")
                    first_member = members[0]
                    print(f"   Type: {type(first_member)}")
                    
                    if isinstance(first_member, dict):
                        print(f"   Keys: {list(first_member.keys())}")
                        
                        # Print some key fields
                        for key in ['name', 'bioguideId', 'partyName', 'state', 'terms']:
                            if key in first_member:
                                print(f"   {key}: {first_member[key]}")
                    else:
                        print(f"   Content: {first_member}")
            
            # Save raw response for analysis
            with open('debug_api_response.json', 'w') as f:
                json.dump(data, f, indent=2)
            
            print(f"\n✅ Raw response saved to debug_api_response.json")
            
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_api_response()