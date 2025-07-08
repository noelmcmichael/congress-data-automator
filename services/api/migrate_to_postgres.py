"""
Database migration script to move from SQLite to PostgreSQL.
"""

import os
import sys
import sqlite3
import asyncio
from pathlib import Path
from typing import Dict, Any, List

# Add the api module to the path
sys.path.insert(0, str(Path(__file__).parent))

from api.core.config import settings
from api.core.logging import logger
from api.database.connection import db_manager
from api.models.database import Member, Committee, Hearing, CommitteeMembership, Witness, HearingDocument
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class DatabaseMigrator:
    """Handles migration from SQLite to PostgreSQL."""
    
    def __init__(self, sqlite_path: str = "test.db"):
        self.sqlite_path = sqlite_path
        self.migration_stats = {
            "members": 0,
            "committees": 0,
            "hearings": 0,
            "committee_memberships": 0,
            "witnesses": 0,
            "hearing_documents": 0,
        }
    
    def export_sqlite_data(self) -> Dict[str, List[Dict[str, Any]]]:
        """Export data from SQLite database."""
        if not os.path.exists(self.sqlite_path):
            logger.warning(f"SQLite database not found at {self.sqlite_path}")
            return {}
        
        conn = sqlite3.connect(self.sqlite_path)
        conn.row_factory = sqlite3.Row  # Enable dict-like access
        
        data = {}
        
        try:
            # Export members
            cursor = conn.execute("SELECT * FROM members")
            data["members"] = [dict(row) for row in cursor.fetchall()]
            logger.info(f"Exported {len(data['members'])} members")
            
            # Export committees
            cursor = conn.execute("SELECT * FROM committees")
            data["committees"] = [dict(row) for row in cursor.fetchall()]
            logger.info(f"Exported {len(data['committees'])} committees")
            
            # Export hearings
            cursor = conn.execute("SELECT * FROM hearings")
            data["hearings"] = [dict(row) for row in cursor.fetchall()]
            logger.info(f"Exported {len(data['hearings'])} hearings")
            
            # Export committee memberships
            cursor = conn.execute("SELECT * FROM committee_memberships")
            data["committee_memberships"] = [dict(row) for row in cursor.fetchall()]
            logger.info(f"Exported {len(data['committee_memberships'])} committee memberships")
            
            # Export witnesses
            try:
                cursor = conn.execute("SELECT * FROM witnesses")
                data["witnesses"] = [dict(row) for row in cursor.fetchall()]
                logger.info(f"Exported {len(data['witnesses'])} witnesses")
            except sqlite3.OperationalError:
                logger.warning("Witnesses table not found in SQLite")
                data["witnesses"] = []
            
            # Export hearing documents
            try:
                cursor = conn.execute("SELECT * FROM hearing_documents")
                data["hearing_documents"] = [dict(row) for row in cursor.fetchall()]
                logger.info(f"Exported {len(data['hearing_documents'])} hearing documents")
            except sqlite3.OperationalError:
                logger.warning("Hearing documents table not found in SQLite")
                data["hearing_documents"] = []
            
        except Exception as e:
            logger.error(f"Error exporting SQLite data: {e}")
            raise
        finally:
            conn.close()
        
        return data
    
    async def import_to_postgres(self, data: Dict[str, List[Dict[str, Any]]]):
        """Import data to PostgreSQL database."""
        async with db_manager.get_session() as session:
            try:
                # Import members
                await self._import_members(session, data.get("members", []))
                
                # Import committees
                await self._import_committees(session, data.get("committees", []))
                
                # Import hearings
                await self._import_hearings(session, data.get("hearings", []))
                
                # Import committee memberships
                await self._import_committee_memberships(session, data.get("committee_memberships", []))
                
                # Import witnesses
                await self._import_witnesses(session, data.get("witnesses", []))
                
                # Import hearing documents
                await self._import_hearing_documents(session, data.get("hearing_documents", []))
                
                await session.commit()
                logger.info("All data imported successfully")
                
            except Exception as e:
                await session.rollback()
                logger.error(f"Error importing data to PostgreSQL: {e}")
                raise
    
    async def _import_members(self, session: AsyncSession, members: List[Dict[str, Any]]):
        """Import members to PostgreSQL."""
        for member_data in members:
            # Check if member already exists
            result = await session.execute(
                text("SELECT id FROM members WHERE bioguide_id = :bioguide_id"),
                {"bioguide_id": member_data.get("bioguide_id")}
            )
            if result.scalar():
                continue
            
            # Create member
            member = Member(
                bioguide_id=member_data.get("bioguide_id"),
                name=member_data.get("name"),
                first_name=member_data.get("first_name"),
                last_name=member_data.get("last_name"),
                chamber=member_data.get("chamber"),
                state=member_data.get("state"),
                district=member_data.get("district"),
                party=member_data.get("party"),
                title=member_data.get("title"),
                phone=member_data.get("phone"),
                office=member_data.get("office"),
                photo_url=member_data.get("photo_url"),
                website_url=member_data.get("website_url"),
                contact_url=member_data.get("contact_url"),
                is_current=member_data.get("is_current", True),
                term_start=member_data.get("term_start"),
                term_end=member_data.get("term_end"),
                term_class=member_data.get("term_class"),
                next_election=member_data.get("next_election"),
                voting_status=member_data.get("voting_status"),
                leadership_role=member_data.get("leadership_role"),
                created_at=member_data.get("created_at"),
                updated_at=member_data.get("updated_at"),
            )
            session.add(member)
            self.migration_stats["members"] += 1
        
        await session.flush()
        logger.info(f"Imported {self.migration_stats['members']} members")
    
    async def _import_committees(self, session: AsyncSession, committees: List[Dict[str, Any]]):
        """Import committees to PostgreSQL."""
        for committee_data in committees:
            # Check if committee already exists
            result = await session.execute(
                text("SELECT id FROM committees WHERE code = :code"),
                {"code": committee_data.get("code")}
            )
            if result.scalar():
                continue
            
            # Create committee
            committee = Committee(
                code=committee_data.get("code"),
                name=committee_data.get("name"),
                chamber=committee_data.get("chamber"),
                committee_type=committee_data.get("committee_type"),
                parent_committee_id=committee_data.get("parent_committee_id"),
                is_active=committee_data.get("is_active", True),
                website_url=committee_data.get("website_url"),
                hearings_url=committee_data.get("hearings_url"),
                members_url=committee_data.get("members_url"),
                official_website_url=committee_data.get("official_website_url"),
                jurisdiction=committee_data.get("jurisdiction"),
                created_at=committee_data.get("created_at"),
                updated_at=committee_data.get("updated_at"),
            )
            session.add(committee)
            self.migration_stats["committees"] += 1
        
        await session.flush()
        logger.info(f"Imported {self.migration_stats['committees']} committees")
    
    async def _import_hearings(self, session: AsyncSession, hearings: List[Dict[str, Any]]):
        """Import hearings to PostgreSQL."""
        for hearing_data in hearings:
            # Check if hearing already exists
            result = await session.execute(
                text("SELECT id FROM hearings WHERE title = :title AND date = :date"),
                {"title": hearing_data.get("title"), "date": hearing_data.get("date")}
            )
            if result.scalar():
                continue
            
            # Create hearing
            hearing = Hearing(
                title=hearing_data.get("title"),
                description=hearing_data.get("description"),
                date=hearing_data.get("date"),
                time=hearing_data.get("time"),
                location=hearing_data.get("location"),
                room=hearing_data.get("room"),
                status=hearing_data.get("status"),
                video_url=hearing_data.get("video_url"),
                transcript_url=hearing_data.get("transcript_url"),
                committee_id=hearing_data.get("committee_id"),
                created_at=hearing_data.get("created_at"),
                updated_at=hearing_data.get("updated_at"),
            )
            session.add(hearing)
            self.migration_stats["hearings"] += 1
        
        await session.flush()
        logger.info(f"Imported {self.migration_stats['hearings']} hearings")
    
    async def _import_committee_memberships(self, session: AsyncSession, memberships: List[Dict[str, Any]]):
        """Import committee memberships to PostgreSQL."""
        for membership_data in memberships:
            # Check if membership already exists
            result = await session.execute(
                text("SELECT id FROM committee_memberships WHERE member_id = :member_id AND committee_id = :committee_id"),
                {"member_id": membership_data.get("member_id"), "committee_id": membership_data.get("committee_id")}
            )
            if result.scalar():
                continue
            
            # Create membership
            membership = CommitteeMembership(
                member_id=membership_data.get("member_id"),
                committee_id=membership_data.get("committee_id"),
                position=membership_data.get("position"),
                is_current=membership_data.get("is_current", True),
                start_date=membership_data.get("start_date"),
                end_date=membership_data.get("end_date"),
                created_at=membership_data.get("created_at"),
                updated_at=membership_data.get("updated_at"),
            )
            session.add(membership)
            self.migration_stats["committee_memberships"] += 1
        
        await session.flush()
        logger.info(f"Imported {self.migration_stats['committee_memberships']} committee memberships")
    
    async def _import_witnesses(self, session: AsyncSession, witnesses: List[Dict[str, Any]]):
        """Import witnesses to PostgreSQL."""
        for witness_data in witnesses:
            # Check if witness already exists
            result = await session.execute(
                text("SELECT id FROM witnesses WHERE name = :name AND hearing_id = :hearing_id"),
                {"name": witness_data.get("name"), "hearing_id": witness_data.get("hearing_id")}
            )
            if result.scalar():
                continue
            
            # Create witness
            witness = Witness(
                name=witness_data.get("name"),
                title=witness_data.get("title"),
                organization=witness_data.get("organization"),
                testimony_url=witness_data.get("testimony_url"),
                bio_url=witness_data.get("bio_url"),
                hearing_id=witness_data.get("hearing_id"),
                created_at=witness_data.get("created_at"),
                updated_at=witness_data.get("updated_at"),
            )
            session.add(witness)
            self.migration_stats["witnesses"] += 1
        
        await session.flush()
        logger.info(f"Imported {self.migration_stats['witnesses']} witnesses")
    
    async def _import_hearing_documents(self, session: AsyncSession, documents: List[Dict[str, Any]]):
        """Import hearing documents to PostgreSQL."""
        for document_data in documents:
            # Check if document already exists
            result = await session.execute(
                text("SELECT id FROM hearing_documents WHERE title = :title AND hearing_id = :hearing_id"),
                {"title": document_data.get("title"), "hearing_id": document_data.get("hearing_id")}
            )
            if result.scalar():
                continue
            
            # Create document
            document = HearingDocument(
                title=document_data.get("title"),
                description=document_data.get("description"),
                document_type=document_data.get("document_type"),
                url=document_data.get("url"),
                hearing_id=document_data.get("hearing_id"),
                created_at=document_data.get("created_at"),
                updated_at=document_data.get("updated_at"),
            )
            session.add(document)
            self.migration_stats["hearing_documents"] += 1
        
        await session.flush()
        logger.info(f"Imported {self.migration_stats['hearing_documents']} hearing documents")
    
    async def create_indexes(self):
        """Create database indexes for performance."""
        async with db_manager.get_session() as session:
            indexes = [
                "CREATE INDEX IF NOT EXISTS idx_members_bioguide_id ON members(bioguide_id)",
                "CREATE INDEX IF NOT EXISTS idx_members_chamber ON members(chamber)",
                "CREATE INDEX IF NOT EXISTS idx_members_state ON members(state)",
                "CREATE INDEX IF NOT EXISTS idx_members_party ON members(party)",
                "CREATE INDEX IF NOT EXISTS idx_members_is_current ON members(is_current)",
                "CREATE INDEX IF NOT EXISTS idx_committees_code ON committees(code)",
                "CREATE INDEX IF NOT EXISTS idx_committees_chamber ON committees(chamber)",
                "CREATE INDEX IF NOT EXISTS idx_committees_is_active ON committees(is_active)",
                "CREATE INDEX IF NOT EXISTS idx_hearings_date ON hearings(date)",
                "CREATE INDEX IF NOT EXISTS idx_hearings_committee_id ON hearings(committee_id)",
                "CREATE INDEX IF NOT EXISTS idx_hearings_status ON hearings(status)",
                "CREATE INDEX IF NOT EXISTS idx_committee_memberships_member_id ON committee_memberships(member_id)",
                "CREATE INDEX IF NOT EXISTS idx_committee_memberships_committee_id ON committee_memberships(committee_id)",
                "CREATE INDEX IF NOT EXISTS idx_committee_memberships_is_current ON committee_memberships(is_current)",
                "CREATE INDEX IF NOT EXISTS idx_witnesses_hearing_id ON witnesses(hearing_id)",
                "CREATE INDEX IF NOT EXISTS idx_hearing_documents_hearing_id ON hearing_documents(hearing_id)",
            ]
            
            for index_sql in indexes:
                try:
                    await session.execute(text(index_sql))
                    logger.info(f"Created index: {index_sql}")
                except Exception as e:
                    logger.warning(f"Failed to create index: {e}")
            
            await session.commit()
            logger.info("Database indexes created successfully")
    
    async def validate_migration(self):
        """Validate the migration by checking data integrity."""
        async with db_manager.get_session() as session:
            # Check counts
            for table in self.migration_stats:
                result = await session.execute(text(f"SELECT COUNT(*) FROM {table}"))
                count = result.scalar()
                expected = self.migration_stats[table]
                
                if count >= expected:
                    logger.info(f"✓ {table}: {count} records (expected {expected})")
                else:
                    logger.error(f"✗ {table}: {count} records (expected {expected})")
            
            # Check foreign key relationships
            result = await session.execute(text("""
                SELECT COUNT(*) FROM committee_memberships cm
                LEFT JOIN members m ON cm.member_id = m.id
                LEFT JOIN committees c ON cm.committee_id = c.id
                WHERE m.id IS NULL OR c.id IS NULL
            """))
            orphaned = result.scalar()
            
            if orphaned == 0:
                logger.info("✓ No orphaned committee memberships")
            else:
                logger.error(f"✗ Found {orphaned} orphaned committee memberships")
            
            logger.info("Migration validation completed")
    
    async def run_migration(self):
        """Run the complete migration process."""
        logger.info("Starting database migration from SQLite to PostgreSQL")
        
        # Initialize PostgreSQL database
        db_manager.initialize()
        db_manager.create_tables()
        
        # Export data from SQLite
        logger.info("Exporting data from SQLite...")
        data = self.export_sqlite_data()
        
        if not data:
            logger.info("No data to migrate")
            return
        
        # Import data to PostgreSQL
        logger.info("Importing data to PostgreSQL...")
        await self.import_to_postgres(data)
        
        # Create indexes
        logger.info("Creating database indexes...")
        await self.create_indexes()
        
        # Validate migration
        logger.info("Validating migration...")
        await self.validate_migration()
        
        logger.info("Database migration completed successfully!")
        logger.info(f"Migration statistics: {self.migration_stats}")


async def main():
    """Main migration function."""
    migrator = DatabaseMigrator()
    await migrator.run_migration()


if __name__ == "__main__":
    asyncio.run(main())