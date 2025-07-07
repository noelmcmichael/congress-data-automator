#!/usr/bin/env python3
"""
Fix Committee Assignment

Update the Chuck Grassley Senate Judiciary Committee assignment to set is_current = True
"""

import psycopg2
import asyncio
import aiohttp
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Database connection
DATABASE_CONFIG = {
    'host': 'localhost',
    'port': 5433,
    'database': 'congress_data',
    'user': 'postgres',
    'password': 'mDf3S9ZnBpQqJvGsY1'
}

# Production API base URL
API_BASE = "https://congressional-data-api-v2-1066017671167.us-central1.run.app"

async def fix_and_verify():
    """Fix the committee assignment and verify it works"""
    logger.info("🔧 Fixing Chuck Grassley's Senate Judiciary Committee assignment")
    
    # Fix the database
    conn = psycopg2.connect(**DATABASE_CONFIG)
    try:
        with conn.cursor() as cursor:
            # Update the committee membership to set is_current = True
            cursor.execute("""
                UPDATE committee_memberships 
                SET is_current = TRUE
                WHERE member_id = (SELECT id FROM members WHERE bioguide_id = 'G000386')
                AND committee_id = (SELECT id FROM committees WHERE name = 'Committee on the Judiciary' AND chamber = 'Senate');
            """)
            
            # Commit the change
            conn.commit()
            logger.info("✅ Updated committee membership to set is_current = True")
            
            # Verify the change
            cursor.execute("""
                SELECT cm.id, cm.position, cm.is_current, c.name, c.chamber
                FROM committee_memberships cm
                JOIN committees c ON cm.committee_id = c.id
                WHERE cm.member_id = (SELECT id FROM members WHERE bioguide_id = 'G000386')
                AND cm.committee_id = (SELECT id FROM committees WHERE name = 'Committee on the Judiciary' AND chamber = 'Senate');
            """)
            
            result = cursor.fetchone()
            if result:
                logger.info(f"✅ Verified: Assignment ID {result[0]}, Position: {result[1]}, Current: {result[2]}, Committee: {result[3]} ({result[4]})")
            else:
                logger.error("❌ Assignment not found after update")
                return False
                
    except Exception as e:
        logger.error(f"❌ Database update failed: {str(e)}")
        conn.rollback()
        return False
    finally:
        conn.close()
    
    # Wait a moment for any caching to clear
    await asyncio.sleep(2)
    
    # Verify via API
    logger.info("🔍 Verifying via API...")
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{API_BASE}/api/v1/members/510/committees") as response:
                if response.status == 200:
                    committees = await response.json()
                    logger.info(f"📋 Chuck Grassley's committees via API: {len(committees)}")
                    
                    judiciary_found = False
                    for committee in committees:
                        comm_name = committee.get('committee', {}).get('name', 'Unknown')
                        chamber = committee.get('committee', {}).get('chamber', 'Unknown')
                        position = committee.get('position', 'Member')
                        logger.info(f"  - {comm_name} ({chamber}) - {position}")
                        
                        if 'Judiciary' in comm_name and chamber == 'Senate':
                            judiciary_found = True
                    
                    if judiciary_found:
                        logger.info("🎉 SUCCESS: Senate Judiciary Committee now visible via API!")
                        return True
                    else:
                        logger.error("❌ Senate Judiciary Committee still not visible")
                        return False
                else:
                    logger.error(f"❌ API request failed: {response.status}")
                    return False
        except Exception as e:
            logger.error(f"❌ API verification failed: {str(e)}")
            return False

if __name__ == "__main__":
    result = asyncio.run(fix_and_verify())
    if result:
        print("🎉 100% SUCCESS ACHIEVED!")
    else:
        print("❌ Fix unsuccessful")