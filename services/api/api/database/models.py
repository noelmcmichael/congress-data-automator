"""SQLAlchemy models for congressional data."""

from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    Index,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Member(Base):
    """Member table model."""
    
    __tablename__ = "members"
    
    id = Column(Integer, primary_key=True, index=True)
    bioguide_id = Column(String(10), unique=True, index=True, nullable=False)
    name = Column(String(200), nullable=False, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False, index=True)
    middle_name = Column(String(100))
    suffix = Column(String(20))
    nickname = Column(String(100))
    
    # Political information
    party = Column(String(20), nullable=False, index=True)
    state = Column(String(2), nullable=False, index=True)
    district = Column(String(10), index=True)
    chamber = Column(String(20), nullable=False, index=True)
    member_type = Column(String(20), nullable=False)
    is_current = Column(Boolean, default=True, index=True)
    
    # Contact information
    photo_url = Column(String(500))
    website_url = Column(String(500))
    contact_form_url = Column(String(500))
    phone = Column(String(20))
    fax = Column(String(20))
    office = Column(String(200))
    
    # Additional information
    terms_served = Column(Integer)
    date_of_birth = Column(DateTime)
    gender = Column(String(10))
    
    # Timestamps
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    
    # Relationships
    committee_memberships = relationship(
        "CommitteeMembership",
        back_populates="member",
        cascade="all, delete-orphan"
    )
    
    # Indexes
    __table_args__ = (
        Index("idx_member_party_state", "party", "state"),
        Index("idx_member_chamber_current", "chamber", "is_current"),
        Index("idx_member_name_search", "name", "last_name", "first_name"),
    )


class Committee(Base):
    """Committee table model."""
    
    __tablename__ = "committees"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    code = Column(String(20), unique=True, index=True)
    chamber = Column(String(20), nullable=False, index=True)
    committee_type = Column(String(20), nullable=False, index=True)
    is_current = Column(Boolean, default=True, index=True)
    
    # Additional information
    description = Column(Text)
    website_url = Column(String(500))
    phone = Column(String(20))
    office = Column(String(200))
    jurisdiction = Column(Text)
    
    # Hierarchy
    parent_committee_id = Column(Integer, ForeignKey("committees.id"), index=True)
    parent_committee = relationship("Committee", remote_side=[id])
    subcommittees = relationship("Committee", cascade="all, delete-orphan")
    
    # Timestamps
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    
    # Relationships
    committee_memberships = relationship(
        "CommitteeMembership",
        back_populates="committee",
        cascade="all, delete-orphan"
    )
    hearings = relationship(
        "Hearing",
        back_populates="committee",
        cascade="all, delete-orphan"
    )
    
    # Indexes
    __table_args__ = (
        Index("idx_committee_chamber_type", "chamber", "committee_type"),
        Index("idx_committee_current", "is_current"),
        Index("idx_committee_name_search", "name"),
    )


class CommitteeMembership(Base):
    """Committee membership table model."""
    
    __tablename__ = "committee_memberships"
    
    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False, index=True)
    committee_id = Column(Integer, ForeignKey("committees.id"), nullable=False, index=True)
    
    # Membership details
    position = Column(String(100))
    is_chair = Column(Boolean, default=False, index=True)
    is_ranking_member = Column(Boolean, default=False, index=True)
    is_current = Column(Boolean, default=True, index=True)
    
    # Timestamps
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    
    # Relationships
    member = relationship("Member", back_populates="committee_memberships")
    committee = relationship("Committee", back_populates="committee_memberships")
    
    # Constraints
    __table_args__ = (
        UniqueConstraint("member_id", "committee_id", name="unique_member_committee"),
        Index("idx_membership_current", "is_current"),
        Index("idx_membership_leadership", "is_chair", "is_ranking_member"),
    )


class Hearing(Base):
    """Hearing table model."""
    
    __tablename__ = "hearings"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False, index=True)
    description = Column(Text)
    date = Column(DateTime, nullable=False, index=True)
    status = Column(String(20), nullable=False, index=True)
    
    # Committee relationship
    committee_id = Column(Integer, ForeignKey("committees.id"), nullable=False, index=True)
    
    # Location information
    location = Column(String(200))
    room = Column(String(100))
    
    # Media information
    video_url = Column(String(500))
    transcript_url = Column(String(500))
    meeting_type = Column(String(50))
    
    # Timestamps
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    
    # Relationships
    committee = relationship("Committee", back_populates="hearings")
    witnesses = relationship(
        "Witness",
        back_populates="hearing",
        cascade="all, delete-orphan"
    )
    documents = relationship(
        "HearingDocument",
        back_populates="hearing",
        cascade="all, delete-orphan"
    )
    
    # Indexes
    __table_args__ = (
        Index("idx_hearing_date_status", "date", "status"),
        Index("idx_hearing_committee_date", "committee_id", "date"),
        Index("idx_hearing_title_search", "title"),
    )


class Witness(Base):
    """Witness table model."""
    
    __tablename__ = "witnesses"
    
    id = Column(Integer, primary_key=True, index=True)
    hearing_id = Column(Integer, ForeignKey("hearings.id"), nullable=False, index=True)
    
    # Witness information
    name = Column(String(200), nullable=False, index=True)
    title = Column(String(200))
    organization = Column(String(200))
    witness_type = Column(String(50))
    
    # Testimony information
    testimony_url = Column(String(500))
    biography_url = Column(String(500))
    
    # Timestamps
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    
    # Relationships
    hearing = relationship("Hearing", back_populates="witnesses")
    
    # Indexes
    __table_args__ = (
        Index("idx_witness_name_search", "name"),
        Index("idx_witness_organization", "organization"),
    )


class HearingDocument(Base):
    """Hearing document table model."""
    
    __tablename__ = "hearing_documents"
    
    id = Column(Integer, primary_key=True, index=True)
    hearing_id = Column(Integer, ForeignKey("hearings.id"), nullable=False, index=True)
    
    # Document information
    title = Column(String(500), nullable=False)
    document_type = Column(String(50), nullable=False)
    url = Column(String(500), nullable=False)
    file_size = Column(Integer)
    
    # Timestamps
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    
    # Relationships
    hearing = relationship("Hearing", back_populates="documents")
    
    # Indexes
    __table_args__ = (
        Index("idx_document_type", "document_type"),
        Index("idx_document_title_search", "title"),
    )