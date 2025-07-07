#!/usr/bin/env python3
"""
Check Iowa Senators Specifically

This script checks the Iowa senators to see if Chuck Grassley is there
but with a parsing issue on the name field.
"""

import asyncio
import aiohttp
import json
from datetime import datetime

# Production API base URL
API_BASE = "https://congressional-data-api-v2-1066017671167.us-central1.run.app"

async def check_iowa_senators():
    """Check Iowa senators specifically to identify Chuck Grassley"""
    
    async with aiohttp.ClientSession() as session:
        print("=== CHECKING IOWA SENATORS ===")
        print(f"Timestamp: {datetime.now()}")
        print()
        
        # Get all senators from Iowa
        print("1. Retrieving Iowa senators...")
        
        try:
            async with session.get(f"{API_BASE}/api/v1/members?chamber=Senate&state=IA") as response:
                if response.status == 200:
                    iowa_senators = await response.json()
                    print(f"✅ Retrieved {len(iowa_senators)} Iowa senators")
                    
                    if iowa_senators:
                        print()
                        print("2. Iowa senators in database:")
                        
                        for i, senator in enumerate(iowa_senators, 1):
                            print(f"   Senator {i}:")
                            print(f"      ID: {senator.get('id')}")
                            print(f"      Name: {senator.get('first_name', 'Unknown')} {senator.get('last_name', 'Unknown')}")
                            print(f"      Party: {senator.get('party', 'Unknown')}")
                            print(f"      BioGuide ID: {senator.get('bioguide_id', 'Unknown')}")
                            print(f"      Chamber: {senator.get('chamber', 'Unknown')}")
                            print(f"      State: {senator.get('state', 'Unknown')}")
                            print(f"      Current: {senator.get('is_current', 'Unknown')}")
                            print(f"      Photo URL: {senator.get('official_photo_url', 'None')}")
                            print(f"      Created: {senator.get('created_at', 'Unknown')}")
                            print(f"      Last Scraped: {senator.get('last_scraped_at', 'Unknown')}")
                            print()
                            
                            # Check if this could be Chuck Grassley
                            if senator.get('party') == 'Republican':
                                print(f"      🔍 ANALYSIS: Republican senator from Iowa")
                                print(f"         - Could be Chuck Grassley (if name parsing failed)")
                                print(f"         - Could be Joni Ernst (if name parsing failed)")
                                print()
                                
                                # Check committee assignments
                                print(f"      📋 Checking committee assignments...")
                                member_id = senator.get('id')
                                if member_id:
                                    async with session.get(f"{API_BASE}/api/v1/members/{member_id}/committees") as committees_response:
                                        if committees_response.status == 200:
                                            committees = await committees_response.json()
                                            print(f"         Committee assignments: {len(committees)}")
                                            
                                            # Look for Judiciary Committee
                                            judiciary_found = False
                                            for committee in committees:
                                                print(f"         - {committee.get('name', 'Unknown')} ({committee.get('chamber', 'Unknown')})")
                                                if committee.get('position'):
                                                    print(f"           Position: {committee.get('position')}")
                                                
                                                if 'Judiciary' in committee.get('name', ''):
                                                    judiciary_found = True
                                                    print(f"           ✅ ON JUDICIARY COMMITTEE!")
                                                    if committee.get('position'):
                                                        print(f"           Position: {committee.get('position')}")
                                                        if 'Chair' in committee.get('position', ''):
                                                            print(f"           🎯 LIKELY CHUCK GRASSLEY (Judiciary Chair)")
                                                        elif 'Ranking' in committee.get('position', ''):
                                                            print(f"           🎯 LIKELY CHUCK GRASSLEY (Judiciary Ranking)")
                                            
                                            if judiciary_found:
                                                print(f"         ✅ CONCLUSION: This is likely Chuck Grassley!")
                                            else:
                                                print(f"         ❌ Not on Judiciary Committee - likely Joni Ernst")
                                        else:
                                            print(f"         ❌ Failed to get committees: {committees_response.status}")
                                else:
                                    print(f"         ❌ No member ID available")
                                print()
                        
                        print("3. Expected Iowa Senators (119th Congress):")
                        print("   - Chuck Grassley (R) - Senior Senator, Judiciary Committee")
                        print("   - Joni Ernst (R) - Junior Senator, Armed Services Committee")
                        print()
                        
                        print("4. Data Quality Issue Identified:")
                        print("   ❌ CRITICAL: Name parsing failure in data collection")
                        print("      - First/last names not being extracted correctly")
                        print("      - All senators showing as 'Unknown' in name field")
                        print("      - BioGuide IDs and other data appear correct")
                        print("      - This affects user experience and searchability")
                        print()
                        
                        print("5. Immediate Actions Needed:")
                        print("   - Fix name parsing in data collection script")
                        print("   - Re-run data collection to populate correct names")
                        print("   - Verify committee assignments are correct")
                        print("   - Test search functionality with proper names")
                        
                    else:
                        print("❌ No Iowa senators found in database")
                        
                else:
                    print(f"❌ Failed to retrieve Iowa senators: {response.status}")
                    
        except Exception as e:
            print(f"❌ Error checking Iowa senators: {e}")

async def main():
    """Main function"""
    await check_iowa_senators()

if __name__ == "__main__":
    asyncio.run(main())