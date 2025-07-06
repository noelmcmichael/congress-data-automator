"""
Data retrieval endpoints for Congressional Data API
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
import logging

from app.core.database import get_db
from app.models.member import Member
from app.models.committee import Committee
from app.models.hearing import Hearing
from app.schemas.member import MemberResponse
from app.schemas.committee import CommitteeResponse
from app.schemas.hearing import HearingResponse

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/debug-test")
async def debug_test():
    """Debug test endpoint to verify we're hitting the right service"""
    return {
        "message": "This is the FIXED version with raw SQL filtering",
        "timestamp": "2025-07-06T15:45:00Z",
        "version": "filter-fix-v3",
        "fix": "Raw SQL implementation replacing broken ORM filtering",
        "deployment": "Testing if new code is deployed"
    }

@router.get("/debug-raw-sql")
async def debug_raw_sql(
    party: Optional[str] = Query(None, description="Filter by party"),
    db: Session = Depends(get_db)
):
    """Debug endpoint to test raw SQL queries"""
    from sqlalchemy import text
    
    logger.info(f"DEBUG: debug_raw_sql called with party={party}")
    print(f"DEBUG: debug_raw_sql called with party={party}")
    
    try:
        # Test raw SQL query
        if party:
            sql = text("SELECT COUNT(*) FROM members WHERE party = :party")
            result = db.execute(sql, {"party": party}).scalar()
            
            # Get a few sample members
            sql_sample = text("SELECT first_name, last_name, party, chamber, state FROM members WHERE party = :party LIMIT 5")
            sample_result = db.execute(sql_sample, {"party": party}).fetchall()
            
            return {
                "message": "Raw SQL test with party filter",
                "party": party,
                "count": result,
                "sample_members": [
                    {
                        "first_name": row[0],
                        "last_name": row[1], 
                        "party": row[2],
                        "chamber": row[3],
                        "state": row[4]
                    } for row in sample_result
                ]
            }
        else:
            # Test without filter
            sql = text("SELECT COUNT(*) FROM members")
            result = db.execute(sql).scalar()
            
            return {
                "message": "Raw SQL test without filter",
                "total_count": result
            }
    except Exception as e:
        logger.error(f"DEBUG: Error in debug_raw_sql: {e}")
        print(f"DEBUG: Error in debug_raw_sql: {e}")
        return {
            "error": str(e),
            "message": "Error executing raw SQL"
        }

@router.get("/members-test")
async def get_members_test():
    """Test endpoint to verify the new code is running"""
    logger.info("DEBUG: get_members_test called - NEW CODE IS RUNNING!")
    print("DEBUG: get_members_test called - NEW CODE IS RUNNING!")
    return {
        "message": "NEW CODE IS RUNNING - Raw SQL implementation",
        "timestamp": "2025-07-06T15:45:00Z",
        "status": "TESTING DEPLOYMENT"
    }

@router.get("/members-fixed")
async def get_members_fixed(
    party: Optional[str] = Query(None, description="Filter by party"),
    db: Session = Depends(get_db)
):
    """
    NEW ENDPOINT: Test the exact same raw SQL logic as in get_members
    This will help us determine if the issue is with routing or logic
    """
    print(f"🚨 FIXED ENDPOINT: get_members_fixed called with party={party}")
    logger.error(f"🚨 FIXED ENDPOINT: get_members_fixed called with party={party}")
    
    from sqlalchemy import text
    
    if party:
        sql = text("SELECT id, first_name, last_name, party, chamber, state FROM members WHERE party = :party LIMIT 5")
        result = db.execute(sql, {"party": party}).fetchall()
        
        members_data = []
        for row in result:
            members_data.append({
                "id": row[0],
                "first_name": row[1],
                "last_name": row[2],
                "party": row[3],
                "chamber": row[4],
                "state": row[5]
            })
        
        return {
            "message": f"Fixed endpoint with party filter: {party}",
            "count": len(members_data),
            "members": members_data
        }
    else:
        sql = text("SELECT COUNT(*) FROM members")
        total = db.execute(sql).scalar()
        return {
            "message": "Fixed endpoint without filter",
            "total_members": total
        }

