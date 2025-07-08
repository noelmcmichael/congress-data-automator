"""
Database models for congressional sessions.
"""
from sqlalchemy import Column, Integer, String, Date, Boolean, DateTime
from sqlalchemy.sql import func
from ..core.database import Base


class CongressionalSession(Base):
    """
    Congressional session metadata and tracking.
    """
    __tablename__ = "congressional_sessions"
    
    session_id = Column(Integer, primary_key=True, index=True)
    congress_number = Column(Integer, unique=True, nullable=False, index=True)
    
    # Session dates
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    is_current = Column(Boolean, nullable=False, default=False)
    
    # Party control information
    party_control_house = Column(String(20))  # Republican, Democratic
    party_control_senate = Column(String(20))  # Republican, Democratic
    
    # Session metadata
    session_name = Column(String(100))  # e.g., "119th Congress"
    description = Column(String(500))
    
    # Election year (even years when House terms begin)
    election_year = Column(Integer)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<CongressionalSession {self.congress_number} ({self.start_date} - {self.end_date})>"
    
    @property
    def display_name(self):
        """Return display name for the congressional session."""
        ordinal = self.get_ordinal_suffix(self.congress_number)
        return f"{self.congress_number}{ordinal} Congress"
    
    @property
    def years_display(self):
        """Return years for display (e.g., '2025-2027')."""
        return f"{self.start_date.year}-{self.end_date.year}"
    
    @property
    def is_republican_controlled_house(self):
        """Check if Republicans control the House."""
        return self.party_control_house == "Republican"
    
    @property
    def is_republican_controlled_senate(self):
        """Check if Republicans control the Senate."""
        return self.party_control_senate == "Republican"
    
    @property
    def unified_control(self):
        """Check if one party controls both chambers."""
        return (self.party_control_house == self.party_control_senate and 
                self.party_control_house is not None)
    
    @staticmethod
    def get_ordinal_suffix(number):
        """Get ordinal suffix for congress number (e.g., 119 -> 'th')."""
        if 10 <= number % 100 <= 20:
            return 'th'
        else:
            suffix_map = {1: 'st', 2: 'nd', 3: 'rd'}
            return suffix_map.get(number % 10, 'th')
    
    @classmethod
    def get_current_session(cls, db_session):
        """Get the current congressional session."""
        return db_session.query(cls).filter(cls.is_current == True).first()
    
    @classmethod
    def get_by_number(cls, db_session, congress_number):
        """Get congressional session by number."""
        return db_session.query(cls).filter(cls.congress_number == congress_number).first()