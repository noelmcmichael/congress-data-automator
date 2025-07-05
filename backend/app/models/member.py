"""
Database models for congressional members.
"""
from sqlalchemy import Column, Integer, String, Date, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base


class Member(Base):
    """
    Congressional member (Representative or Senator).
    """
    __tablename__ = "members"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Congress.gov identifiers
    bioguide_id = Column(String(10), unique=True, index=True, nullable=False)
    congress_gov_id = Column(String(20), unique=True, index=True)
    
    # Personal information
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    middle_name = Column(String(100))
    suffix = Column(String(20))
    nickname = Column(String(100))
    
    # Political information
    party = Column(String(50), nullable=False)
    chamber = Column(String(20), nullable=False)  # House or Senate
    state = Column(String(2), nullable=False)
    district = Column(String(10))  # For House members
    
    # Service information
    term_start = Column(Date)
    term_end = Column(Date)
    is_current = Column(Boolean, default=True)
    
    # Contact information
    phone = Column(String(20))
    email = Column(String(255))
    website = Column(String(500))
    
    # Additional information
    birth_date = Column(Date)
    birth_state = Column(String(2))
    birth_city = Column(String(100))
    
    # Images and media
    official_photo_url = Column(String(500))
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_scraped_at = Column(DateTime(timezone=True))
    
    # Relationships
    committee_memberships = relationship("CommitteeMembership", back_populates="member")
    
    def __repr__(self):
        return f"<Member {self.first_name} {self.last_name} ({self.party}-{self.state})>"
    
    @property
    def full_name(self):
        """Return full name of the member."""
        parts = [self.first_name]
        if self.middle_name:
            parts.append(self.middle_name)
        parts.append(self.last_name)
        if self.suffix:
            parts.append(self.suffix)
        return " ".join(parts)
    
    @property
    def display_name(self):
        """Return display name for the member."""
        name = f"{self.first_name} {self.last_name}"
        if self.nickname:
            name = f"{self.nickname} {self.last_name}"
        return name