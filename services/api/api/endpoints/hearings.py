"""Hearings API endpoints."""

from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..core.exceptions import NotFoundError
from ..database.connection import get_db
from ..database.repositories import HearingRepository
from ..models.base import PaginatedResponse, PaginationParams, PaginationResponse
from ..models.congress import (
    HearingDetail,
    HearingSummary,
    HearingFilterParams,
    HearingWithDetails,
    CommitteeSummary,
)

router = APIRouter(prefix="/hearings", tags=["hearings"])


@router.get(
    "",
    response_model=PaginatedResponse,
    summary="List hearings",
    description="Get a paginated list of congressional hearings with optional filtering and search.",
)
async def get_hearings(
    # Pagination parameters
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(20, ge=1, le=100, description="Page size"),
    
    # Filter parameters
    committee_id: Optional[int] = Query(None, description="Filter by committee ID"),
    status: Optional[str] = Query(None, description="Filter by hearing status (Scheduled, Completed, Cancelled, Postponed)"),
    date_from: Optional[datetime] = Query(None, description="Filter by start date (YYYY-MM-DD)"),
    date_to: Optional[datetime] = Query(None, description="Filter by end date (YYYY-MM-DD)"),
    
    # Search and sort parameters
    search: str = Query(None, description="Search in hearing titles and descriptions"),
    sort_by: str = Query(None, description="Sort field (title, date, status)"),
    sort_order: str = Query("asc", description="Sort order (asc, desc)"),
    
    # Dependencies
    db: Session = Depends(get_db),
):
    """Get paginated list of hearings with filtering and search."""
    
    # Create filter parameters
    filters = HearingFilterParams(
        committee_id=committee_id,
        status=status,
        date_from=date_from,
        date_to=date_to,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order,
    )
    
    # Create pagination parameters
    pagination = PaginationParams(page=page, size=size)
    
    # Get hearings from repository
    repo = HearingRepository(db)
    hearings, total = repo.get_all(filters, pagination)
    
    # Convert to response models
    hearing_summaries = [HearingSummary.model_validate(hearing) for hearing in hearings]
    
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
        data=hearing_summaries,
        pagination=pagination_response,
    )


@router.get(
    "/{hearing_id}",
    response_model=HearingDetail,
    summary="Get hearing details",
    description="Get detailed information about a specific congressional hearing.",
)
async def get_hearing(
    hearing_id: int,
    db: Session = Depends(get_db),
):
    """Get hearing details by ID."""
    
    repo = HearingRepository(db)
    hearing = repo.get_by_id(hearing_id)
    
    if not hearing:
        raise NotFoundError(
            message="Hearing not found",
            detail=f"Hearing with ID {hearing_id} not found",
        )
    
    return HearingDetail.model_validate(hearing)


@router.get(
    "/{hearing_id}/full",
    response_model=HearingWithDetails,
    summary="Get hearing with details",
    description="Get detailed hearing information including committee information and witnesses.",
)
async def get_hearing_with_details(
    hearing_id: int,
    db: Session = Depends(get_db),
):
    """Get hearing with committee and witness information."""
    
    repo = HearingRepository(db)
    hearing = repo.get_hearing_with_committee(hearing_id)
    
    if not hearing:
        raise NotFoundError(
            message="Hearing not found",
            detail=f"Hearing with ID {hearing_id} not found",
        )
    
    # Create response with committee and witnesses
    hearing_data = HearingDetail.model_validate(hearing)
    committee_data = CommitteeSummary.model_validate(hearing.committee)
    
    # Get witnesses (simplified for now)
    witnesses = [witness.name for witness in hearing.witnesses]
    
    return HearingWithDetails(
        **hearing_data.dict(),
        committee=committee_data,
        witnesses=witnesses,
    )


@router.get(
    "/upcoming",
    response_model=List[HearingSummary],
    summary="Get upcoming hearings",
    description="Get upcoming hearings (next 30 days).",
)
async def get_upcoming_hearings(
    limit: int = Query(10, ge=1, le=50, description="Maximum number of hearings to return"),
    db: Session = Depends(get_db),
):
    """Get upcoming hearings."""
    
    from datetime import datetime, timedelta
    
    # Get hearings in the next 30 days
    now = datetime.utcnow()
    thirty_days_later = now + timedelta(days=30)
    
    filters = HearingFilterParams(
        date_from=now,
        date_to=thirty_days_later,
        status="Scheduled",
        sort_by="date",
        sort_order="asc",
    )
    
    pagination = PaginationParams(page=1, size=limit)
    
    repo = HearingRepository(db)
    hearings, _ = repo.get_all(filters, pagination)
    
    return [HearingSummary.model_validate(hearing) for hearing in hearings]


@router.get(
    "/recent",
    response_model=List[HearingSummary],
    summary="Get recent hearings",
    description="Get recent hearings (last 30 days).",
)
async def get_recent_hearings(
    limit: int = Query(10, ge=1, le=50, description="Maximum number of hearings to return"),
    db: Session = Depends(get_db),
):
    """Get recent hearings."""
    
    from datetime import datetime, timedelta
    
    # Get hearings in the last 30 days
    now = datetime.utcnow()
    thirty_days_ago = now - timedelta(days=30)
    
    filters = HearingFilterParams(
        date_from=thirty_days_ago,
        date_to=now,
        sort_by="date",
        sort_order="desc",
    )
    
    pagination = PaginationParams(page=1, size=limit)
    
    repo = HearingRepository(db)
    hearings, _ = repo.get_all(filters, pagination)
    
    return [HearingSummary.model_validate(hearing) for hearing in hearings]


@router.get(
    "/committee/{committee_id}",
    response_model=List[HearingSummary],
    summary="Get committee hearings",
    description="Get all hearings for a specific committee.",
)
async def get_committee_hearings(
    committee_id: int,
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(20, ge=1, le=100, description="Page size"),
    db: Session = Depends(get_db),
):
    """Get hearings for a specific committee."""
    
    filters = HearingFilterParams(
        committee_id=committee_id,
        sort_by="date",
        sort_order="desc",
    )
    
    pagination = PaginationParams(page=page, size=size)
    
    repo = HearingRepository(db)
    hearings, _ = repo.get_all(filters, pagination)
    
    return [HearingSummary.model_validate(hearing) for hearing in hearings]


@router.get(
    "/statistics",
    response_model=dict,
    summary="Get hearing statistics",
    description="Get statistical information about congressional hearings.",
)
async def get_hearing_statistics(
    db: Session = Depends(get_db),
):
    """Get hearing statistics."""
    
    repo = HearingRepository(db)
    return repo.get_statistics()