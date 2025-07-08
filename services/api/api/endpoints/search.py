"""Search and analytics endpoints."""

from typing import List, Dict, Any, Union
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, func

from ..database.connection import get_db
from ..database.models import Member, Committee, Hearing
from ..database.repositories import MemberRepository, CommitteeRepository, HearingRepository
from ..models.base import PaginationParams
from ..models.congress import MemberSummary, CommitteeSummary, HearingSummary

router = APIRouter(prefix="/search", tags=["search"])


@router.get(
    "",
    response_model=Dict[str, List[Union[MemberSummary, CommitteeSummary, HearingSummary]]],
    summary="Global search",
    description="Search across all congressional data (members, committees, hearings).",
)
async def global_search(
    query: str = Query(..., description="Search query"),
    limit: int = Query(10, ge=1, le=50, description="Maximum results per category"),
    db: Session = Depends(get_db),
):
    """Perform global search across all data types."""
    
    results = {
        "members": [],
        "committees": [],
        "hearings": [],
    }
    
    if not query.strip():
        return results
    
    # Search members
    members = (
        db.query(Member)
        .filter(
            or_(
                Member.name.ilike(f"%{query}%"),
                Member.first_name.ilike(f"%{query}%"),
                Member.last_name.ilike(f"%{query}%"),
            )
        )
        .limit(limit)
        .all()
    )
    results["members"] = [MemberSummary.from_orm(member) for member in members]
    
    # Search committees
    committees = (
        db.query(Committee)
        .filter(
            or_(
                Committee.name.ilike(f"%{query}%"),
                Committee.description.ilike(f"%{query}%"),
            )
        )
        .limit(limit)
        .all()
    )
    results["committees"] = [CommitteeSummary.from_orm(committee) for committee in committees]
    
    # Search hearings
    hearings = (
        db.query(Hearing)
        .filter(
            or_(
                Hearing.title.ilike(f"%{query}%"),
                Hearing.description.ilike(f"%{query}%"),
            )
        )
        .limit(limit)
        .all()
    )
    results["hearings"] = [HearingSummary.from_orm(hearing) for hearing in hearings]
    
    return results


@router.get(
    "/members",
    response_model=List[MemberSummary],
    summary="Search members",
    description="Search for congressional members by name.",
)
async def search_members(
    query: str = Query(..., description="Search query"),
    limit: int = Query(20, ge=1, le=100, description="Maximum results"),
    db: Session = Depends(get_db),
):
    """Search for members by name."""
    
    members = (
        db.query(Member)
        .filter(
            or_(
                Member.name.ilike(f"%{query}%"),
                Member.first_name.ilike(f"%{query}%"),
                Member.last_name.ilike(f"%{query}%"),
            )
        )
        .limit(limit)
        .all()
    )
    
    return [MemberSummary.from_orm(member) for member in members]


@router.get(
    "/committees",
    response_model=List[CommitteeSummary],
    summary="Search committees",
    description="Search for congressional committees by name or description.",
)
async def search_committees(
    query: str = Query(..., description="Search query"),
    limit: int = Query(20, ge=1, le=100, description="Maximum results"),
    db: Session = Depends(get_db),
):
    """Search for committees by name or description."""
    
    committees = (
        db.query(Committee)
        .filter(
            or_(
                Committee.name.ilike(f"%{query}%"),
                Committee.description.ilike(f"%{query}%"),
            )
        )
        .limit(limit)
        .all()
    )
    
    return [CommitteeSummary.from_orm(committee) for committee in committees]


@router.get(
    "/hearings",
    response_model=List[HearingSummary],
    summary="Search hearings",
    description="Search for congressional hearings by title or description.",
)
async def search_hearings(
    query: str = Query(..., description="Search query"),
    limit: int = Query(20, ge=1, le=100, description="Maximum results"),
    db: Session = Depends(get_db),
):
    """Search for hearings by title or description."""
    
    hearings = (
        db.query(Hearing)
        .filter(
            or_(
                Hearing.title.ilike(f"%{query}%"),
                Hearing.description.ilike(f"%{query}%"),
            )
        )
        .limit(limit)
        .all()
    )
    
    return [HearingSummary.from_orm(hearing) for hearing in hearings]


# Analytics endpoints
analytics_router = APIRouter(prefix="/analytics", tags=["analytics"])


@analytics_router.get(
    "/overview",
    response_model=Dict[str, Any],
    summary="Get overview analytics",
    description="Get comprehensive overview of congressional data.",
)
async def get_overview_analytics(
    db: Session = Depends(get_db),
):
    """Get overview analytics for all data types."""
    
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
            "total_committees": committee_stats["total_committees"],
            "total_hearings": hearing_stats["total_hearings"],
            "current_members": member_stats["current_members"],
            "current_committees": committee_stats["current_committees"],
        },
    }


@analytics_router.get(
    "/members",
    response_model=Dict[str, Any],
    summary="Get member analytics",
    description="Get detailed analytics for congressional members.",
)
async def get_member_analytics(
    db: Session = Depends(get_db),
):
    """Get member analytics."""
    
    repo = MemberRepository(db)
    return repo.get_statistics()


@analytics_router.get(
    "/committees",
    response_model=Dict[str, Any],
    summary="Get committee analytics",
    description="Get detailed analytics for congressional committees.",
)
async def get_committee_analytics(
    db: Session = Depends(get_db),
):
    """Get committee analytics."""
    
    repo = CommitteeRepository(db)
    return repo.get_statistics()


@analytics_router.get(
    "/hearings",
    response_model=Dict[str, Any],
    summary="Get hearing analytics",
    description="Get detailed analytics for congressional hearings.",
)
async def get_hearing_analytics(
    db: Session = Depends(get_db),
):
    """Get hearing analytics."""
    
    repo = HearingRepository(db)
    return repo.get_statistics()


@analytics_router.get(
    "/trends",
    response_model=Dict[str, Any],
    summary="Get trend analytics",
    description="Get trending data and patterns.",
)
async def get_trend_analytics(
    db: Session = Depends(get_db),
):
    """Get trend analytics."""
    
    from datetime import datetime, timedelta
    
    # Get hearings by month for the last year
    one_year_ago = datetime.utcnow() - timedelta(days=365)
    
    hearing_trends = (
        db.query(
            func.date_trunc('month', Hearing.date).label('month'),
            func.count(Hearing.id).label('count')
        )
        .filter(Hearing.date >= one_year_ago)
        .group_by(func.date_trunc('month', Hearing.date))
        .order_by(func.date_trunc('month', Hearing.date))
        .all()
    )
    
    return {
        "hearing_trends": [
            {
                "month": trend.month.strftime("%Y-%m"),
                "count": trend.count
            }
            for trend in hearing_trends
        ],
        "period": "last_12_months",
    }


# Include analytics router in search router
router.include_router(analytics_router)