#!/usr/bin/env python3
"""
Debug Grassley Search Issue

This script debugs why Chuck Grassley isn't being found in search results.
"""

import asyncio
import aiohttp
import json
from datetime import datetime

# Production API base URL
API_BASE = "https://congressional-data-api-v2-1066017671167.us-central1.run.app"

async def debug_grassley_search():
    """Debug why Chuck Grassley isn't found in search"""
    
    async with aiohttp.ClientSession() as session:
        print("=== DEBUGGING CHUCK GRASSLEY SEARCH ===")
        print(f"Timestamp: {datetime.now()}")
        print()
        
        # Test different search patterns
        search_patterns = [
            "Chuck Grassley",
            "Grassley",
            "Chuck",
            "G000386",  # His BioGuide ID
            "Iowa"
        ]
        
        for pattern in search_patterns:
            print(f"1. Searching for '{pattern}'...")
            
            try:
                async with session.get(f"{API_BASE}/api/v1/members?search={pattern}") as response:
                    if response.status == 200:
                        members = await response.json()
                        print(f"   ✅ Found {len(members)} members")
                        
                        if members:
                            for member in members:
                                name = member.get('name', 'Unknown')
                                state = member.get('state', 'Unknown')
                                party = member.get('party', 'Unknown')
                                bioguide_id = member.get('bioguide_id', 'Unknown')
                                print(f"      - {name} ({party}-{state}) - {bioguide_id}")
                                
                                # Check if this could be Grassley
                                if (('Grassley' in name) or 
                                    (bioguide_id == 'G000386') or
                                    (state == 'IA' and party == 'Republican')):
                                    print(f"        🎯 POTENTIAL MATCH!")
                        else:
                            print(f"   ❌ No members found")
                    else:
                        print(f"   ❌ Search failed: {response.status}")
                        
            except Exception as e:
                print(f"   ❌ Error searching for '{pattern}': {e}")
            
            print()
        
        # Check Iowa senators directly
        print("2. Checking Iowa senators directly...")
        
        try:
            async with session.get(f"{API_BASE}/api/v1/members?state=IA&chamber=Senate") as response:
                if response.status == 200:
                    iowa_senators = await response.json()
                    print(f"   ✅ Found {len(iowa_senators)} Iowa senators")
                    
                    for senator in iowa_senators:
                        print(f"   Senator Details:")
                        print(f"      ID: {senator.get('id')}")
                        print(f"      Name: '{senator.get('name', 'Unknown')}'")
                        print(f"      First Name: '{senator.get('first_name', 'Unknown')}'")
                        print(f"      Last Name: '{senator.get('last_name', 'Unknown')}'")
                        print(f"      Party: '{senator.get('party', 'Unknown')}'")
                        print(f"      State: '{senator.get('state', 'Unknown')}'")
                        print(f"      BioGuide ID: '{senator.get('bioguide_id', 'Unknown')}'")
                        print()
                        
                        # Check if this is Grassley
                        if senator.get('bioguide_id') == 'G000386':
                            print(f"      🎯 THIS IS CHUCK GRASSLEY!")
                            print(f"         Full name field: '{senator.get('name')}'")
                            print(f"         Search should match: 'Grassley' in '{senator.get('name')}'")
                            print(f"         Match test: {'Grassley' in senator.get('name', '')}")
                            print()
                else:
                    print(f"   ❌ Failed to get Iowa senators: {response.status}")
                    
        except Exception as e:
            print(f"   ❌ Error getting Iowa senators: {e}")
        
        # Test the search functionality itself
        print("3. Testing search functionality...")
        
        try:
            async with session.get(f"{API_BASE}/api/v1/members?search=") as response:
                if response.status == 200:
                    all_members = await response.json()
                    print(f"   ✅ All members query returned {len(all_members)} members")
                    
                    # Look for any member with 'Grassley' in any field
                    grassley_matches = []
                    for member in all_members:
                        member_str = json.dumps(member).lower()
                        if 'grassley' in member_str:
                            grassley_matches.append(member)
                    
                    if grassley_matches:
                        print(f"   ✅ Found {len(grassley_matches)} potential Grassley matches:")
                        for match in grassley_matches:
                            print(f"      - {match.get('name', 'Unknown')} (ID: {match.get('id')})")
                    else:
                        print(f"   ❌ No Grassley matches found in entire database")
                        
                        # Check for any Iowa senators
                        iowa_members = [m for m in all_members if m.get('state') == 'IA']
                        print(f"   Iowa members found: {len(iowa_members)}")
                        
                        for member in iowa_members:
                            print(f"      - {member.get('name')} ({member.get('chamber')})")
                            
                else:
                    print(f"   ❌ Failed to get all members: {response.status}")
                    
        except Exception as e:
            print(f"   ❌ Error testing search: {e}")
        
        print()
        print("4. Analysis:")
        print("   This will help us understand:")
        print("   - If Chuck Grassley is in the database at all")
        print("   - What his name field actually contains")
        print("   - Why search isn't matching him")
        print("   - If there are data quality issues")

async def main():
    """Main function"""
    await debug_grassley_search()

if __name__ == "__main__":
    asyncio.run(main())