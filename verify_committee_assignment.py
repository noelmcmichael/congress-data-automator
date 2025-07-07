#!/usr/bin/env python3
"""
Verify Committee Assignment

Check if Chuck Grassley's committee assignment is correctly added.
"""

import psycopg2
import asyncio
import aiohttp

async def verify_assignment():
    """Verify the committee assignment"""
    print("🔍 Verifying Chuck Grassley's committee assignment...")
    
    # Database connection
    conn = psycopg2.connect(
        host='localhost',
        port=5433,
        database='congress_data',
        user='postgres',
        password='mDf3S9ZnBpQqJvGsY1'
    )
    
    try:
        with conn.cursor() as cursor:
            # Check if committee membership exists in database
            cursor.execute("""
                SELECT cm.id, cm.member_id, cm.committee_id, cm.position, 
                       m.first_name, m.last_name, c.name
                FROM committee_memberships cm
                JOIN members m ON cm.member_id = m.id
                JOIN committees c ON cm.committee_id = c.id
                WHERE m.bioguide_id = 'G000386';
            """)
            
            assignments = cursor.fetchall()
            print(f"📋 Chuck Grassley's committee assignments in database: {len(assignments)}")
            
            for assignment in assignments:
                print(f"  - {assignment[6]} ({assignment[3] or 'Member'})")
            
            # Check via API
            async with aiohttp.ClientSession() as session:
                # First get Grassley's member ID via API
                async with session.get("https://congressional-data-api-v2-1066017671167.us-central1.run.app/api/v1/members?search=Grassley") as response:
                    if response.status == 200:
                        members = await response.json()
                        grassley_member = None
                        for member in members:
                            if member.get('bioguide_id') == 'G000386':
                                grassley_member = member
                                break
                        
                        if grassley_member:
                            print(f"✅ Found Grassley via API: {grassley_member['first_name']} {grassley_member['last_name']}")
                            
                            # Now get his committee assignments
                            member_id = grassley_member['id']
                            async with session.get(f"https://congressional-data-api-v2-1066017671167.us-central1.run.app/api/v1/members/{member_id}/committees") as committee_response:
                                if committee_response.status == 200:
                                    committees = await committee_response.json()
                                    print(f"📋 Chuck Grassley's committees via API: {len(committees)}")
                                    
                                    for committee in committees:
                                        print(f"  - {committee.get('name', 'Unknown Committee')}")
                                        
                                    # Check if Judiciary is in the list
                                    judiciary_found = any('Judiciary' in committee.get('name', '') for committee in committees)
                                    
                                    if judiciary_found:
                                        print("✅ Senate Judiciary Committee found in API response")
                                    else:
                                        print("❌ Senate Judiciary Committee not found in API response")
                                        
                                        # Let's check what the API is actually returning
                                        print("\nAPI Debug Info:")
                                        print(f"Response status: {committee_response.status}")
                                        print(f"Response content: {committees}")
                                        
                                else:
                                    print(f"❌ API committee request failed: {committee_response.status}")
                                    
                        else:
                            print("❌ Grassley not found via API")
                    else:
                        print(f"❌ API member search failed: {response.status}")
    
    finally:
        conn.close()

if __name__ == "__main__":
    asyncio.run(verify_assignment())