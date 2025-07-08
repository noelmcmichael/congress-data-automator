#!/usr/bin/env python3
"""
Populate test database with real congressional data from production API.
This simulates the validated data that would come from the validation service.
"""

import asyncio
import httpx
from datetime import datetime
from sqlalchemy import text

from api.database.connection import DatabaseManager
from api.core.logging import logger


class TestDataPopulator:
    """Populate test database with real congressional data."""
    
    def __init__(self):
        self.db = DatabaseManager()
        self.db.initialize()
        self.production_api_base = "https://congressional-data-api-v2-1066017671167.us-central1.run.app/api/v1"
        
    async def populate_members(self, limit: int = 50):
        """Populate members table with real data."""
        logger.info(f"Populating members table with {limit} records...")
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Get members from production API
            response = await client.get(f"{self.production_api_base}/members?limit={limit}")
            response.raise_for_status()
            members = response.json()
            
            logger.info(f"Retrieved {len(members)} members from production API")
            
            # Insert members into test database
            with self.db.get_session() as session:
                for member in members:
                    # Convert production API format to database format
                    query = text("""
                        INSERT OR REPLACE INTO members (
                            id, bioguide_id, name, first_name, last_name, middle_name, nickname,
                            party, chamber, state, district, is_current, photo_url,
                            member_type, created_at, updated_at
                        ) VALUES (
                            :id, :bioguide_id, :name, :first_name, :last_name, :middle_name, :nickname,
                            :party, :chamber, :state, :district, :is_current, :photo_url,
                            :member_type, :created_at, :updated_at
                        )
                    """)
                    
                    # Create full name
                    full_name = f"{member['first_name']} {member['last_name']}"
                    if member.get('middle_name'):
                        full_name = f"{member['first_name']} {member['middle_name']} {member['last_name']}"
                    
                    session.execute(query, {
                        'id': member['id'],
                        'bioguide_id': member['bioguide_id'],
                        'name': full_name,
                        'first_name': member['first_name'],
                        'last_name': member['last_name'],
                        'middle_name': member.get('middle_name'),
                        'nickname': member.get('nickname'),
                        'party': member['party'],
                        'chamber': member['chamber'],
                        'state': member['state'],
                        'district': member.get('district'),
                        'is_current': member['is_current'],
                        'photo_url': member.get('official_photo_url'),
                        'member_type': 'representative' if member['chamber'] == 'House' else 'senator',
                        'created_at': member.get('created_at') or datetime.now().isoformat(),
                        'updated_at': member.get('updated_at') or datetime.now().isoformat()
                    })
                
                session.commit()
                logger.info(f"✅ Successfully populated {len(members)} members")
    
    async def populate_committees(self, limit: int = 30):
        """Populate committees table with real data."""
        logger.info(f"Populating committees table with {limit} records...")
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Get committees from production API
            response = await client.get(f"{self.production_api_base}/committees?limit={limit}")
            response.raise_for_status()
            committees = response.json()
            
            logger.info(f"Retrieved {len(committees)} committees from production API")
            
            # Insert committees into test database
            with self.db.get_session() as session:
                for committee in committees:
                    query = text("""
                        INSERT OR REPLACE INTO committees (
                            id, name, chamber, committee_type, description, jurisdiction,
                            is_current, created_at, updated_at, code
                        ) VALUES (
                            :id, :name, :chamber, :committee_type, :description, :jurisdiction,
                            :is_current, :created_at, :updated_at, :code
                        )
                    """)
                    
                    session.execute(query, {
                        'id': committee['id'],
                        'name': committee['name'],
                        'chamber': committee['chamber'],
                        'committee_type': committee.get('committee_type', 'standing'),
                        'description': committee.get('description'),
                        'jurisdiction': committee.get('jurisdiction'),
                        'is_current': committee.get('is_current', True),
                        'created_at': committee.get('created_at') or datetime.now().isoformat(),
                        'updated_at': committee.get('updated_at') or datetime.now().isoformat(),
                        'code': committee.get('code')
                    })
                
                session.commit()
                logger.info(f"✅ Successfully populated {len(committees)} committees")
    
    async def populate_hearings(self, limit: int = 20):
        """Populate hearings table with real data."""
        logger.info(f"Populating hearings table with {limit} records...")
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Get hearings from production API
            response = await client.get(f"{self.production_api_base}/hearings?limit={limit}")
            response.raise_for_status()
            hearings = response.json()
            
            logger.info(f"Retrieved {len(hearings)} hearings from production API")
            
            # Insert hearings into test database
            with self.db.get_session() as session:
                valid_hearings = 0
                for hearing in hearings:
                    # Skip hearings with invalid data
                    if not hearing.get('title') or not hearing.get('date'):
                        logger.warning(f"Skipping invalid hearing: {hearing.get('id')} - missing title or date")
                        continue
                    
                    query = text("""
                        INSERT OR REPLACE INTO hearings (
                            id, title, date, committee_id, location, room, status,
                            description, video_url, created_at, updated_at
                        ) VALUES (
                            :id, :title, :date, :committee_id, :location, :room, :status,
                            :description, :video_url, :created_at, :updated_at
                        )
                    """)
                    
                    session.execute(query, {
                        'id': hearing['id'],
                        'title': hearing['title'],
                        'date': hearing.get('date'),
                        'committee_id': hearing.get('committee_id'),
                        'location': hearing.get('location'),
                        'room': hearing.get('room'),
                        'status': hearing.get('status', 'Scheduled'),
                        'description': hearing.get('description'),
                        'video_url': hearing.get('video_url'),
                        'created_at': hearing.get('created_at') or datetime.now().isoformat(),
                        'updated_at': hearing.get('updated_at') or datetime.now().isoformat()
                    })
                    valid_hearings += 1
                
                session.commit()
                logger.info(f"✅ Successfully populated {valid_hearings} valid hearings (out of {len(hearings)} total)")
    
    async def populate_relationships(self):
        """Populate member-committee relationships."""
        logger.info("Populating member-committee relationships...")
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Get members with their committees
            response = await client.get(f"{self.production_api_base}/members?limit=20")
            response.raise_for_status()
            members = response.json()
            
            with self.db.get_session() as session:
                relationship_count = 0
                for member in members:
                    try:
                        # Get member's committee assignments
                        member_response = await client.get(f"{self.production_api_base}/members/{member['id']}/committees")
                        member_response.raise_for_status()
                        committees = member_response.json()
                        
                        for committee in committees:
                            query = text("""
                                INSERT OR REPLACE INTO committee_memberships (
                                    member_id, committee_id, position, is_current,
                                    created_at, updated_at
                                ) VALUES (
                                    :member_id, :committee_id, :position, :is_current,
                                    :created_at, :updated_at
                                )
                            """)
                            
                            session.execute(query, {
                                'member_id': member['id'],
                                'committee_id': committee['id'],
                                'position': committee.get('position', 'Member'),
                                'is_current': committee.get('is_current', True),
                                'created_at': datetime.now().isoformat(),
                                'updated_at': datetime.now().isoformat()
                            })
                            relationship_count += 1
                    
                    except Exception as e:
                        logger.warning(f"Failed to get committees for member {member['id']}: {e}")
                        continue
                
                session.commit()
                logger.info(f"✅ Successfully populated {relationship_count} member-committee relationships")
    
    async def populate_all(self):
        """Populate all tables with test data."""
        logger.info("🚀 Starting test data population...")
        
        try:
            await self.populate_members(limit=50)
            await self.populate_committees(limit=30)
            await self.populate_hearings(limit=20)
            await self.populate_relationships()
            
            # Summary
            with self.db.get_session() as session:
                member_count = session.execute(text("SELECT COUNT(*) FROM members")).scalar()
                committee_count = session.execute(text("SELECT COUNT(*) FROM committees")).scalar()
                hearing_count = session.execute(text("SELECT COUNT(*) FROM hearings")).scalar()
                relationship_count = session.execute(text("SELECT COUNT(*) FROM committee_memberships")).scalar()
                
                logger.info(f"""
                ✅ Test data population complete!
                
                📊 Database Summary:
                - Members: {member_count}
                - Committees: {committee_count}
                - Hearings: {hearing_count}
                - Relationships: {relationship_count}
                
                🎯 Ready for integration testing!
                """)
            
        except Exception as e:
            logger.error(f"❌ Failed to populate test data: {e}")
            raise


async def main():
    """Main function to populate test data."""
    populator = TestDataPopulator()
    await populator.populate_all()


if __name__ == "__main__":
    asyncio.run(main())