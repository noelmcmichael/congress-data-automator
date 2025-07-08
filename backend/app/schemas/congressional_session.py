"""
Pydantic schemas for congressional sessions.
"""
from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field


class CongressionalSessionBase(BaseModel):
    """Base schema for congressional sessions."""
    congress_number: int = Field(..., description="Congress number (e.g., 119)")
    start_date: date = Field(..., description="Session start date")
    end_date: date = Field(..., description="Session end date")
    is_current: bool = Field(default=False, description="Whether this is the current session")
    party_control_house: Optional[str] = Field(None, description="Party controlling the House")
    party_control_senate: Optional[str] = Field(None, description="Party controlling the Senate")
    session_name: Optional[str] = Field(None, description="Display name (e.g., '119th Congress')")
    description: Optional[str] = Field(None, description="Session description")
    election_year: Optional[int] = Field(None, description="Election year for this Congress")


class CongressionalSessionCreate(CongressionalSessionBase):
    """Schema for creating congressional sessions."""
    pass


class CongressionalSessionUpdate(BaseModel):
    """Schema for updating congressional sessions."""
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_current: Optional[bool] = None
    party_control_house: Optional[str] = None
    party_control_senate: Optional[str] = None
    session_name: Optional[str] = None
    description: Optional[str] = None
    election_year: Optional[int] = None


class CongressionalSession(CongressionalSessionBase):
    """Schema for congressional session responses."""
    session_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    # Computed properties
    display_name: str = Field(..., description="Formatted display name")
    years_display: str = Field(..., description="Years in format '2025-2027'")
    is_republican_controlled_house: bool = Field(..., description="Whether Republicans control House")
    is_republican_controlled_senate: bool = Field(..., description="Whether Republicans control Senate")
    unified_control: bool = Field(..., description="Whether one party controls both chambers")

    class Config:
        from_attributes = True


class CongressionalSessionSummary(BaseModel):
    """Summary schema for congressional sessions."""
    congress_number: int
    display_name: str
    years_display: str
    is_current: bool
    party_control_house: Optional[str] = None
    party_control_senate: Optional[str] = None
    unified_control: bool


class CurrentCongressInfo(BaseModel):
    """Information about the current Congress."""
    current_session: CongressionalSession
    days_remaining: int = Field(..., description="Days remaining in current session")
    next_election_year: int = Field(..., description="Next House election year")
    house_majority: str = Field(..., description="Party with House majority")
    senate_majority: str = Field(..., description="Party with Senate majority")
    unified_government: bool = Field(..., description="Whether same party controls both chambers")
    
    # Historical context
    previous_session: Optional[CongressionalSessionSummary] = None
    next_session: Optional[CongressionalSessionSummary] = None