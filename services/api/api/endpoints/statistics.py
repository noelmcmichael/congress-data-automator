"""Statistics API endpoints."""

from typing import Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database.connection import get_db
from ..database.repositories import MemberRepository, CommitteeRepository, HearingRepository

router = APIRouter(prefix="/statistics", tags=["statistics"])


@router.get(
    "/members",
    response_model=Dict[str, Any],
    summary="Get member statistics",
    description="Get comprehensive statistics about congressional members.",
)
async def get_member_statistics(
    db: Session = Depends(get_db),
):
    """Get member statistics."""
    
    repo = MemberRepository(db)
    return repo.get_statistics()


@router.get(
    "/committees",
    response_model=Dict[str, Any],
    summary="Get committee statistics",
    description="Get comprehensive statistics about congressional committees.",
)
async def get_committee_statistics(
    db: Session = Depends(get_db),
):
    """Get committee statistics."""
    
    repo = CommitteeRepository(db)
    return repo.get_statistics()


@router.get(
    "/hearings",
    response_model=Dict[str, Any],
    summary="Get hearing statistics",
    description="Get comprehensive statistics about congressional hearings.",
)
async def get_hearing_statistics(
    db: Session = Depends(get_db),
):
    """Get hearing statistics."""
    
    repo = HearingRepository(db)
    return repo.get_statistics()


@router.get(
    "/overview",
    response_model=Dict[str, Any],
    summary="Get overview statistics",
    description="Get comprehensive overview of all congressional data.",
)
async def get_overview_statistics(
    db: Session = Depends(get_db),
):
    """Get overview statistics."""
    
    member_repo = MemberRepository(db)
    committee_repo = CommitteeRepository(db)
    hearing_repo = HearingRepository(db)
    
    member_stats = member_repo.get_statistics()
    committee_stats = committee_repo.get_statistics()
    hearing_stats = hearing_repo.get_statistics()
    
    return {
        "members": member_stats,
        "committees": committee_stats,
        "hearings": hearing_stats,
        "summary": {
            "total_members": member_stats["total_members"],
            "current_members": member_stats["current_members"],
            "total_committees": committee_stats["total_committees"],
            "current_committees": committee_stats["current_committees"],
            "total_hearings": hearing_stats["total_hearings"],
        },
    }