#!/usr/bin/env python3
"""
Examine the actual API data structure
"""

import requests
import json
import time

def examine_api_data():
    """Examine the API data structure"""
    
    api_key = 'NcMVmULsduvTXfEIXhKgAb1uWDDFdzOcPI57jpRG'
    base_url = "https://api.congress.gov/v3"
    
    print("🔍 EXAMINING API DATA STRUCTURE")
    
    # Check members endpoint for 119th Congress
    members_url = f"{base_url}/member/congress/119"
    params = {
        'api_key': api_key,
        'format': 'json',
        'limit': 10
    }
    
    try:
        response = requests.get(members_url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"📊 119th Congress Members:")
            print(f"   Total members: {data.get('pagination', {}).get('count', 0)}")
            
            members = data.get('members', [])
            
            # Analyze senators and representatives
            senators = []
            representatives = []
            
            for member in members[:20]:  # Look at first 20 members
                name = member.get('name', {})
                first_name = name.get('first', '')
                last_name = name.get('last', '')
                party = member.get('partyName', '')
                state = member.get('state', '')
                
                # Check if this is a senator
                terms = member.get('terms', {}).get('item', [])
                current_chamber = None
                
                if terms:
                    latest_term = terms[-1]  # Get most recent term
                    current_chamber = latest_term.get('chamber', '')
                
                member_info = {
                    'name': f"{first_name} {last_name}",
                    'party': party,
                    'state': state,
                    'chamber': current_chamber,
                    'bioguide_id': member.get('bioguideId', ''),
                    'district': latest_term.get('district', '') if terms else ''
                }
                
                if current_chamber == 'Senate':
                    senators.append(member_info)
                elif current_chamber == 'House of Representatives':
                    representatives.append(member_info)
                
                print(f"   {first_name} {last_name} ({party}-{state}) - {current_chamber}")
                
                if len(senators) >= 5 and len(representatives) >= 5:
                    break
            
            print(f"\n📋 SENATORS FOUND: {len(senators)}")
            for senator in senators:
                print(f"   {senator['name']} ({senator['party']}-{senator['state']})")
            
            print(f"\n📋 REPRESENTATIVES FOUND: {len(representatives)}")
            for rep in representatives:
                district = f" {rep['district']}" if rep['district'] else ""
                print(f"   {rep['name']} ({rep['party']}-{rep['state']}{district})")
            
            # Now let's get ALL members to see the full dataset
            print(f"\n🔍 FETCHING ALL MEMBERS...")
            all_members = []
            offset = 0
            limit = 250
            
            while True:
                params = {
                    'api_key': api_key,
                    'format': 'json',
                    'offset': offset,
                    'limit': limit
                }
                
                response = requests.get(members_url, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    members = data.get('members', [])
                    
                    print(f"   Fetched {len(members)} members (offset {offset})")
                    
                    all_members.extend(members)
                    
                    # Check if there are more pages
                    if len(members) < limit:
                        break
                        
                    offset += limit
                    time.sleep(0.5)  # Rate limiting
                else:
                    print(f"   ❌ Error fetching offset {offset}: {response.status_code}")
                    break
            
            print(f"\n📊 TOTAL MEMBERS FETCHED: {len(all_members)}")
            
            # Analyze all members by chamber
            all_senators = []
            all_representatives = []
            
            for member in all_members:
                terms = member.get('terms', {}).get('item', [])
                
                if terms:
                    latest_term = terms[-1]
                    chamber = latest_term.get('chamber', '')
                    
                    if chamber == 'Senate':
                        all_senators.append(member)
                    elif chamber == 'House of Representatives':
                        all_representatives.append(member)
            
            print(f"\n📋 CHAMBER BREAKDOWN:")
            print(f"   Senators: {len(all_senators)}")
            print(f"   Representatives: {len(all_representatives)}")
            
            # Save the data for analysis
            output_data = {
                'total_members': len(all_members),
                'senators': len(all_senators),
                'representatives': len(all_representatives),
                'senator_data': all_senators,
                'representative_data': all_representatives
            }
            
            with open('congress_119_data.json', 'w') as f:
                json.dump(output_data, f, indent=2)
            
            print(f"\n✅ Data saved to congress_119_data.json")
            
        else:
            print(f"❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    examine_api_data()