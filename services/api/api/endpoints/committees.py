"""Committees API endpoints."""

from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..core.exceptions import NotFoundError, ValidationError
from ..core.validators import validate_id_parameter, validate_pagination_params, validate_committee_filters
from ..database.connection import get_db
from ..database.repositories import CommitteeRepository
from ..models.base import PaginatedResponse, PaginationParams, PaginationResponse
from ..models.congress import (
    CommitteeDetail,
    CommitteeSummary,
    CommitteeFilterParams,
    CommitteeWithMembers,
    MemberSummary,
)

router = APIRouter(prefix="/committees", tags=["committees"])


@router.get(
    "",
    response_model=PaginatedResponse,
    summary="List committees",
    description="Get a paginated list of congressional committees with optional filtering and search.",
)
async def get_committees(
    # Pagination parameters
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(20, ge=1, le=100, description="Page size"),
    
    # Filter parameters
    chamber: str = Query(None, description="Filter by chamber (House, Senate, Joint)"),
    committee_type: str = Query(None, description="Filter by committee type (Standing, Subcommittee, Select, Joint)"),
    is_current: bool = Query(None, description="Filter by current status"),
    
    # Search and sort parameters
    search: str = Query(None, description="Search in committee names and descriptions"),
    sort_by: str = Query(None, description="Sort field (name, chamber, committee_type)"),
    sort_order: str = Query("asc", description="Sort order (asc, desc)"),
    
    # Dependencies
    db: Session = Depends(get_db),
):
    """Get paginated list of committees with filtering and search."""
    
    # Validate pagination parameters
    validate_pagination_params(page, size)
    
    # Validate filter parameters
    validate_committee_filters(
        chamber=chamber,
        committee_type=committee_type,
        is_current=is_current,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order,
    )
    
    # Create filter parameters
    filters = CommitteeFilterParams(
        chamber=chamber,
        committee_type=committee_type,
        is_current=is_current,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order,
    )
    
    # Create pagination parameters
    pagination = PaginationParams(page=page, size=size)
    
    # Get committees from repository
    repo = CommitteeRepository(db)
    committees, total = repo.get_all(filters, pagination)
    
    # Convert to response models
    committee_summaries = [CommitteeSummary.model_validate(committee) for committee in committees]
    
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
        data=committee_summaries,
        pagination=pagination_response,
    )


@router.get(
    "/{committee_id}",
    response_model=CommitteeDetail,
    summary="Get committee details",
    description="Get detailed information about a specific congressional committee.",
)
async def get_committee(
    committee_id: int,
    db: Session = Depends(get_db),
):
    """Get committee details by ID."""
    
    # Validate committee ID
    validate_id_parameter(committee_id, "Committee")
    
    repo = CommitteeRepository(db)
    committee = repo.get_by_id(committee_id)  # Now raises exceptions automatically
    
    return CommitteeDetail.model_validate(committee)


@router.get(
    "/{committee_id}/members",
    response_model=List[MemberSummary],
    summary="Get committee members",
    description="Get all members of a specific committee.",
)
async def get_committee_members(
    committee_id: int,
    db: Session = Depends(get_db),
):
    """Get members of a committee."""
    
    # Validate committee ID
    validate_id_parameter(committee_id, "Committee")
    
    repo = CommitteeRepository(db)
    
    # Get members (repository now handles validation and errors)
    members = repo.get_committee_members(committee_id)
    
    return [MemberSummary.model_validate(member) for member in members]


@router.get(
    "/{committee_id}/subcommittees",
    response_model=List[CommitteeSummary],
    summary="Get committee subcommittees",
    description="Get all subcommittees of a specific committee.",
)
async def get_committee_subcommittees(
    committee_id: int,
    db: Session = Depends(get_db),
):
    """Get subcommittees of a committee."""
    
    # Validate committee ID
    validate_id_parameter(committee_id, "Committee")
    
    repo = CommitteeRepository(db)
    
    # Get subcommittees (repository now handles validation and errors)
    subcommittees = repo.get_subcommittees(committee_id)
    
    return [CommitteeSummary.model_validate(subcommittee) for subcommittee in subcommittees]


@router.get(
    "/{committee_id}/full",
    response_model=CommitteeWithMembers,
    summary="Get committee with members",
    description="Get detailed committee information including all members.",
)
async def get_committee_with_members(
    committee_id: int,
    db: Session = Depends(get_db),
):
    """Get committee with its members."""
    
    # Validate committee ID
    validate_id_parameter(committee_id, "Committee")
    
    repo = CommitteeRepository(db)
    committee = repo.get_committee_with_members(committee_id)  # Now raises exceptions automatically
    
    # Create response with members
    committee_data = CommitteeDetail.model_validate(committee)
    members = [
        MemberSummary.model_validate(membership.member)
        for membership in committee.committee_memberships
        if membership.is_current
    ]
    
    return CommitteeWithMembers(
        **committee_data.model_dump(),
        members=members,
    )


@router.get(
    "/code/{committee_code}",
    response_model=CommitteeDetail,
    summary="Get committee by code",
    description="Get committee details by their committee code.",
)
async def get_committee_by_code(
    committee_code: str,
    db: Session = Depends(get_db),
):
    """Get committee by code."""
    
    # Validate committee code
    if not committee_code or not committee_code.strip():
        raise ValidationError(
            message="Invalid committee code",
            detail="Committee code cannot be empty"
        )
    
    committee_code = committee_code.strip()
    if len(committee_code) > 20:
        raise ValidationError(
            message="Invalid committee code",
            detail="Committee code cannot exceed 20 characters"
        )
    
    repo = CommitteeRepository(db)
    committee = repo.get_by_code(committee_code)
    
    if not committee:
        raise NotFoundError(
            message="Committee not found",
            detail=f"Committee with code {committee_code} not found",
        )
    
    return CommitteeDetail.model_validate(committee)


@router.get(
    "/statistics",
    response_model=dict,
    summary="Get committee statistics",
    description="Get statistical information about congressional committees.",
)
async def get_committee_statistics(
    db: Session = Depends(get_db),
):
    """Get committee statistics."""
    
    repo = CommitteeRepository(db)
    return repo.get_statistics()