"""Congressional data models for validation service."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum

from pydantic import Field, validator, model_validator

from .base import BaseModel


class ChamberType(str, Enum):
    """Congressional chamber enumeration."""
    HOUSE = "house"
    SENATE = "senate"


class PartyType(str, Enum):
    """Political party enumeration."""
    REPUBLICAN = "Republican"
    DEMOCRAT = "Democratic"
    INDEPENDENT = "Independent"
    LIBERTARIAN = "Libertarian"
    GREEN = "Green"
    OTHER = "Other"


class HearingStatus(str, Enum):
    """Hearing status enumeration."""
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    POSTPONED = "postponed"


class Member(BaseModel):
    """Congressional member data model."""
    
    member_id: str = Field(..., description="Unique member identifier")
    bioguide_id: Optional[str] = Field(None, description="Bioguide identifier")
    first_name: str = Field(..., description="Member first name")
    last_name: str = Field(..., description="Member last name")
    full_name: str = Field(..., description="Member full name")
    
    # Chamber and party information
    chamber: ChamberType = Field(..., description="Congressional chamber")
    party: PartyType = Field(..., description="Political party")
    
    # Geographic information
    state: str = Field(..., description="State abbreviation (e.g., 'CA', 'NY')")
    district: Optional[str] = Field(None, description="District number (House only)")
    
    # Term information
    term_start: Optional[datetime] = Field(None, description="Current term start date")
    term_end: Optional[datetime] = Field(None, description="Current term end date")
    
    # Status information
    in_office: bool = Field(default=True, description="Currently in office")
    
    # URLs and contact information
    official_url: Optional[str] = Field(None, description="Official website URL")
    contact_form_url: Optional[str] = Field(None, description="Contact form URL")
    
    # Metadata
    source: str = Field(..., description="Data source (e.g., 'congress_api', 'web_scraping')")
    
    @validator("state")
    def validate_state(cls, v: str) -> str:
        """Validate state abbreviation."""
        if len(v) != 2:
            raise ValueError("State must be a 2-letter abbreviation")
        return v.upper()
    
    @validator("district")
    def validate_district(cls, v: Optional[str], values: Dict[str, Any]) -> Optional[str]:
        """Validate district number."""
        if v is not None and values.get("chamber") == ChamberType.SENATE:
            raise ValueError("Senators should not have district numbers")
        return v


class Committee(BaseModel):
    """Congressional committee data model."""
    
    committee_id: str = Field(..., description="Unique committee identifier")
    name: str = Field(..., description="Committee name")
    full_name: str = Field(..., description="Committee full name")
    
    # Chamber and type information
    chamber: ChamberType = Field(..., description="Congressional chamber")
    committee_type: str = Field(..., description="Committee type (e.g., 'standing', 'subcommittee')")
    
    # Hierarchy information
    parent_committee_id: Optional[str] = Field(None, description="Parent committee ID (for subcommittees)")
    is_subcommittee: bool = Field(default=False, description="Is this a subcommittee")
    
    # URLs and resources
    official_url: Optional[str] = Field(None, description="Official committee website URL")
    hearings_url: Optional[str] = Field(None, description="Committee hearings URL")
    members_url: Optional[str] = Field(None, description="Committee members URL")
    documents_url: Optional[str] = Field(None, description="Committee documents URL")
    
    # Status information
    active: bool = Field(default=True, description="Committee is currently active")
    
    # Metadata
    source: str = Field(..., description="Data source")
    
    @model_validator(mode='after')
    def validate_parent_committee(self) -> 'Committee':
        """Validate parent committee relationship."""
        if self.is_subcommittee and self.parent_committee_id is None:
            raise ValueError("Subcommittees must have a parent committee ID")
        if not self.is_subcommittee and self.parent_committee_id is not None:
            raise ValueError("Only subcommittees should have parent committee IDs")
        return self


class Hearing(BaseModel):
    """Congressional hearing data model."""
    
    hearing_id: str = Field(..., description="Unique hearing identifier")
    title: str = Field(..., description="Hearing title")
    description: Optional[str] = Field(None, description="Hearing description")
    
    # Committee information
    committee_id: str = Field(..., description="Committee conducting the hearing")
    committee_name: str = Field(..., description="Committee name")
    chamber: ChamberType = Field(..., description="Congressional chamber")
    
    # Scheduling information
    date: Optional[datetime] = Field(None, description="Hearing date")
    time: Optional[str] = Field(None, description="Hearing time")
    location: Optional[str] = Field(None, description="Hearing location")
    
    # Status information
    status: HearingStatus = Field(..., description="Hearing status")
    
    # URLs and resources
    hearing_url: Optional[str] = Field(None, description="Hearing details URL")
    transcript_url: Optional[str] = Field(None, description="Hearing transcript URL")
    video_url: Optional[str] = Field(None, description="Hearing video URL")
    
    # Witnesses and participants
    witnesses: List[Dict[str, Any]] = Field(default_factory=list, description="Hearing witnesses")
    
    # Metadata
    source: str = Field(..., description="Data source")
    
    @validator("date")
    def validate_date(cls, v: Optional[datetime]) -> Optional[datetime]:
        """Validate hearing date."""
        if v is not None and v.year < 1900:
            raise ValueError("Hearing date cannot be before 1900")
        return v


class ValidationResult(BaseModel):
    """Data validation result model."""
    
    table_name: str = Field(..., description="Name of the validated table")
    expectation_suite: str = Field(..., description="Name of the expectation suite")
    run_id: str = Field(..., description="Validation run identifier")
    
    # Results
    success: bool = Field(..., description="Overall validation success")
    results_count: int = Field(..., description="Number of validation results")
    successful_expectations: int = Field(..., description="Number of successful expectations")
    unsuccessful_expectations: int = Field(..., description="Number of unsuccessful expectations")
    
    # Timing
    run_time: datetime = Field(..., description="Validation run time")
    duration_seconds: float = Field(..., description="Validation duration in seconds")
    
    # Details
    validation_details: Dict[str, Any] = Field(default_factory=dict, description="Detailed validation results")
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate percentage."""
        if self.results_count == 0:
            return 0.0
        return (self.successful_expectations / self.results_count) * 100.0


class DataPromotion(BaseModel):
    """Data promotion tracking model."""
    
    promotion_id: str = Field(..., description="Unique promotion identifier")
    table_name: str = Field(..., description="Name of the promoted table")
    
    # Source and target
    source_schema: str = Field(..., description="Source schema name")
    target_schema: str = Field(..., description="Target schema name")
    target_table: str = Field(..., description="Target table name (with version)")
    
    # Metrics
    records_processed: int = Field(..., description="Number of records processed")
    records_promoted: int = Field(..., description="Number of records promoted")
    records_failed: int = Field(..., description="Number of records that failed promotion")
    
    # Status
    success: bool = Field(..., description="Promotion success")
    error_message: Optional[str] = Field(None, description="Error message if failed")
    
    # Timing
    started_at: datetime = Field(..., description="Promotion start time")
    completed_at: Optional[datetime] = Field(None, description="Promotion completion time")
    
    @property
    def duration_seconds(self) -> Optional[float]:
        """Calculate promotion duration in seconds."""
        if self.completed_at is None:
            return None
        return (self.completed_at - self.started_at).total_seconds()
    
    @property
    def success_rate(self) -> float:
        """Calculate promotion success rate percentage."""
        if self.records_processed == 0:
            return 0.0
        return (self.records_promoted / self.records_processed) * 100.0