@router.get("/members", response_model=List[MemberResponse])
async def get_members(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(50, ge=1, le=200, description="Items per page"),
    search: Optional[str] = Query(None, description="Search by name"),
    chamber: Optional[str] = Query(None, description="Filter by chamber (house/senate)"),
    state: Optional[str] = Query(None, description="Filter by state"),
    party: Optional[str] = Query(None, description="Filter by party"),
    sort_by: Optional[str] = Query("last_name", description="Sort by field (last_name, first_name, state, party)"),
    sort_order: Optional[str] = Query("asc", description="Sort order (asc/desc)"),
    db: Session = Depends(get_db)
):
    """
    Retrieve congressional members with search, filtering, and sorting
    """
    # CRITICAL DEBUG - MUST APPEAR IN LOGS
    print("🚨 CRITICAL DEBUG: get_members function called - NEW VERSION!")
    logger.error(f"🚨 CRITICAL DEBUG: get_members called with party={party}")
    
    # Debug logging to verify parameters are received
    logger.info(f"DEBUG: get_members called with params: page={page}, limit={limit}, search={search}, chamber={chamber}, state={state}, party={party}, sort_by={sort_by}, sort_order={sort_order}")
    print(f"DEBUG: get_members called with params: page={page}, limit={limit}, search={search}, chamber={chamber}, state={state}, party={party}, sort_by={sort_by}, sort_order={sort_order}")
    
    # TEMPORARY FIX: Use raw SQL instead of ORM since ORM filtering is broken
    from sqlalchemy import text
    
    # Build WHERE clause
    where_conditions = []
    params = {}
    
    if search:
        search_term = f"%{search}%"
        where_conditions.append("(first_name ILIKE :search OR last_name ILIKE :search OR middle_name ILIKE :search OR nickname ILIKE :search)")
        params["search"] = search_term
    
    if chamber:
        where_conditions.append("chamber = :chamber")
        params["chamber"] = chamber
    
    if state:
        where_conditions.append("state = :state")
        params["state"] = state
    
    if party:
        where_conditions.append("party = :party")
        params["party"] = party
    
    # Build ORDER BY clause
    order_by = "last_name"
    if sort_by in ["first_name", "last_name", "state", "party", "chamber"]:
        order_by = sort_by
    
    if sort_order.lower() == "desc":
        order_by += " DESC"
    else:
        order_by += " ASC"
    
    # Build complete SQL
    where_clause = " AND ".join(where_conditions) if where_conditions else "1=1"
    offset = (page - 1) * limit
    
    sql = text(f"""
        SELECT id, bioguide_id, congress_gov_id, first_name, last_name, middle_name, 
               suffix, nickname, party, chamber, state, district, term_start, term_end, 
               is_current, phone, email, website, birth_date, birth_state, birth_city, 
               official_photo_url, created_at, updated_at, last_scraped_at
        FROM members 
        WHERE {where_clause}
        ORDER BY {order_by}
        LIMIT :limit OFFSET :offset
    """)
    
    params.update({"limit": limit, "offset": offset})
    
    logger.info(f"DEBUG: Executing raw SQL with params: {params}")
    print(f"DEBUG: Executing raw SQL with params: {params}")
    
    # Execute the query
    result = db.execute(sql, params).fetchall()
    
    logger.info(f"DEBUG: Raw SQL returned {len(result)} members")
    print(f"DEBUG: Raw SQL returned {len(result)} members")
    
    # Convert to Member objects
    members = []
    for row in result:
        member = Member()
        member.id = row[0]
        member.bioguide_id = row[1]
        member.congress_gov_id = row[2]
        member.first_name = row[3]
        member.last_name = row[4]
        member.middle_name = row[5]
        member.suffix = row[6]
        member.nickname = row[7]
        member.party = row[8]
        member.chamber = row[9]
        member.state = row[10]
        member.district = row[11]
        member.term_start = row[12]
        member.term_end = row[13]
        member.is_current = row[14]
        member.phone = row[15]
        member.email = row[16]
        member.website = row[17]
        member.birth_date = row[18]
        member.birth_state = row[19]
        member.birth_city = row[20]
        member.official_photo_url = row[21]
        member.created_at = row[22]
        member.updated_at = row[23]
        member.last_scraped_at = row[24]
        members.append(member)
    
    if members:
        logger.info(f"DEBUG: First member: {members[0].first_name} {members[0].last_name} ({members[0].party}, {members[0].chamber}, {members[0].state})")
        print(f"DEBUG: First member: {members[0].first_name} {members[0].last_name} ({members[0].party}, {members[0].chamber}, {members[0].state})")
    
    return [MemberResponse.from_orm(member) for member in members]

