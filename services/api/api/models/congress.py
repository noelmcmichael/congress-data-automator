"""Congressional data models for the API service."""

from datetime import datetime
from typing import List, Optional
from enum import Enum

from pydantic import BaseModel, Field, field_validator, ConfigDict, ValidationInfo

from .base import FilterParams


class Chamber(str, Enum):
    """Congressional chamber enumeration."""
    HOUSE = "House"
    SENATE = "Senate"
    JOINT = "Joint"


class Party(str, Enum):
    """Political party enumeration."""
    DEMOCRATIC = "Democratic"
    REPUBLICAN = "Republican"
    INDEPENDENT = "Independent"


class MemberType(str, Enum):
    """Member type enumeration."""
    REPRESENTATIVE = "Representative"
    SENATOR = "Senator"
    DELEGATE = "Delegate"
    COMMISSIONER = "Commissioner"


class CommitteeType(str, Enum):
    """Committee type enumeration."""
    STANDING = "Standing"
    SUBCOMMITTEE = "Subcommittee"
    JOINT = "Joint"
    SELECT = "Select"
    TASK_FORCE = "Task Force"


class HearingStatus(str, Enum):
    """Hearing status enumeration."""
    SCHEDULED = "Scheduled"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"
    POSTPONED = "Postponed"


# Member Models
class MemberBase(BaseModel):
    """Base member model."""
    
    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        json_encoders={
            datetime: lambda v: v.isoformat() if v else None
        }
    )
    
    bioguide_id: str = Field(description="Bioguide ID")
    name: str = Field(description="Full name")
    first_name: str = Field(description="First name")
    last_name: str = Field(description="Last name")
    party: Party = Field(description="Political party")
    state: str = Field(description="State abbreviation")
    district: Optional[str] = Field(default=None, description="District number")
    chamber: Chamber = Field(description="Congressional chamber")
    member_type: MemberType = Field(description="Member type")
    is_current: bool = Field(description="Whether member is currently serving")
    
    @field_validator("state")
    @classmethod
    def validate_state(cls, v: str) -> str:
        """Validate state abbreviation."""
        if len(v) != 2:
            raise ValueError("State must be a 2-letter abbreviation")
        return v.upper()
    
    @field_validator("district")
    @classmethod
    def validate_district(cls, v: Optional[str], info: ValidationInfo) -> Optional[str]:
        """Validate district for House members."""
        if info.data:
            chamber = info.data.get("chamber")
            if chamber == Chamber.HOUSE and v is None:
                raise ValueError("House members must have a district")
            if chamber == Chamber.SENATE and v is not None:
                raise ValueError("Senate members cannot have a district")
        return v


class MemberDetail(MemberBase):
    """Detailed member model."""
    
    id: int = Field(description="Database ID")
    middle_name: Optional[str] = Field(default=None, description="Middle name")
    suffix: Optional[str] = Field(default=None, description="Name suffix")
    nickname: Optional[str] = Field(default=None, description="Nickname")
    photo_url: Optional[str] = Field(default=None, description="Photo URL")
    website_url: Optional[str] = Field(default=None, description="Website URL")
    contact_form_url: Optional[str] = Field(default=None, description="Contact form URL")
    phone: Optional[str] = Field(default=None, description="Phone number")
    fax: Optional[str] = Field(default=None, description="Fax number")
    office: Optional[str] = Field(default=None, description="Office address")
    terms_served: Optional[int] = Field(default=None, description="Number of terms served")
    date_of_birth: Optional[datetime] = Field(default=None, description="Date of birth")
    gender: Optional[str] = Field(default=None, description="Gender")
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Last update timestamp")


class MemberSummary(MemberBase):
    """Summary member model."""
    
    id: int = Field(description="Database ID")


class MemberFilterParams(FilterParams):
    """Member filter parameters."""
    
    chamber: Optional[Chamber] = Field(default=None, description="Filter by chamber")
    party: Optional[Party] = Field(default=None, description="Filter by party")
    state: Optional[str] = Field(default=None, description="Filter by state")
    is_current: Optional[bool] = Field(default=None, description="Filter by current status")
    
    @field_validator("state")
    @classmethod
    def validate_state(cls, v: Optional[str]) -> Optional[str]:
        """Validate state abbreviation."""
        if v and len(v) != 2:
            raise ValueError("State must be a 2-letter abbreviation")
        return v.upper() if v else v


