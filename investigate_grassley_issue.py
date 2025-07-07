#!/usr/bin/env python3
"""
Investigate Chuck Grassley Committee Assignment Issue

This script checks the current state of Chuck Grassley's committee assignments
in our database and compares with known facts about his committee positions.
"""

import asyncio
import aiohttp
import json
from datetime import datetime

# Production API base URL
API_BASE = "https://congressional-data-api-v2-1066017671167.us-central1.run.app"

async def investigate_grassley():
    """Investigate Chuck Grassley's committee assignments"""
    
    async with aiohttp.ClientSession() as session:
        print("=== INVESTIGATING CHUCK GRASSLEY COMMITTEE ASSIGNMENTS ===")
        print(f"Timestamp: {datetime.now()}")
        print()
        
        # Step 1: Find Chuck Grassley in our database
        print("1. Searching for Chuck Grassley in database...")
        
        try:
            async with session.get(f"{API_BASE}/api/v1/members?search=Grassley") as response:
                if response.status == 200:
                    members = await response.json()
                    grassley_members = [m for m in members if "Grassley" in m.get("name", "")]
                    
                    if grassley_members:
                        grassley = grassley_members[0]
                        print(f"✅ Found: {grassley['name']}")
                        print(f"   Chamber: {grassley.get('chamber', 'Unknown')}")
                        print(f"   Party: {grassley.get('party', 'Unknown')}")
                        print(f"   State: {grassley.get('state', 'Unknown')}")
                        print(f"   ID: {grassley.get('id', 'Unknown')}")
                        print()
                        
                        # Step 2: Check his committee assignments
                        print("2. Checking Chuck Grassley's committee assignments...")
                        
                        member_id = grassley['id']
                        async with session.get(f"{API_BASE}/api/v1/members/{member_id}/committees") as committees_response:
                            if committees_response.status == 200:
                                committees = await committees_response.json()
                                
                                print(f"   Current assignments: {len(committees)} committees")
                                
                                # Check for Senate Judiciary Committee
                                judiciary_found = False
                                for committee in committees:
                                    print(f"   - {committee['name']} ({committee.get('chamber', 'Unknown')})")
                                    if committee.get('position'):
                                        print(f"     Position: {committee['position']}")
                                    
                                    if "Judiciary" in committee['name'] and committee.get('chamber') == 'Senate':
                                        judiciary_found = True
                                        print(f"     ✅ FOUND: Senate Judiciary Committee")
                                        if committee.get('position'):
                                            print(f"     Position: {committee['position']}")
                                        else:
                                            print(f"     ⚠️  No position listed")
                                
                                if not judiciary_found:
                                    print("   ❌ ISSUE CONFIRMED: Chuck Grassley NOT listed on Senate Judiciary Committee")
                                    print()
                                    
                                    # Step 3: Check if Senate Judiciary Committee exists
                                    print("3. Checking if Senate Judiciary Committee exists in database...")
                                    
                                    async with session.get(f"{API_BASE}/api/v1/committees?search=Judiciary") as judiciary_response:
                                        if judiciary_response.status == 200:
                                            judiciary_committees = await judiciary_response.json()
                                            
                                            senate_judiciary = None
                                            for committee in judiciary_committees:
                                                if committee.get('chamber') == 'Senate' and 'Judiciary' in committee['name']:
                                                    senate_judiciary = committee
                                                    break
                                            
                                            if senate_judiciary:
                                                print(f"   ✅ Senate Judiciary Committee exists: {senate_judiciary['name']}")
                                                print(f"   Committee ID: {senate_judiciary['id']}")
                                                
                                                # Check who is listed as members
                                                committee_id = senate_judiciary['id']
                                                async with session.get(f"{API_BASE}/api/v1/committees/{committee_id}/members") as members_response:
                                                    if members_response.status == 200:
                                                        committee_members = await members_response.json()
                                                        
                                                        print(f"   Current Senate Judiciary members: {len(committee_members)}")
                                                        
                                                        # Look for leadership positions
                                                        chair_found = False
                                                        ranking_found = False
                                                        
                                                        for member in committee_members:
                                                            position = member.get('position', 'Member')
                                                            print(f"   - {member['name']} ({position})")
                                                            
                                                            if 'Chair' in position:
                                                                chair_found = True
                                                                print(f"     ✅ Current Chair: {member['name']}")
                                                            elif 'Ranking' in position:
                                                                ranking_found = True
                                                                print(f"     ✅ Current Ranking Member: {member['name']}")
                                                        
                                                        if not chair_found:
                                                            print("     ⚠️  No Chairman listed")
                                                        if not ranking_found:
                                                            print("     ⚠️  No Ranking Member listed")
                                                        
                                                        # Check if Grassley is listed at all
                                                        grassley_in_judiciary = any(
                                                            "Grassley" in member.get('name', '') for member in committee_members
                                                        )
                                                        
                                                        if not grassley_in_judiciary:
                                                            print("   ❌ CONFIRMED: Chuck Grassley NOT listed as Senate Judiciary member")
                                                        else:
                                                            print("   ✅ Chuck Grassley IS listed as Senate Judiciary member")
                                                    else:
                                                        print(f"   ❌ Failed to get Senate Judiciary members: {members_response.status}")
                                            else:
                                                print("   ❌ Senate Judiciary Committee NOT found in database")
                                        else:
                                            print(f"   ❌ Failed to search for Judiciary committees: {judiciary_response.status}")
                                else:
                                    print("   ✅ Chuck Grassley IS listed on Senate Judiciary Committee")
                            else:
                                print(f"   ❌ Failed to get committees for Grassley: {committees_response.status}")
                    else:
                        print("❌ Chuck Grassley NOT found in database")
                else:
                    print(f"❌ Failed to search for Grassley: {response.status}")
        except Exception as e:
            print(f"❌ Error investigating Grassley: {e}")
        
        print()
        print("=== INVESTIGATION COMPLETE ===")
        print()
        
        # Step 4: Known facts verification
        print("4. Known Facts about Chuck Grassley (119th Congress):")
        print("   - Senator from Iowa (R)")
        print("   - Senior member of Senate Judiciary Committee")
        print("   - Likely Chairman or Ranking Member (depends on majority control)")
        print("   - Also serves on Agriculture, Budget, Finance committees")
        print()
        
        print("5. Recommended Actions:")
        print("   - Verify Grassley's current committee assignments from official sources")
        print("   - Check if he's Chairman or Ranking Member of Senate Judiciary")
        print("   - Update database with correct assignments")
        print("   - Implement scraping to keep assignments current")

async def main():
    """Main function"""
    await investigate_grassley()

if __name__ == "__main__":
    asyncio.run(main())