@router.get("/committees", response_model=List[CommitteeResponse])
async def get_committees(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(50, ge=1, le=200, description="Items per page"),
    search: Optional[str] = Query(None, description="Search by committee name"),
    chamber: Optional[str] = Query(None, description="Filter by chamber (house/senate)"),
    active_only: bool = Query(True, description="Only return active committees"),
    sort_by: Optional[str] = Query("name", description="Sort by field (name, chamber)"),
    sort_order: Optional[str] = Query("asc", description="Sort order (asc/desc)"),
    db: Session = Depends(get_db)
):
    """
    Retrieve congressional committees with search, filtering, and sorting
    """
    query = db.query(Committee)
    
    # Apply search
    if search:
        search_term = f"%{search}%"
        query = query.filter(Committee.name.ilike(search_term))
    
    # Apply filters (exact match for better accuracy)
    if chamber:
        query = query.filter(Committee.chamber == chamber)
    if active_only:
        query = query.filter(Committee.is_active == True)
    
    # Apply sorting
    sort_column = getattr(Committee, sort_by, Committee.name)
    if sort_order.lower() == "desc":
        query = query.order_by(desc(sort_column))
    else:
        query = query.order_by(sort_column)
    
    # Apply pagination
    offset = (page - 1) * limit
    committees = query.offset(offset).limit(limit).all()
    
    return [CommitteeResponse.from_orm(committee) for committee in committees]

@router.get("/hearings", response_model=List[HearingResponse])
async def get_hearings(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(50, ge=1, le=200, description="Items per page"),
    search: Optional[str] = Query(None, description="Search by hearing title"),
    status: Optional[str] = Query(None, description="Filter by status (scheduled/completed)"),
    committee_id: Optional[int] = Query(None, description="Filter by committee ID"),
    sort_by: Optional[str] = Query("scheduled_date", description="Sort by field (title, scheduled_date, created_at)"),
    sort_order: Optional[str] = Query("desc", description="Sort order (asc/desc)"),
    db: Session = Depends(get_db)
):
    """
    Retrieve congressional hearings with search, filtering, and sorting
    """
    query = db.query(Hearing)
    
    # Apply search
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (Hearing.title.ilike(search_term)) |
            (Hearing.description.ilike(search_term))
        )
    
    # Apply filters (exact match for better accuracy)
    if status:
        query = query.filter(Hearing.status == status)
    if committee_id:
        query = query.filter(Hearing.committee_id == committee_id)
    
    # Apply sorting
    sort_column = getattr(Hearing, sort_by, Hearing.scheduled_date)
    if sort_order.lower() == "desc":
        query = query.order_by(desc(sort_column))
    else:
        query = query.order_by(sort_column)
    
    # Apply pagination
    offset = (page - 1) * limit
    hearings = query.offset(offset).limit(limit).all()
    
    return [HearingResponse.from_orm(hearing) for hearing in hearings]

@router.get("/members/{member_id}", response_model=MemberResponse)
async def get_member(member_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific member by ID
    """
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    return MemberResponse.from_orm(member)

@router.get("/committees/{committee_id}", response_model=CommitteeResponse)
async def get_committee(committee_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific committee by ID
    """
    committee = db.query(Committee).filter(Committee.id == committee_id).first()
    if not committee:
        raise HTTPException(status_code=404, detail="Committee not found")
    
    return CommitteeResponse.from_orm(committee)

@router.get("/hearings/{hearing_id}", response_model=HearingResponse)
async def get_hearing(hearing_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific hearing by ID
    """
    hearing = db.query(Hearing).filter(Hearing.id == hearing_id).first()
    if not hearing:
        raise HTTPException(status_code=404, detail="Hearing not found")
    
    return HearingResponse.from_orm(hearing)