# Committee Models
class CommitteeBase(BaseModel):
    """Base committee model."""
    
    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        json_encoders={
            datetime: lambda v: v.isoformat() if v else None
        }
    )
    
    name: str = Field(description="Committee name")
    chamber: Chamber = Field(description="Committee chamber")
    committee_type: CommitteeType = Field(description="Committee type")
    is_current: bool = Field(description="Whether committee is currently active")


class CommitteeDetail(CommitteeBase):
    """Detailed committee model."""
    
    id: int = Field(description="Database ID")
    code: Optional[str] = Field(default=None, description="Committee code")
    description: Optional[str] = Field(default=None, description="Committee description")
    website_url: Optional[str] = Field(default=None, description="Website URL")
    phone: Optional[str] = Field(default=None, description="Phone number")
    office: Optional[str] = Field(default=None, description="Office address")
    jurisdiction: Optional[str] = Field(default=None, description="Committee jurisdiction")
    parent_committee_id: Optional[int] = Field(default=None, description="Parent committee ID")
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Last update timestamp")
    
    class Config:
        """Pydantic configuration."""
        from_attributes = True


class CommitteeSummary(CommitteeBase):
    """Summary committee model."""
    
    id: int = Field(description="Database ID")
    member_count: Optional[int] = Field(default=None, description="Number of members")
    
    class Config:
        """Pydantic configuration."""
        from_attributes = True


class CommitteeFilterParams(FilterParams):
    """Committee filter parameters."""
    
    chamber: Optional[Chamber] = Field(default=None, description="Filter by chamber")
    committee_type: Optional[CommitteeType] = Field(default=None, description="Filter by type")
    is_current: Optional[bool] = Field(default=None, description="Filter by current status")


# Hearing Models
class HearingBase(BaseModel):
    """Base hearing model."""
    
    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        json_encoders={
            datetime: lambda v: v.isoformat() if v else None
        }
    )
    
    title: str = Field(description="Hearing title")
    date: datetime = Field(description="Hearing date")
    status: HearingStatus = Field(description="Hearing status")
    committee_id: int = Field(description="Committee ID")


class HearingDetail(HearingBase):
    """Detailed hearing model."""
    
    id: int = Field(description="Database ID")
    description: Optional[str] = Field(default=None, description="Hearing description")
    location: Optional[str] = Field(default=None, description="Hearing location")
    room: Optional[str] = Field(default=None, description="Hearing room")
    video_url: Optional[str] = Field(default=None, description="Video URL")
    transcript_url: Optional[str] = Field(default=None, description="Transcript URL")
    meeting_type: Optional[str] = Field(default=None, description="Meeting type")
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Last update timestamp")
    
    class Config:
        """Pydantic configuration."""
        from_attributes = True


class HearingSummary(HearingBase):
    """Summary hearing model."""
    
    id: int = Field(description="Database ID")
    committee_name: Optional[str] = Field(default=None, description="Committee name")
    
    class Config:
        """Pydantic configuration."""
        from_attributes = True


class HearingFilterParams(FilterParams):
    """Hearing filter parameters."""
    
    committee_id: Optional[int] = Field(default=None, description="Filter by committee ID")
    status: Optional[HearingStatus] = Field(default=None, description="Filter by status")
    date_from: Optional[datetime] = Field(default=None, description="Filter by start date")
    date_to: Optional[datetime] = Field(default=None, description="Filter by end date")
    
    @field_validator("date_from", "date_to")
    @classmethod
    def validate_dates(cls, v: Optional[datetime]) -> Optional[datetime]:
        """Validate date format."""
        return v


# Relationship Models
class CommitteeMembership(BaseModel):
    """Committee membership model."""
    
    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        json_encoders={
            datetime: lambda v: v.isoformat() if v else None
        }
    )
    
    member_id: int = Field(description="Member ID")
    committee_id: int = Field(description="Committee ID")
    position: Optional[str] = Field(default=None, description="Position on committee")
    is_chair: bool = Field(default=False, description="Whether member is chair")
    is_ranking_member: bool = Field(default=False, description="Whether member is ranking member")
    is_current: bool = Field(default=True, description="Whether membership is current")


class MemberWithCommittees(MemberDetail):
    """Member with committee assignments."""
    
    committees: List[CommitteeSummary] = Field(description="Committee assignments")


class CommitteeWithMembers(CommitteeDetail):
    """Committee with member roster."""
    
    members: List[MemberSummary] = Field(description="Committee members")


class HearingWithDetails(HearingDetail):
    """Hearing with related details."""
    
    committee: CommitteeSummary = Field(description="Committee information")
    witnesses: List[str] = Field(default=[], description="Hearing witnesses")