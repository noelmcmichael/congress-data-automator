"""
Pydantic schemas for relationship and detail endpoints.
"""
from datetime import datetime, date
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from .member import Member
from .committee import Committee
from .hearing import Hearing

class MemberCommitteeResponse(BaseModel):
    """Response schema for member's committee membership."""
    committee: Committee
    position: Optional[str] = None
    is_current: bool = True
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

    class Config:
        from_attributes = True

class CommitteeMemberResponse(BaseModel):
    """Response schema for committee's member."""
    member: Member
    position: Optional[str] = None
    is_current: bool = True
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

    class Config:
        from_attributes = True

class CommitteeHearingResponse(BaseModel):
    """Response schema for committee's hearing."""
    hearing: Hearing
    witness_count: int = 0
    document_count: int = 0

    class Config:
        from_attributes = True

class MemberDetailResponse(BaseModel):
    """Detailed response schema for a single member."""
    member: Member
    committee_memberships: List[MemberCommitteeResponse] = []
    recent_hearings: List[Hearing] = []
    statistics: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        from_attributes = True

class CommitteeDetailResponse(BaseModel):
    """Detailed response schema for a single committee."""
    committee: Committee
    memberships: List[CommitteeMemberResponse] = []
    subcommittees: List[Committee] = []
    recent_hearings: List[Hearing] = []
    statistics: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        from_attributes = True

class HearingDetailResponse(BaseModel):
    """Detailed response schema for a single hearing."""
    hearing: Hearing
    committee: Optional[Committee] = None
    witnesses: List[Dict[str, Any]] = []  # Will be Witness objects when available
    documents: List[Dict[str, Any]] = []  # Will be HearingDocument objects when available
    statistics: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        from_attributes = True

class RelationshipSummary(BaseModel):
    """Summary of relationship data."""
    total_members: int
    total_committees: int
    total_hearings: int
    committee_memberships: int
    subcommittees: int
    active_hearings: int

    class Config:
        from_attributes = True

class NetworkNode(BaseModel):
    """Node in a relationship network graph."""
    id: str
    type: str  # "member", "committee", "hearing"
    label: str
    data: Dict[str, Any]

class NetworkEdge(BaseModel):
    """Edge in a relationship network graph."""
    source: str
    target: str
    type: str  # "member_of", "chair_of", "hearing_of", etc.
    label: str
    data: Dict[str, Any] = Field(default_factory=dict)

class NetworkGraph(BaseModel):
    """Complete network graph of relationships."""
    nodes: List[NetworkNode]
    edges: List[NetworkEdge]
    statistics: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        from_attributes = True