#!/usr/bin/env python3
"""
Examine Senate Judiciary Committee

This script examines the Senate Judiciary Committee structure
to understand why Chuck Grassley is not showing up as a member.
"""

import asyncio
import aiohttp
import json
from datetime import datetime

# Production API base URL
API_BASE = "https://congressional-data-api-v2-1066017671167.us-central1.run.app"

async def examine_judiciary_committee():
    """Examine Senate Judiciary Committee structure"""
    
    async with aiohttp.ClientSession() as session:
        print("=== EXAMINING SENATE JUDICIARY COMMITTEE ===")
        print(f"Timestamp: {datetime.now()}")
        print()
        
        # Find Senate Judiciary Committee
        print("1. Searching for Senate Judiciary Committee...")
        
        try:
            async with session.get(f"{API_BASE}/api/v1/committees?search=Judiciary") as response:
                if response.status == 200:
                    committees = await response.json()
                    print(f"✅ Found {len(committees)} committees matching 'Judiciary'")
                    
                    senate_judiciary = None
                    for committee in committees:
                        print(f"   - {committee.get('name', 'Unknown')} ({committee.get('chamber', 'Unknown')})")
                        if committee.get('chamber') == 'Senate' and 'Judiciary' in committee.get('name', ''):
                            senate_judiciary = committee
                    
                    if senate_judiciary:
                        print(f"✅ Found Senate Judiciary Committee: {senate_judiciary.get('name')}")
                        print(f"   ID: {senate_judiciary.get('id')}")
                        print(f"   Chamber: {senate_judiciary.get('chamber')}")
                        print()
                        
                        # Get committee members
                        print("2. Examining Senate Judiciary Committee members...")
                        
                        committee_id = senate_judiciary.get('id')
                        async with session.get(f"{API_BASE}/api/v1/committees/{committee_id}/members") as members_response:
                            if members_response.status == 200:
                                members = await members_response.json()
                                print(f"✅ Found {len(members)} members on Senate Judiciary Committee")
                                print()
                                
                                # List all members
                                print("   Current members:")
                                grassley_found = False
                                chair_found = False
                                ranking_found = False
                                
                                for member in members:
                                    name = member.get('name', 'Unknown')
                                    position = member.get('position', 'Member')
                                    party = member.get('party', 'Unknown')
                                    state = member.get('state', 'Unknown')
                                    bioguide_id = member.get('bioguide_id', 'Unknown')
                                    
                                    print(f"   - {name} ({party}-{state}) - {position}")
                                    print(f"     BioGuide ID: {bioguide_id}")
                                    
                                    if 'Grassley' in name or bioguide_id == 'G000386':
                                        grassley_found = True
                                        print(f"     ✅ CHUCK GRASSLEY FOUND!")
                                    
                                    if 'Chair' in position:
                                        chair_found = True
                                        print(f"     🎯 COMMITTEE CHAIR: {name}")
                                    elif 'Ranking' in position:
                                        ranking_found = True
                                        print(f"     🎯 RANKING MEMBER: {name}")
                                    
                                    print()
                                
                                # Summary
                                print("3. Analysis:")
                                if grassley_found:
                                    print("   ✅ Chuck Grassley IS on Senate Judiciary Committee")
                                else:
                                    print("   ❌ Chuck Grassley NOT found on Senate Judiciary Committee")
                                    print("      - This confirms the original issue")
                                
                                if chair_found:
                                    print("   ✅ Committee has a Chair")
                                else:
                                    print("   ❌ No Chair identified")
                                
                                if ranking_found:
                                    print("   ✅ Committee has a Ranking Member")
                                else:
                                    print("   ❌ No Ranking Member identified")
                                
                                print()
                                print("4. Expected Senate Judiciary Committee Leadership (119th Congress):")
                                print("   - Chair: Likely Chuck Grassley (R-IA) if Republicans control Senate")
                                print("   - Ranking Member: Likely Dick Durbin (D-IL) if Republicans control Senate")
                                print("   - OR Chair: Dick Durbin (D-IL) if Democrats control Senate")
                                print("   - OR Ranking Member: Chuck Grassley (R-IA) if Democrats control Senate")
                                print()
                                
                                # Check for other key members
                                print("5. Looking for other key Judiciary Committee members:")
                                expected_members = [
                                    'Grassley', 'Durbin', 'Graham', 'Whitehouse', 'Cornyn', 
                                    'Klobuchar', 'Cruz', 'Coons', 'Hawley', 'Hirono'
                                ]
                                
                                found_members = []
                                for member in members:
                                    name = member.get('name', '')
                                    for expected in expected_members:
                                        if expected in name:
                                            found_members.append(expected)
                                            break
                                
                                print(f"   Expected key members found: {len(found_members)}/{len(expected_members)}")
                                print(f"   Found: {', '.join(found_members)}")
                                print(f"   Missing: {', '.join(set(expected_members) - set(found_members))}")
                                
                                if len(found_members) < len(expected_members) / 2:
                                    print("   ❌ CRITICAL: Major committee membership gaps")
                                    print("      - This indicates systematic data collection issues")
                                    print("      - Committee assignments may be incomplete or incorrect")
                                
                            else:
                                print(f"   ❌ Failed to get committee members: {members_response.status}")
                    else:
                        print("❌ Senate Judiciary Committee not found")
                        
                        # Check what committees we do have
                        print()
                        print("Available committees:")
                        for committee in committees:
                            print(f"   - {committee.get('name', 'Unknown')} ({committee.get('chamber', 'Unknown')})")
                        
                else:
                    print(f"❌ Failed to search for committees: {response.status}")
                    
        except Exception as e:
            print(f"❌ Error examining Judiciary Committee: {e}")
        
        print()
        print("6. Next Steps:")
        print("   - Verify committee data collection from Congress.gov API")
        print("   - Check if committee-member relationships are being created correctly")
        print("   - Look for data in committee_memberships table")
        print("   - Consider manual verification of Chuck Grassley's committee assignments")

async def main():
    """Main function"""
    await examine_judiciary_committee()

if __name__ == "__main__":
    asyncio.run(main())