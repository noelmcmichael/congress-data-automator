"""
import os
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


@router.get("/debug/environment")
async def debug_environment():
    """Debug endpoint to check environment variables."""
    return {
        "congress_api_key_exists": bool(os.getenv("CONGRESS_API_KEY")),
        "congress_api_key_length": len(os.getenv("CONGRESS_API_KEY", "")),
        "congress_api_key_prefix": os.getenv("CONGRESS_API_KEY", "")[:8] if os.getenv("CONGRESS_API_KEY") else None,
        "all_env_vars": list(os.environ.keys()),
        "database_url_exists": bool(os.getenv("DATABASE_URL")),
        "secret_key_exists": bool(os.getenv("SECRET_KEY"))
    }
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
        # Show environment variable status
        env_debug = {
            "congress_api_key_exists": bool(os.getenv("CONGRESS_API_KEY")),
            "congress_api_key_length": len(os.getenv("CONGRESS_API_KEY", "")),
            "congress_api_key_prefix": os.getenv("CONGRESS_API_KEY", "")[:8] if os.getenv("CONGRESS_API_KEY") else None,
            "database_url_exists": bool(os.getenv("DATABASE_URL")),
            "secret_key_exists": bool(os.getenv("SECRET_KEY"))
        }
        
        # Test basic API connectivity
        members = await data_processor.congress_api.get_members(chamber="house")
        rate_limit_status = data_processor.congress_api.get_rate_limit_status()
        
        return {
            "api_connection": "successful",
            "sample_members_count": len(members),
            "rate_limit_status": rate_limit_status,
            "first_member_sample": members[0] if members else None,
            "environment_debug": env_debug
        }
        
    except Exception as e:
        logger.error("Error testing Congress API", error=str(e))
        # Return debug info even on error
        env_debug = {
            "congress_api_key_exists": bool(os.getenv("CONGRESS_API_KEY")),
            "congress_api_key_length": len(os.getenv("CONGRESS_API_KEY", "")),
            "congress_api_key_prefix": os.getenv("CONGRESS_API_KEY", "")[:8] if os.getenv("CONGRESS_API_KEY") else None,
            "database_url_exists": bool(os.getenv("DATABASE_URL")),
            "secret_key_exists": bool(os.getenv("SECRET_KEY"))
        }
        raise HTTPException(status_code=500, detail=f"Congress API test failed: {str(e)}", headers={"X-Debug-Info": str(env_debug)})


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


@router.post("/populate/test-relationships")
async def populate_test_relationships(
    db: Session = Depends(get_db)
):
    """
    Populate test relationship data for demonstration purposes.
    
    Args:
        db: Database session
        
    Returns:
        Population results
    """
    try:
        import random
        from datetime import datetime
        from ...models.member import Member
        from ...models.committee import Committee, CommitteeMembership
        
        # Get ALL members and committees (not just first 20)
        members = db.query(Member).all()
        committees = db.query(Committee).all()
        
        if not members or not committees:
            return {
                "error": "No members or committees found in database",
                "members_count": len(members),
                "committees_count": len(committees)
            }
        
        # Clear existing relationships first
        db.query(CommitteeMembership).delete()
        db.commit()
        
        # Create test relationships for current members
        relationships_created = 0
        
        # Use first 50 members to avoid overwhelming the system
        for i, member in enumerate(members[:50]):
            # Assign each member to 1-2 random committees
            num_committees = random.randint(1, min(2, len(committees)))
            assigned_committees = random.sample(committees, num_committees)
            
            for j, committee in enumerate(assigned_committees):
                # Determine position
                if j == 0 and i < 10:  # First 10 members get chair positions
                    position = "Chair"
                elif j == 0 and i < 20:  # Next 10 get ranking member
                    position = "Ranking Member"
                else:
                    position = "Member"
                
                # Create membership
                membership = CommitteeMembership(
                    member_id=member.id,
                    committee_id=committee.id,
                    position=position,
                    is_current=True,
                    start_date=datetime.now()
                )
                
                db.add(membership)
                relationships_created += 1
        
        # Commit changes
        db.commit()
        
        return {
            "message": "Test relationship data created successfully",
            "relationships_created": relationships_created,
            "members_processed": min(50, len(members)),
            "committees_available": len(committees),
            "status": "completed"
        }
        
    except Exception as e:
        logger.error("Error creating test relationships", error=str(e))
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create test relationships: {str(e)}")

@router.post("/populate/relationships")
async def populate_relationships(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Populate relationship data (committee memberships, hierarchies, hearing associations).
    
    Args:
        background_tasks: Background task executor
        db: Database session
        
    Returns:
        Population status
    """
    try:
        from ...services.relationship_data_collector import populate_all_relationship_data
        
        # Run in background for large operations
        background_tasks.add_task(
            populate_all_relationship_data,
            db
        )
        
        return {
            "message": "Relationship data population started",
            "status": "processing",
            "operations": [
                "committee_memberships",
                "committee_hierarchies", 
                "hearing_associations"
            ]
        }
        
    except Exception as e:
        logger.error("Error starting relationship data population", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to start relationship data population")


# REMOVED DUPLICATE /members, /committees, /hearings endpoints
# These were overriding the advanced filtering endpoints in data_retrieval.py
# Using the ones in data_retrieval.py which have proper search and filtering capabilities