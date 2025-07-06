"""
API endpoints for data updates and management.
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Dict, Any
import structlog
from ...core.database import get_db
from ...services.data_processor import DataProcessor

logger = structlog.get_logger()

router = APIRouter()

# Initialize data processor
data_processor = DataProcessor()


@router.post("/update/members")
async def update_members(
    background_tasks: BackgroundTasks,
    force_refresh: bool = False,
    db: Session = Depends(get_db)
):
    """
    Update congressional members from Congress.gov API.
    
    Args:
        force_refresh: Force refresh even if recently updated
        db: Database session
        
    Returns:
        Update summary
    """
    try:
        # Run in background for large updates
        background_tasks.add_task(
            data_processor.update_members,
            force_refresh=force_refresh
        )
        
        return {
            "message": "Members update started",
            "force_refresh": force_refresh,
            "status": "processing"
        }
        
    except Exception as e:
        logger.error("Error starting members update", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to start members update")


@router.post("/update/committees")
async def update_committees(
    background_tasks: BackgroundTasks,
    force_refresh: bool = False,
    db: Session = Depends(get_db)
):
    """
    Update committees from Congress.gov API and web scraping.
    
    Args:
        force_refresh: Force refresh even if recently updated
        db: Database session
        
    Returns:
        Update summary
    """
    try:
        # Run in background for large updates
        background_tasks.add_task(
            data_processor.update_committees,
            force_refresh=force_refresh
        )
        
        return {
            "message": "Committees update started",
            "force_refresh": force_refresh,
            "status": "processing"
        }
        
    except Exception as e:
        logger.error("Error starting committees update", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to start committees update")


@router.post("/update/hearings")
async def update_hearings(
    background_tasks: BackgroundTasks,
    force_refresh: bool = False,
    db: Session = Depends(get_db)
):
    """
    Update hearings from Congress.gov API and web scraping.
    
    Args:
        force_refresh: Force refresh even if recently updated
        db: Database session
        
    Returns:
        Update summary
    """
    try:
        # Run in background for large updates
        background_tasks.add_task(
            data_processor.update_hearings,
            force_refresh=force_refresh
        )
        
        return {
            "message": "Hearings update started",
            "force_refresh": force_refresh,
            "status": "processing"
        }
        
    except Exception as e:
        logger.error("Error starting hearings update", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to start hearings update")


@router.post("/update/full")
async def full_update(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Perform full update of all data sources.
    
    Args:
        db: Database session
        
    Returns:
        Update summary
    """
    try:
        # Run in background for large updates
        background_tasks.add_task(data_processor.full_update)
        
        return {
            "message": "Full data update started",
            "status": "processing",
            "updates": ["members", "committees", "hearings"]
        }
        
    except Exception as e:
        logger.error("Error starting full update", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to start full update")


@router.get("/test/congress-api")
async def test_congress_api():
    """
    Test Congress.gov API connection and rate limiting.
    
    Returns:
        API test results
    """
    try:
        # Test basic API connectivity
        members = await data_processor.congress_api.get_members(chamber="house")
        rate_limit_status = data_processor.congress_api.get_rate_limit_status()
        
        return {
            "api_connection": "successful",
            "sample_members_count": len(members),
            "rate_limit_status": rate_limit_status,
            "first_member_sample": members[0] if members else None
        }
        
    except Exception as e:
        logger.error("Error testing Congress API", error=str(e))
        raise HTTPException(status_code=500, detail=f"Congress API test failed: {str(e)}")


@router.get("/test/scrapers")
async def test_scrapers():
    """
    Test web scrapers for House and Senate.
    
    Returns:
        Scraper test results
    """
    try:
        # Test House scraper
        house_results = {"status": "success", "error": None}
        try:
            house_committees = await data_processor.house_scraper.scrape_committees()
            house_results["committees_found"] = len(house_committees)
            house_results["sample_committee"] = house_committees[0] if house_committees else None
        except Exception as e:
            house_results["status"] = "error"
            house_results["error"] = str(e)
        
        # Test Senate scraper  
        senate_results = {"status": "success", "error": None}
        try:
            senate_committees = await data_processor.senate_scraper.scrape_committees()
            senate_results["committees_found"] = len(senate_committees)
            senate_results["sample_committee"] = senate_committees[0] if senate_committees else None
        except Exception as e:
            senate_results["status"] = "error"
            senate_results["error"] = str(e)
        
        return {
            "house_scraper": house_results,
            "senate_scraper": senate_results
        }
        
    except Exception as e:
        logger.error("Error testing scrapers", error=str(e))
        raise HTTPException(status_code=500, detail=f"Scrapers test failed: {str(e)}")


@router.get("/stats/database")
async def database_stats(db: Session = Depends(get_db)):
    """
    Get database statistics.
    
    Args:
        db: Database session
        
    Returns:
        Database statistics
    """
    try:
        from ...models import Member, Committee, Hearing
        
        stats = {
            "members": {
                "total": db.query(Member).count(),
                "house": db.query(Member).filter(Member.chamber == "House").count(),
                "senate": db.query(Member).filter(Member.chamber == "Senate").count(),
                "current": db.query(Member).filter(Member.is_current == True).count(),
            },
            "committees": {
                "total": db.query(Committee).count(),
                "house": db.query(Committee).filter(Committee.chamber == "House").count(),
                "senate": db.query(Committee).filter(Committee.chamber == "Senate").count(),
                "active": db.query(Committee).filter(Committee.is_active == True).count(),
                "subcommittees": db.query(Committee).filter(Committee.is_subcommittee == True).count(),
            },
            "hearings": {
                "total": db.query(Hearing).count(),
                "scheduled": db.query(Hearing).filter(Hearing.status == "Scheduled").count(),
                "completed": db.query(Hearing).filter(Hearing.status == "Completed").count(),
            }
        }
        
        return stats
        
    except Exception as e:
        logger.error("Error getting database stats", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to get database statistics")


@router.get("/members")
async def get_members(
    page: int = 1,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get congressional members using same DB pattern as stats endpoint."""
    try:
        from ...models import Member
        
        offset = (page - 1) * limit
        members = db.query(Member).offset(offset).limit(limit).all()
        
        return [
            {
                "id": m.id,
                "bioguide_id": m.bioguide_id,
                "first_name": m.first_name,
                "last_name": m.last_name,
                "middle_name": m.middle_name,
                "nickname": m.nickname,
                "party": m.party,
                "chamber": m.chamber,
                "state": m.state,
                "district": m.district,
                "is_current": m.is_current,
                "official_photo_url": m.official_photo_url,
                "created_at": m.created_at.isoformat() if m.created_at else None,
                "updated_at": m.updated_at.isoformat() if m.updated_at else None,
                "last_scraped_at": m.last_scraped_at.isoformat() if m.last_scraped_at else None,
            }
            for m in members
        ]
        
    except Exception as e:
        logger.error("Error getting members", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to get members")


@router.get("/committees")
async def get_committees(
    page: int = 1,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get congressional committees using same DB pattern as stats endpoint."""
    try:
        from ...models import Committee
        
        offset = (page - 1) * limit
        committees = db.query(Committee).offset(offset).limit(limit).all()
        
        return [
            {
                "id": c.id,
                "name": c.name,
                "chamber": c.chamber,
                "committee_code": c.committee_code,
                "congress_gov_id": c.congress_gov_id,
                "is_active": c.is_active,
                "is_subcommittee": c.is_subcommittee,
                "parent_committee_id": c.parent_committee_id,
                "website_url": c.website_url,
                "created_at": c.created_at.isoformat() if c.created_at else None,
                "updated_at": c.updated_at.isoformat() if c.updated_at else None,
            }
            for c in committees
        ]
        
    except Exception as e:
        logger.error("Error getting committees", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to get committees")


@router.get("/hearings")
async def get_hearings(
    page: int = 1,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get congressional hearings using same DB pattern as stats endpoint."""
    try:
        from ...models import Hearing
        
        offset = (page - 1) * limit
        hearings = db.query(Hearing).offset(offset).limit(limit).all()
        
        return [
            {
                "id": h.id,
                "congress_gov_id": h.congress_gov_id,
                "title": h.title,
                "description": h.description,
                "committee_id": h.committee_id,
                "scheduled_date": h.scheduled_date.isoformat() if h.scheduled_date else None,
                "start_time": h.start_time.isoformat() if h.start_time else None,
                "end_time": h.end_time.isoformat() if h.end_time else None,
                "location": h.location,
                "room": h.room,
                "hearing_type": h.hearing_type,
                "status": h.status,
                "transcript_url": h.transcript_url,
                "video_url": h.video_url,
                "webcast_url": h.webcast_url,
                "congress_session": h.congress_session,
                "congress_number": h.congress_number,
                "scraped_video_urls": h.scraped_video_urls,
                "created_at": h.created_at.isoformat() if h.created_at else None,
                "updated_at": h.updated_at.isoformat() if h.updated_at else None,
                "last_scraped_at": h.last_scraped_at.isoformat() if h.last_scraped_at else None,
            }
            for h in hearings
        ]
        
    except Exception as e:
        logger.error("Error getting hearings", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to get hearings")


# Data retrieval endpoints
@router.get("/members")
async def get_members(
    page: int = 1,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    Get congressional members.
    
    Args:
        page: Page number (default: 1)
        limit: Items per page (default: 50)
        db: Database session
        
    Returns:
        List of congressional members
    """
    try:
        from ...models import Member
        
        offset = (page - 1) * limit
        members = db.query(Member).offset(offset).limit(limit).all()
        
        # Convert to dict format
        return [
            {
                "id": member.id,
                "bioguide_id": member.bioguide_id,
                "first_name": member.first_name,
                "last_name": member.last_name,
                "middle_name": member.middle_name,
                "party": member.party,
                "chamber": member.chamber,
                "state": member.state,
                "district": member.district,
                "is_current": member.is_current,
                "created_at": member.created_at.isoformat() if member.created_at else None,
                "updated_at": member.updated_at.isoformat() if member.updated_at else None,
            }
            for member in members
        ]
        
    except Exception as e:
        logger.error("Error getting members", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to get members")


@router.get("/committees")
async def get_committees(
    page: int = 1,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    Get congressional committees.
    
    Args:
        page: Page number (default: 1)
        limit: Items per page (default: 50)
        db: Database session
        
    Returns:
        List of congressional committees
    """
    try:
        from ...models import Committee
        
        offset = (page - 1) * limit
        committees = db.query(Committee).offset(offset).limit(limit).all()
        
        # Convert to dict format
        return [
            {
                "id": committee.id,
                "name": committee.name,
                "chamber": committee.chamber,
                "committee_code": committee.committee_code,
                "is_active": committee.is_active,
                "is_subcommittee": committee.is_subcommittee,
                "website_url": committee.website_url,
                "created_at": committee.created_at.isoformat() if committee.created_at else None,
                "updated_at": committee.updated_at.isoformat() if committee.updated_at else None,
            }
            for committee in committees
        ]
        
    except Exception as e:
        logger.error("Error getting committees", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to get committees")


@router.get("/hearings")
async def get_hearings(
    page: int = 1,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    Get congressional hearings.
    
    Args:
        page: Page number (default: 1)
        limit: Items per page (default: 50)
        db: Database session
        
    Returns:
        List of congressional hearings
    """
    try:
        from ...models import Hearing
        
        offset = (page - 1) * limit
        hearings = db.query(Hearing).offset(offset).limit(limit).all()
        
        # Convert to dict format
        return [
            {
                "id": hearing.id,
                "title": hearing.title,
                "description": hearing.description,
                "committee_id": hearing.committee_id,
                "scheduled_date": hearing.scheduled_date.isoformat() if hearing.scheduled_date else None,
                "location": hearing.location,
                "room": hearing.room,
                "status": hearing.status,
                "video_url": hearing.video_url,
                "webcast_url": hearing.webcast_url,
                "created_at": hearing.created_at.isoformat() if hearing.created_at else None,
                "updated_at": hearing.updated_at.isoformat() if hearing.updated_at else None,
            }
            for hearing in hearings
        ]
        
    except Exception as e:
        logger.error("Error getting hearings", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to get hearings")