"""Members API endpoints."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..core.exceptions import NotFoundError
from ..database.connection import get_db
from ..database.repositories import MemberRepository
from ..models.base import PaginatedResponse, PaginationParams, PaginationResponse
from ..models.congress import (
    MemberDetail,
    MemberSummary,
    MemberFilterParams,
    MemberWithCommittees,
    CommitteeSummary,
)

router = APIRouter(prefix="/members", tags=["members"])


@router.get(
    "",
    summary="List members",
    description="Get a paginated list of congressional members with optional filtering and search.",
)
async def get_members(
    # Pagination parameters
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(20, ge=1, le=100, description="Page size"),
    
    # Filter parameters
    chamber: str = Query(None, description="Filter by chamber (House, Senate)"),
    party: str = Query(None, description="Filter by party (Democratic, Republican, Independent)"),
    state: str = Query(None, description="Filter by state abbreviation"),
    is_current: bool = Query(None, description="Filter by current status"),
    
    # Search and sort parameters
    search: str = Query(None, description="Search in member names"),
    sort_by: str = Query(None, description="Sort field (name, party, state, chamber)"),
    sort_order: str = Query("asc", description="Sort order (asc, desc)"),
    
    # Dependencies
    db: Session = Depends(get_db),
):
    """Get paginated list of members with filtering and search."""
    
    # Create filter parameters
    filters = MemberFilterParams(
        chamber=chamber,
        party=party,
        state=state,
        is_current=is_current,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order,
    )
    
    # Create pagination parameters
    pagination = PaginationParams(page=page, size=size)
    
    # Get members from repository
    repo = MemberRepository(db)
    members, total = repo.get_all(filters, pagination)
    
    # Convert to response models
    member_summaries = [MemberSummary.model_validate(member) for member in members]
    
    # Create pagination response
    pagination_response = PaginationResponse(
        page=pagination.page,
        size=pagination.size,
        total=total,
        pages=(total + pagination.size - 1) // pagination.size,
        has_next=pagination.page * pagination.size < total,
        has_prev=pagination.page > 1,
    )
    
    return PaginatedResponse(
        data=member_summaries,
        pagination=pagination_response,
    )


@router.get(
    "/{member_id}",
    response_model=MemberDetail,
    summary="Get member details",
    description="Get detailed information about a specific congressional member.",
)
async def get_member(
    member_id: int,
    db: Session = Depends(get_db),
):
    """Get member details by ID."""
    
    repo = MemberRepository(db)
    member = repo.get_by_id(member_id)
    
    if not member:
        raise NotFoundError(
            message="Member not found",
            detail=f"Member with ID {member_id} not found",
        )
    
    return MemberDetail.model_validate(member)


@router.get(
    "/{member_id}/committees",
    response_model=List[CommitteeSummary],
    summary="Get member committees",
    description="Get all committee assignments for a specific member.",
)
async def get_member_committees(
    member_id: int,
    db: Session = Depends(get_db),
):
    """Get committee assignments for a member."""
    
    repo = MemberRepository(db)
    
    # Check if member exists
    member = repo.get_by_id(member_id)
    if not member:
        raise NotFoundError(
            message="Member not found",
            detail=f"Member with ID {member_id} not found",
        )
    
    # Get committees
    committees = repo.get_member_committees(member_id)
    
    return [CommitteeSummary.model_validate(committee) for committee in committees]


@router.get(
    "/{member_id}/full",
    response_model=MemberWithCommittees,
    summary="Get member with committees",
    description="Get detailed member information including all committee assignments.",
)
async def get_member_with_committees(
    member_id: int,
    db: Session = Depends(get_db),
):
    """Get member with their committee assignments."""
    
    repo = MemberRepository(db)
    member = repo.get_member_with_committees(member_id)
    
    if not member:
        raise NotFoundError(
            message="Member not found",
            detail=f"Member with ID {member_id} not found",
        )
    
    # Create response with committees
    member_data = MemberDetail.model_validate(member)
    committees = [
        CommitteeSummary.model_validate(membership.committee)
        for membership in member.committee_memberships
        if membership.is_current
    ]
    
    return MemberWithCommittees(
        **member_data.dict(),
        committees=committees,
    )


@router.get(
    "/bioguide/{bioguide_id}",
    response_model=MemberDetail,
    summary="Get member by bioguide ID",
    description="Get member details by their bioguide ID.",
)
async def get_member_by_bioguide(
    bioguide_id: str,
    db: Session = Depends(get_db),
):
    """Get member by bioguide ID."""
    
    repo = MemberRepository(db)
    member = repo.get_by_bioguide_id(bioguide_id)
    
    if not member:
        raise NotFoundError(
            message="Member not found",
            detail=f"Member with bioguide ID {bioguide_id} not found",
        )
    
    return MemberDetail.model_validate(member)


@router.get(
    "/statistics",
    response_model=dict,
    summary="Get member statistics",
    description="Get statistical information about congressional members.",
)
async def get_member_statistics(
    db: Session = Depends(get_db),
):
    """Get member statistics."""
    
    repo = MemberRepository(db)
    return repo.get_statistics()