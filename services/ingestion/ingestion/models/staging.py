"""
Staging table models for the ingestion service.

These models define the structure for staging tables used to store
raw ingested data before validation and promotion to production.
"""

from datetime import datetime
from typing import Optional, Any, Dict
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base

from ..core.database import staging_metadata

# Create staging base with schema
StagingBase = declarative_base(metadata=staging_metadata)


class StagingMember(StagingBase):
    """
    Staging table for congressional members.
    
    Stores raw member data from Congress.gov API before validation
    and promotion to the production members table.
    """
    __tablename__ = "members"
    __table_args__ = {"schema": "staging"}
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Congress.gov identifiers
    bioguide_id = Column(String(10), index=True)
    congress_gov_id = Column(String(20), index=True)
    
    # Personal information
    first_name = Column(String(100))
    last_name = Column(String(100))
    middle_name = Column(String(100))
    suffix = Column(String(20))
    nickname = Column(String(100))
    
    # Political information
    party = Column(String(50))
    chamber = Column(String(20))  # House or Senate
    state = Column(String(2))
    district = Column(String(10))  # For House members
    
    # Service information
    term_start = Column(DateTime)
    term_end = Column(DateTime)
    is_current = Column(Boolean, default=True)
    
    # Contact information
    phone = Column(String(20))
    email = Column(String(255))
    website = Column(String(500))
    
    # Additional information
    birth_date = Column(DateTime)
    birth_state = Column(String(2))
    birth_city = Column(String(100))
    
    # Images and media
    photo_url = Column(String(500))
    
    # Raw data and metadata
    raw_data = Column(JSON)  # Store original API response
    collected_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime)
    
    # Data quality flags
    validation_status = Column(String(20), default='pending')  # pending, valid, invalid
    validation_errors = Column(JSON)
    
    def __repr__(self) -> str:
        return f"<StagingMember(bioguide_id='{self.bioguide_id}', name='{self.first_name} {self.last_name}')>"


class StagingCommittee(StagingBase):
    """
    Staging table for congressional committees.
    
    Stores raw committee data from Congress.gov API before validation
    and promotion to the production committees table.
    """
    __tablename__ = "committees"
    __table_args__ = {"schema": "staging"}
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Committee identifiers
    system_code = Column(String(10), index=True)
    name = Column(String(255))
    chamber = Column(String(20))  # House, Senate, Joint
    
    # Committee metadata
    committee_type = Column(String(50), default='Standing')
    is_subcommittee = Column(Boolean, default=False)
    parent_committee_code = Column(String(10))
    
    # Jurisdiction and description
    jurisdiction = Column(Text)
    
    # URLs and links
    congress_gov_url = Column(String(500))
    official_website_url = Column(String(500))
    hearings_url = Column(String(500))
    members_url = Column(String(500))
    
    # Raw data and metadata
    raw_data = Column(JSON)  # Store original API response
    collected_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime)
    
    # Data quality flags
    validation_status = Column(String(20), default='pending')
    validation_errors = Column(JSON)
    
    def __repr__(self) -> str:
        return f"<StagingCommittee(system_code='{self.system_code}', name='{self.name}')>"


class StagingHearing(StagingBase):
    """
    Staging table for congressional hearings.
    
    Stores raw hearing data from Congress.gov API and web scraping
    before validation and promotion to the production hearings table.
    """
    __tablename__ = "hearings"
    __table_args__ = {"schema": "staging"}
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Hearing basic information
    title = Column(String(500))
    description = Column(Text)
    
    # Scheduling information
    date_time = Column(DateTime)
    location = Column(String(500))
    room = Column(String(100))
    status = Column(String(50), default='scheduled')  # scheduled, completed, cancelled
    
    # Committee association
    committee_code = Column(String(10), index=True)
    
    # URLs and sources
    congress_gov_url = Column(String(500))
    source_url = Column(String(500))  # For web-scraped data
    
    # Media and documents
    video_url = Column(String(500))
    transcript_url = Column(String(500))
    
    # Raw data and metadata
    raw_data = Column(JSON)  # Store original response/scraped data
    collected_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime)
    source_type = Column(String(20))  # 'api' or 'scraping'
    
    # Data quality flags
    validation_status = Column(String(20), default='pending')
    validation_errors = Column(JSON)
    
    def __repr__(self) -> str:
        return f"<StagingHearing(title='{self.title[:50]}...', date='{self.date_time}')>"


class StagingWitness(StagingBase):
    """
    Staging table for hearing witnesses.
    
    Stores witness information collected from web scraping
    before validation and promotion to production.
    """
    __tablename__ = "witnesses"
    __table_args__ = {"schema": "staging"}
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Witness information
    name = Column(String(255))
    title = Column(String(255))
    organization = Column(String(255))
    
    # Hearing association
    hearing_id = Column(Integer)  # References staging hearing
    hearing_title = Column(String(500))  # For matching before ID assignment
    
    # Testimony information
    testimony_url = Column(String(500))
    biography_url = Column(String(500))
    
    # Raw data and metadata
    raw_data = Column(JSON)
    collected_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime)
    source_url = Column(String(500))
    
    # Data quality flags
    validation_status = Column(String(20), default='pending')
    validation_errors = Column(JSON)
    
    def __repr__(self) -> str:
        return f"<StagingWitness(name='{self.name}', organization='{self.organization}')>"


class StagingDocument(StagingBase):
    """
    Staging table for hearing documents.
    
    Stores document information collected from web scraping
    before validation and promotion to production.
    """
    __tablename__ = "documents"
    __table_args__ = {"schema": "staging"}
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Document information
    title = Column(String(500))
    document_type = Column(String(100))  # testimony, agenda, transcript, etc.
    document_url = Column(String(500))
    
    # Hearing association
    hearing_id = Column(Integer)  # References staging hearing
    hearing_title = Column(String(500))  # For matching before ID assignment
    
    # Document metadata
    file_size = Column(Integer)
    file_format = Column(String(20))  # pdf, doc, txt, etc.
    
    # Raw data and metadata
    raw_data = Column(JSON)
    collected_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime)
    source_url = Column(String(500))
    
    # Data quality flags
    validation_status = Column(String(20), default='pending')
    validation_errors = Column(JSON)
    
    def __repr__(self) -> str:
        return f"<StagingDocument(title='{self.title[:50]}...', type='{self.document_type}')>"


# Metadata for all staging tables
def get_staging_tables():
    """Get list of all staging table classes."""
    return [
        StagingMember,
        StagingCommittee,
        StagingHearing,
        StagingWitness,
        StagingDocument
    ]


def create_staging_tables(engine):
    """
    Create all staging tables.
    
    Args:
        engine: SQLAlchemy engine instance
    """
    try:
        # Create staging schema if it doesn't exist
        with engine.connect() as conn:
            conn.execute("CREATE SCHEMA IF NOT EXISTS staging")
            conn.commit()
        
        # Create all staging tables
        staging_metadata.create_all(bind=engine)
        
        return True
    except Exception as e:
        raise Exception(f"Failed to create staging tables: {str(e)}")


def drop_staging_tables(engine):
    """
    Drop all staging tables.
    
    Args:
        engine: SQLAlchemy engine instance
    """
    try:
        staging_metadata.drop_all(bind=engine)
        return True
    except Exception as e:
        raise Exception(f"Failed to drop staging tables: {str(e)}")