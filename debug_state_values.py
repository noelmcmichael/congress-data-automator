#!/usr/bin/env python3
"""
Debug state values from API
"""

import requests
import time

def debug_state_values():
    """Debug state values from API"""
    
    api_key = 'NcMVmULsduvTXfEIXhKgAb1uWDDFdzOcPI57jpRG'
    base_url = "https://api.congress.gov/v3"
    
    print("🔍 DEBUGGING STATE VALUES")
    
    url = f"{base_url}/member/congress/119"
    params = {
        'api_key': api_key,
        'format': 'json',
        'limit': 50
    }
    
    try:
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            members = data.get('members', [])
            
            print(f"📊 First 50 members - State values:")
            
            state_values = set()
            
            for member in members:
                state = member.get('state', '')
                state_values.add(state)
                
                # Check if this is a senator
                terms = member.get('terms', {}).get('item', [])
                if terms:
                    latest_term = terms[-1]
                    chamber = latest_term.get('chamber', '')
                    
                    if chamber == 'Senate':
                        name = member.get('name', '')
                        print(f"   Senator: {name} - State: '{state}' (length: {len(state)})")
            
            print(f"\n📋 Unique state values found:")
            for state in sorted(state_values):
                print(f"   '{state}' (length: {len(state)})")
            
        else:
            print(f"❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_state_values()