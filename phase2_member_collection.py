#!/usr/bin/env python3
"""
Phase 2: Complete Member Collection Implementation

Expands Congressional member database from 50 → 535 members using optimized
Congress.gov API data collection with batching and rate limiting.

Implementation Roadmap: docs/progress/phase2_member_collection_plan.md
"""

import json
import time
import asyncio
import aiohttp
import os
import sys
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
import logging
import psycopg2
from psycopg2.extras import RealDictCursor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('phase2_collection.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class MemberRecord:
    """Standardized member record structure"""
    bioguide_id: str
    first_name: str
    last_name: str
    full_name: str
    chamber: str
    state: str
    party: str
    district: Optional[str] = None
    wikipedia_url: Optional[str] = None
    congress_url: Optional[str] = None
    
class CongressAPIClient:
    """Optimized Congress.gov API client with rate limiting"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.congress.gov/v3"
        self.rate_limit_delay = 0.7  # seconds between requests
        self.max_concurrent = 3
        self.batch_size = 15
        
    async def get_current_members(self, session: aiohttp.ClientSession) -> List[Dict]:
        """Get all current Congressional members"""
        members = []
        url = f"{self.base_url}/member"
        
        # Start with first batch to get pagination info
        params = {
            'api_key': self.api_key, 
            'limit': 250, 
            'currentMember': 'true'
        }
        
        try:
            await asyncio.sleep(self.rate_limit_delay)
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    first_batch = data.get('members', [])
                    members.extend(first_batch)
                    
                    # Get pagination info
                    pagination = data.get('pagination', {})
                    total_count = pagination.get('count', 0)
                    
                    logger.info(f"Found {total_count} total members, got {len(first_batch)} in first batch")
                    
                    # Get remaining batches if needed
                    if total_count > len(first_batch):
                        remaining_batches = await self._get_remaining_members(session, total_count, len(first_batch))
                        members.extend(remaining_batches)
                    
                    logger.info(f"Collected {len(members)} total members")
                    return members
                else:
                    logger.error(f"API request failed: {response.status}")
                    return []
        except Exception as e:
            logger.error(f"Error fetching members: {e}")
            return []
    
    async def _get_remaining_members(self, session: aiohttp.ClientSession, 
                                   total_count: int, already_fetched: int) -> List[Dict]:
        """Get remaining members in batches"""
        remaining_members = []
        offset = already_fetched
        
        while offset < total_count:
            params = {
                'api_key': self.api_key,
                'limit': 250,
                'currentMember': 'true',
                'offset': offset
            }
            
            try:
                await asyncio.sleep(self.rate_limit_delay)
                async with session.get(f"{self.base_url}/member", params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        batch_members = data.get('members', [])
                        remaining_members.extend(batch_members)
                        offset += len(batch_members)
                        logger.info(f"Fetched batch: {len(batch_members)} members (total: {len(remaining_members) + already_fetched})")
                        
                        if len(batch_members) == 0:
                            break
                    else:
                        logger.error(f"Batch request failed: {response.status}")
                        break
            except Exception as e:
                logger.error(f"Error fetching batch at offset {offset}: {e}")
                break
        
        return remaining_members

class MemberProcessor:
    """Process and standardize member data"""
    
    # State name to abbreviation mapping
    STATE_MAPPING = {
        'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR',
        'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE',
        'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID',
        'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS',
        'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
        'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS',
        'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV',
        'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY',
        'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK',
        'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
        'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT',
        'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV',
        'Wisconsin': 'WI', 'Wyoming': 'WY', 'District of Columbia': 'DC',
        'Puerto Rico': 'PR', 'Virgin Islands': 'VI', 'Guam': 'GU', 'American Samoa': 'AS',
        'Northern Mariana Islands': 'MP'
    }
    
    @staticmethod
    def process_congress_member(member_data: Dict) -> Optional[MemberRecord]:
        """Convert Congress.gov API response to MemberRecord"""
        try:
            # Extract basic info
            bioguide_id = member_data.get('bioguideId', '')
            
            # Parse name - Congress API returns "LastName, FirstName MiddleInitial" format
            name = member_data.get('name', '')
            name_parts = name.split(', ')
            if len(name_parts) >= 2:
                last_name = name_parts[0].strip()
                first_name = name_parts[1].strip()
            else:
                # Fallback parsing
                name_words = name.split()
                first_name = name_words[0] if name_words else ''
                last_name = ' '.join(name_words[1:]) if len(name_words) > 1 else ''
            
            full_name = f"{first_name} {last_name}".strip()
            
            # Determine chamber based on district presence
            district = member_data.get('district')
            chamber = "House" if district is not None else "Senate"
            
            # Get state and convert to abbreviation
            state_full = member_data.get('state', '')
            state = MemberProcessor.STATE_MAPPING.get(state_full, state_full[:2] if state_full else '')
            
            # Get party
            party = member_data.get('partyName', '')
            
            # Get district for House members (convert to string)
            district_str = str(district) if district is not None else None
            
            # Generate URLs
            wikipedia_url = None  # Will be populated later if needed
            congress_url = member_data.get('url') if member_data.get('url') else None
            
            return MemberRecord(
                bioguide_id=bioguide_id,
                first_name=first_name,
                last_name=last_name,
                full_name=full_name,
                chamber=chamber,
                state=state,
                party=party,
                district=district_str,
                wikipedia_url=wikipedia_url,
                congress_url=congress_url
            )
            
        except Exception as e:
            logger.error(f"Error processing member data: {e}")
            return None

class DatabaseManager:
    """Handle database operations for member data"""
    
    def __init__(self, database_url: str):
        self.database_url = database_url
        
    def get_current_member_count(self) -> int:
        """Get current member count from database"""
        try:
            with psycopg2.connect(self.database_url) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT COUNT(*) FROM members")
                    count = cur.fetchone()[0]
                    logger.info(f"Current database member count: {count}")
                    return count
        except Exception as e:
            logger.error(f"Error getting member count: {e}")
            return 0
    
    def backup_members_table(self) -> str:
        """Create backup of current members table"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_table = f"members_backup_{timestamp}"
        
        try:
            with psycopg2.connect(self.database_url) as conn:
                with conn.cursor() as cur:
                    cur.execute(f"""
                        CREATE TABLE {backup_table} AS 
                        SELECT * FROM members
                    """)
                    conn.commit()
                    logger.info(f"Created backup table: {backup_table}")
                    return backup_table
        except Exception as e:
            logger.error(f"Error creating backup: {e}")
            return ""
    
    def insert_members_batch(self, members: List[MemberRecord]) -> Tuple[int, int]:
        """Insert batch of members, return (inserted, updated) counts"""
        inserted_count = 0
        updated_count = 0
        
        try:
            with psycopg2.connect(self.database_url) as conn:
                with conn.cursor() as cur:
                    for member in members:
                        # Check if member exists
                        cur.execute(
                            "SELECT id FROM members WHERE bioguide_id = %s",
                            (member.bioguide_id,)
                        )
                        existing = cur.fetchone()
                        
                        if existing:
                            # Update existing member
                            cur.execute("""
                                UPDATE members SET
                                    first_name = %s,
                                    last_name = %s,
                                    chamber = %s,
                                    state = %s,
                                    party = %s,
                                    district = %s,
                                    website = %s,
                                    is_current = %s,
                                    congress_session = %s,
                                    updated_at = NOW()
                                WHERE bioguide_id = %s
                            """, (
                                member.first_name,
                                member.last_name,
                                member.chamber,
                                member.state,
                                member.party,
                                member.district,
                                member.congress_url,
                                True,  # is_current
                                119,   # congress_session
                                member.bioguide_id
                            ))
                            updated_count += 1
                        else:
                            # Insert new member
                            cur.execute("""
                                INSERT INTO members (
                                    bioguide_id, first_name, last_name, chamber, 
                                    state, party, district, website, is_current, 
                                    congress_session, created_at, updated_at
                                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
                            """, (
                                member.bioguide_id,
                                member.first_name,
                                member.last_name,
                                member.chamber,
                                member.state,
                                member.party,
                                member.district,
                                member.congress_url,
                                True,  # is_current
                                119    # congress_session
                            ))
                            inserted_count += 1
                    
                    conn.commit()
                    logger.info(f"Batch complete: {inserted_count} inserted, {updated_count} updated")
                    
        except Exception as e:
            logger.error(f"Error inserting member batch: {e}")
            
        return inserted_count, updated_count

class Phase2Coordinator:
    """Main coordinator for Phase 2 member collection"""
    
    def __init__(self):
        self.start_time = datetime.now()
        self.api_client = None
        self.db_manager = None
        self.results = {
            'start_time': self.start_time.isoformat(),
            'phase': 'Phase 2: Complete Member Collection',
            'status': 'initializing'
        }
    
    async def execute(self) -> Dict:
        """Execute complete Phase 2 member collection"""
        logger.info("=== Starting Phase 2: Complete Member Collection ===")
        
        try:
            # Step 2.1: Pre-Implementation Setup
            await self._setup()
            
            # Step 2.2: Member Data Collection  
            collected_members = await self._collect_members()
            
            # Step 2.3: Database Integration
            await self._integrate_database(collected_members)
            
            # Step 2.4: Production Deployment (API refresh)
            await self._deploy_to_production()
            
            # Step 2.5: Validation & Documentation
            await self._validate_results()
            
            self.results['status'] = 'completed'
            self.results['end_time'] = datetime.now().isoformat()
            logger.info("=== Phase 2 Complete ===")
            
        except Exception as e:
            self.results['status'] = 'failed'
            self.results['error'] = str(e)
            logger.error(f"Phase 2 failed: {e}")
            
        return self.results
    
    async def _setup(self):
        """Step 2.1: Pre-Implementation Setup"""
        logger.info("Step 2.1: Pre-Implementation Setup")
        
        # Get API key from environment
        api_key = os.getenv('CONGRESS_API_KEY')
        if not api_key:
            raise ValueError("CONGRESS_API_KEY environment variable required")
        
        # Initialize components
        self.api_client = CongressAPIClient(api_key)
        
        database_url = os.getenv('DATABASE_URL')
        if not database_url:
            raise ValueError("DATABASE_URL environment variable required")
        self.db_manager = DatabaseManager(database_url)
        
        # Create database backup
        backup_table = self.db_manager.backup_members_table()
        self.results['backup_table'] = backup_table
        
        # Record baseline
        current_count = self.db_manager.get_current_member_count()
        self.results['baseline_count'] = current_count
        
        logger.info(f"Setup complete. Current members: {current_count}")
    
    async def _collect_members(self) -> List[MemberRecord]:
        """Step 2.2: Member Data Collection"""
        logger.info("Step 2.2: Member Data Collection")
        
        collected_members = []
        
        async with aiohttp.ClientSession() as session:
            # Collect from Congress.gov API
            raw_members = await self.api_client.get_current_members(session)
            
            # Process collected data
            processor = MemberProcessor()
            for raw_member in raw_members:
                member = processor.process_congress_member(raw_member)
                if member:
                    collected_members.append(member)
        
        self.results['collected_count'] = len(collected_members)
        logger.info(f"Collected {len(collected_members)} member records")
        
        return collected_members
    
    async def _integrate_database(self, members: List[MemberRecord]):
        """Step 2.3: Database Integration"""
        logger.info("Step 2.3: Database Integration")
        
        # Process in batches
        batch_size = 50
        total_inserted = 0
        total_updated = 0
        
        for i in range(0, len(members), batch_size):
            batch = members[i:i + batch_size]
            inserted, updated = self.db_manager.insert_members_batch(batch)
            total_inserted += inserted
            total_updated += updated
            
            logger.info(f"Processed batch {i//batch_size + 1}: {len(batch)} members")
        
        self.results['inserted_count'] = total_inserted
        self.results['updated_count'] = total_updated
        
        # Get final count
        final_count = self.db_manager.get_current_member_count()
        self.results['final_count'] = final_count
        
        logger.info(f"Database integration complete. Final count: {final_count}")
    
    async def _deploy_to_production(self):
        """Step 2.4: Production Deployment"""
        logger.info("Step 2.4: Production Deployment")
        
        # Test API endpoint responsiveness
        import requests
        api_url = "https://congressional-data-api-v2-1066017671167.us-central1.run.app"
        
        try:
            # Test health endpoint
            health_response = requests.get(f"{api_url}/health", timeout=10)
            self.results['api_health'] = health_response.status_code == 200
            
            # Test members endpoint
            members_response = requests.get(f"{api_url}/api/v1/members", timeout=10)
            if members_response.status_code == 200:
                api_member_count = len(members_response.json())
                self.results['api_member_count'] = api_member_count
                logger.info(f"API responding with {api_member_count} members")
            else:
                logger.warning(f"API members endpoint returned {members_response.status_code}")
                
        except Exception as e:
            logger.error(f"Error testing production API: {e}")
            self.results['api_error'] = str(e)
    
    async def _validate_results(self):
        """Step 2.5: Validation & Documentation"""
        logger.info("Step 2.5: Validation & Documentation")
        
        # Calculate execution time
        end_time = datetime.now()
        execution_time = (end_time - self.start_time).total_seconds()
        self.results['execution_time_seconds'] = execution_time
        self.results['execution_time_formatted'] = f"{execution_time/60:.1f} minutes"
        
        # Validate target achievement
        final_count = self.results.get('final_count', 0)
        target_met = final_count >= 535
        self.results['target_met'] = target_met
        self.results['target_count'] = 535
        
        if target_met:
            logger.info(f"✅ Phase 2 target achieved: {final_count}/535 members")
        else:
            logger.warning(f"⚠️ Phase 2 target not fully met: {final_count}/535 members")
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = f"phase2_results_{timestamp}.json"
        with open(results_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        logger.info(f"Results saved to {results_file}")

async def main():
    """Main execution function"""
    coordinator = Phase2Coordinator()
    results = await coordinator.execute()
    
    print("\n" + "="*60)
    print("PHASE 2 EXECUTION SUMMARY")
    print("="*60)
    print(f"Status: {results.get('status', 'unknown')}")
    print(f"Baseline Count: {results.get('baseline_count', 0)}")
    print(f"Final Count: {results.get('final_count', 0)}")
    print(f"Inserted: {results.get('inserted_count', 0)}")
    print(f"Updated: {results.get('updated_count', 0)}")
    print(f"Execution Time: {results.get('execution_time_formatted', 'unknown')}")
    print(f"Target Met: {results.get('target_met', False)}")
    print("="*60)
    
    return results

if __name__ == "__main__":
    # Check for required environment variables
    required_env_vars = ['CONGRESS_API_KEY', 'DATABASE_URL']
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"Error: Missing required environment variables: {', '.join(missing_vars)}")
        sys.exit(1)
    
    # Run Phase 2
    asyncio.run(main())