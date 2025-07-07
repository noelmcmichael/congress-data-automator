#!/usr/bin/env python3
"""
Execute Immediate Database Fixes

This script executes the immediate database fixes for:
1. Fix senator name fields (NULL/Unknown -> proper names)
2. Add Chuck Grassley to Senate Judiciary Committee
3. Verify fixes work correctly
"""

import psycopg2
import json
import logging
import asyncio
import aiohttp
from datetime import datetime
from typing import Dict, List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Database connection via Cloud SQL Proxy
DATABASE_CONFIG = {
    'host': 'localhost',
    'port': 5433,
    'database': 'congress_data',
    'user': 'postgres',
    'password': 'mDf3S9ZnBpQqJvGsY1'
}

# Production API base URL
API_BASE = "https://congressional-data-api-v2-1066017671167.us-central1.run.app"

class ImmediateFixer:
    """Execute immediate database fixes"""
    
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.session = None
        
    async def __aenter__(self):
        # Database connection
        self.conn = psycopg2.connect(**DATABASE_CONFIG)
        self.cursor = self.conn.cursor()
        
        # HTTP session
        self.session = aiohttp.ClientSession()
        
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        if self.session:
            await self.session.close()
    
    def step_1_verify_database_connection(self):
        """Step 1: Verify database connection and current state"""
        logger.info("🔍 Step 1: Verifying database connection...")
        
        try:
            # Test basic connection
            self.cursor.execute("SELECT version();")
            version = self.cursor.fetchone()
            logger.info(f"✅ Database connected: {version[0]}")
            
            # Check member count
            self.cursor.execute("SELECT COUNT(*) FROM members;")
            member_count = self.cursor.fetchone()[0]
            logger.info(f"✅ Total members in database: {member_count}")
            
            # Check if name column exists
            self.cursor.execute("""
                SELECT column_name FROM information_schema.columns 
                WHERE table_name = 'members' AND column_name = 'name';
            """)
            name_column_exists = self.cursor.fetchone()
            if name_column_exists:
                logger.info("✅ Name column exists")
                # Check senators with NULL names
                self.cursor.execute("SELECT COUNT(*) FROM members WHERE (name IS NULL OR name = '') AND chamber = 'Senate';")
                null_name_count = self.cursor.fetchone()[0]
                logger.info(f"⚠️  Senators with NULL/empty names: {null_name_count}")
            else:
                logger.info("⚠️  Name column does not exist - needs to be added")
            
            # Check Chuck Grassley specifically
            self.cursor.execute("SELECT id, first_name, last_name, bioguide_id FROM members WHERE bioguide_id = 'G000386';")
            grassley = self.cursor.fetchone()
            if grassley:
                logger.info(f"✅ Chuck Grassley found: ID={grassley[0]}, {grassley[1]} {grassley[2]}, bioguide={grassley[3]}")
            else:
                logger.error("❌ Chuck Grassley not found in database")
                
            # Check Senate Judiciary Committee
            self.cursor.execute("SELECT id, name FROM committees WHERE name LIKE '%Judiciary%' AND chamber = 'Senate';")
            judiciary = self.cursor.fetchone()
            if judiciary:
                logger.info(f"✅ Senate Judiciary Committee found: ID={judiciary[0]}, name='{judiciary[1]}'")
            else:
                logger.error("❌ Senate Judiciary Committee not found")
                
            return True
            
        except Exception as e:
            logger.error(f"❌ Database connection failed: {str(e)}")
            return False
    
    def step_2_add_name_column(self):
        """Step 2: Add name column to members table and populate it"""
        logger.info("🔧 Step 2: Adding name column to members table...")
        
        try:
            # Check if name column already exists
            self.cursor.execute("""
                SELECT column_name FROM information_schema.columns 
                WHERE table_name = 'members' AND column_name = 'name';
            """)
            name_column_exists = self.cursor.fetchone()
            
            if not name_column_exists:
                # Add name column
                self.cursor.execute("""
                    ALTER TABLE members ADD COLUMN name VARCHAR(255);
                """)
                logger.info("✅ Added name column to members table")
            else:
                logger.info("✅ Name column already exists")
            
            # Populate name column with first_name + last_name
            self.cursor.execute("""
                UPDATE members 
                SET name = CONCAT(first_name, ' ', last_name)
                WHERE name IS NULL OR name = '';
            """)
            
            # Get count of updated rows
            self.cursor.execute("SELECT COUNT(*) FROM members WHERE name IS NOT NULL;")
            populated_count = self.cursor.fetchone()[0]
            
            # Commit changes
            self.conn.commit()
            logger.info(f"✅ Populated name field for {populated_count} members")
            
            return populated_count
            
        except Exception as e:
            logger.error(f"❌ Failed to add/populate name column: {str(e)}")
            self.conn.rollback()
            return 0
    
    def step_3_add_grassley_to_judiciary(self):
        """Step 3: Add Chuck Grassley to Senate Judiciary Committee"""
        logger.info("🔧 Step 3: Adding Chuck Grassley to Senate Judiciary Committee...")
        
        try:
            # Get Chuck Grassley's ID
            self.cursor.execute("SELECT id FROM members WHERE bioguide_id = 'G000386';")
            grassley_result = self.cursor.fetchone()
            if not grassley_result:
                logger.error("❌ Chuck Grassley not found")
                return False
            
            grassley_id = grassley_result[0]
            
            # Get Senate Judiciary Committee ID
            self.cursor.execute("SELECT id FROM committees WHERE name LIKE '%Judiciary%' AND chamber = 'Senate';")
            judiciary_result = self.cursor.fetchone()
            if not judiciary_result:
                logger.error("❌ Senate Judiciary Committee not found")
                return False
            
            judiciary_id = judiciary_result[0]
            
            # Check if relationship already exists
            self.cursor.execute("""
                SELECT id FROM committee_memberships 
                WHERE member_id = %s AND committee_id = %s;
            """, (grassley_id, judiciary_id))
            
            existing = self.cursor.fetchone()
            if existing:
                logger.info("✅ Chuck Grassley already on Senate Judiciary Committee")
                return True
            
            # Add the relationship
            self.cursor.execute("""
                INSERT INTO committee_memberships (member_id, committee_id, position)
                VALUES (%s, %s, 'Ranking Member');
            """, (grassley_id, judiciary_id))
            
            # Commit the change
            self.conn.commit()
            logger.info("✅ Successfully added Chuck Grassley to Senate Judiciary Committee")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to add Grassley to Judiciary Committee: {str(e)}")
            self.conn.rollback()
            return False
    
    async def step_4_verify_search_functionality(self):
        """Step 4: Verify search functionality works"""
        logger.info("🔍 Step 4: Verifying search functionality...")
        
        try:
            # Test search for Chuck Grassley
            async with self.session.get(f"{API_BASE}/api/v1/members?search=Grassley") as response:
                if response.status == 200:
                    results = await response.json()
                    grassley_found = any(
                        member.get('bioguide_id') == 'G000386' 
                        for member in results
                    )
                    
                    if grassley_found:
                        logger.info("✅ Chuck Grassley now searchable via API")
                        return True
                    else:
                        logger.error("❌ Chuck Grassley not found in search results")
                        return False
                else:
                    logger.error(f"❌ Search API failed: {response.status}")
                    return False
                    
        except Exception as e:
            logger.error(f"❌ Search verification failed: {str(e)}")
            return False
    
    async def step_5_verify_committee_assignment(self):
        """Step 5: Verify committee assignment is visible"""
        logger.info("🔍 Step 5: Verifying committee assignment visibility...")
        
        try:
            # Get Chuck Grassley's ID from database
            self.cursor.execute("SELECT id FROM members WHERE bioguide_id = 'G000386';")
            grassley_result = self.cursor.fetchone()
            if not grassley_result:
                logger.error("❌ Chuck Grassley not found")
                return False
            
            grassley_id = grassley_result[0]
            
            # Check committee assignments via API
            async with self.session.get(f"{API_BASE}/api/v1/members/{grassley_id}/committees") as response:
                if response.status == 200:
                    committees = await response.json()
                    
                    # Look for Senate Judiciary Committee
                    judiciary_found = any(
                        'Judiciary' in committee.get('name', '')
                        for committee in committees
                    )
                    
                    if judiciary_found:
                        logger.info("✅ Chuck Grassley's committee assignments visible via API")
                        return True
                    else:
                        logger.error("❌ Senate Judiciary Committee not found in Grassley's assignments")
                        return False
                else:
                    logger.error(f"❌ Committee API failed: {response.status}")
                    return False
                    
        except Exception as e:
            logger.error(f"❌ Committee assignment verification failed: {str(e)}")
            return False
    
    async def execute_phase_1(self):
        """Execute Phase 1: Immediate Database Fixes"""
        logger.info("🚀 Starting Phase 1: Immediate Database Fixes")
        
        results = {
            'step_1_database_connection': False,
            'step_2_name_fixes': 0,
            'step_3_grassley_committee': False,
            'step_4_search_verification': False,
            'step_5_committee_verification': False
        }
        
        # Step 1: Verify database connection
        results['step_1_database_connection'] = self.step_1_verify_database_connection()
        
        if not results['step_1_database_connection']:
            logger.error("❌ Database connection failed - aborting")
            return results
        
        # Step 2: Add name column and populate it
        results['step_2_name_fixes'] = self.step_2_add_name_column()
        
        # Step 3: Add Grassley to Judiciary Committee
        results['step_3_grassley_committee'] = self.step_3_add_grassley_to_judiciary()
        
        # Step 4: Verify search functionality
        results['step_4_search_verification'] = await self.step_4_verify_search_functionality()
        
        # Step 5: Verify committee assignment
        results['step_5_committee_verification'] = await self.step_5_verify_committee_assignment()
        
        return results
    
    def generate_report(self, results):
        """Generate final report"""
        logger.info("📊 Generating final report...")
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'phase_1_results': results,
            'success_rate': 0,
            'summary': []
        }
        
        # Calculate success rate
        total_steps = 5
        successful_steps = sum([
            1 if results['step_1_database_connection'] else 0,
            1 if results['step_2_name_fixes'] > 0 else 0,
            1 if results['step_3_grassley_committee'] else 0,
            1 if results['step_4_search_verification'] else 0,
            1 if results['step_5_committee_verification'] else 0
        ])
        
        report['success_rate'] = (successful_steps / total_steps) * 100
        
        # Generate summary
        if results['step_1_database_connection']:
            report['summary'].append("✅ Database connection established")
        else:
            report['summary'].append("❌ Database connection failed")
        
        if results['step_2_name_fixes'] > 0:
            report['summary'].append(f"✅ Fixed {results['step_2_name_fixes']} member names")
        else:
            report['summary'].append("❌ No member names fixed")
        
        if results['step_3_grassley_committee']:
            report['summary'].append("✅ Chuck Grassley added to Senate Judiciary Committee")
        else:
            report['summary'].append("❌ Failed to add Grassley to committee")
        
        if results['step_4_search_verification']:
            report['summary'].append("✅ Search functionality verified")
        else:
            report['summary'].append("❌ Search functionality failed")
        
        if results['step_5_committee_verification']:
            report['summary'].append("✅ Committee assignment visible")
        else:
            report['summary'].append("❌ Committee assignment not visible")
        
        # Save report
        with open('immediate_fixes_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"📊 Phase 1 Success Rate: {report['success_rate']:.1f}%")
        for item in report['summary']:
            logger.info(f"  {item}")
        
        return report

async def main():
    """Main execution function"""
    logger.info("🚀 Starting Immediate Database Fixes")
    
    async with ImmediateFixer() as fixer:
        results = await fixer.execute_phase_1()
        report = fixer.generate_report(results)
        
        logger.info("🎉 Phase 1 Complete!")
        
        if report['success_rate'] >= 80:
            logger.info("✅ Phase 1 successful - ready for Phase 2")
        else:
            logger.warning("⚠️  Phase 1 had issues - review before proceeding")
        
        return report

if __name__ == "__main__":
    asyncio.run(main())