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


# REMOVED DUPLICATE /members endpoint - using the one in data_retrieval.py with filtering
# This endpoint was overriding the advanced filtering endpoint in data_retrieval.py


# REMOVED DUPLICATE /committees endpoint - using the one in data_retrieval.py with filtering
# This endpoint was overriding the advanced filtering endpoint in data_retrieval.py


# REMOVED DUPLICATE /hearings endpoint - using the one in data_retrieval.py with filtering
# This endpoint was overriding the advanced filtering endpoint in data_retrieval.py


# REMOVED DUPLICATE /members endpoint - using the one in data_retrieval.py with filtering
# This endpoint was overriding the advanced filtering endpoint in data_retrieval.py

# REMOVED DUPLICATE /committees and /hearings endpoints
# These were overriding the advanced filtering endpoints in data_retrieval.py
# Using the ones in data_retrieval.py which have proper search and filtering capabilities