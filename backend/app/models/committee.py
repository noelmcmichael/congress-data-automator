"""
Database models for congressional committees and subcommittees.
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base


class Committee(Base):
    """
    Congressional committee or subcommittee.
    """
    __tablename__ = "committees"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Congress.gov identifiers
    congress_gov_id = Column(String(50), unique=True, index=True)
    committee_code = Column(String(10), index=True)
    
    # Basic information
    name = Column(String(255), nullable=False)
    chamber = Column(String(20), nullable=False)  # House, Senate, or Joint
    committee_type = Column(String(50), nullable=False)  # Standing, Select, Joint, etc.
    
    # Hierarchy
    parent_committee_id = Column(Integer, ForeignKey("committees.id"))
    is_subcommittee = Column(Boolean, default=False)
    
    # Details
    description = Column(Text)
    jurisdiction = Column(Text)
    
    # Leadership
    chair_member_id = Column(Integer, ForeignKey("members.id"))
    ranking_member_id = Column(Integer, ForeignKey("members.id"))
    
    # Contact information
    phone = Column(String(20))
    email = Column(String(255))
    website = Column(String(500))
    office_location = Column(String(255))
    
    # Official URLs
    hearings_url = Column(String(255))
    members_url = Column(String(255))
    official_website_url = Column(String(255))
    last_url_update = Column(DateTime(timezone=True))
    
    # Activity status
    is_active = Column(Boolean, default=True)
    
    # Congressional session tracking
    congress_session = Column(Integer, nullable=False, default=119)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_scraped_at = Column(DateTime(timezone=True))
    
    # Relationships
    parent_committee = relationship("Committee", remote_side=[id], back_populates="subcommittees")
    subcommittees = relationship("Committee", back_populates="parent_committee")
    
    chair = relationship("Member", foreign_keys=[chair_member_id])
    ranking_member = relationship("Member", foreign_keys=[ranking_member_id])
    
    memberships = relationship("CommitteeMembership", back_populates="committee")
    hearings = relationship("Hearing", back_populates="committee")
    
    def __repr__(self):
        return f"<Committee {self.name} ({self.chamber})>"
    
    @property
    def full_name(self):
        """Return full committee name including parent if subcommittee."""
        if self.is_subcommittee and self.parent_committee:
            return f"{self.parent_committee.name} - {self.name}"
        return self.name


class CommitteeMembership(Base):
    """
    Relationship between members and committees.
    """
    __tablename__ = "committee_memberships"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False)
    committee_id = Column(Integer, ForeignKey("committees.id"), nullable=False)
    
    # Membership details
    position = Column(String(50))  # Chair, Ranking Member, Member, etc.
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    is_current = Column(Boolean, default=True)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    member = relationship("Member", back_populates="committee_memberships")
    committee = relationship("Committee", back_populates="memberships")
    
    def __repr__(self):
        return f"<CommitteeMembership {self.member.full_name} - {self.committee.name}>"