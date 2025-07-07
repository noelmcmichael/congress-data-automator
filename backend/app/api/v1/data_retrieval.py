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
        "message": "FINAL DEPLOYMENT - Duplicate endpoints removed",
        "timestamp": "2025-07-06T16:00:00Z",
        "version": "filter-fix-final",
        "fix": "Removed duplicate endpoints from data_updates.py",
        "deployment": "Should now use data_retrieval.py endpoints with filtering"
    }

@router.get("/test-members-endpoint")
async def test_members_endpoint(
    party: Optional[str] = Query(None, description="Filter by party"),
    db: Session = Depends(get_db)
):
    """
    Test endpoint to verify if the get_members function logic is accessible
    """
    print(f"🎯 TEST ENDPOINT: test_members_endpoint called with party={party}")
    logger.error(f"🎯 TEST ENDPOINT: test_members_endpoint called with party={party}")
    
    # Call the exact same function that should be called by /members
    result = await get_members(party=party, db=db)
    
    return {
        "message": "This is calling the SAME get_members function",
        "party_filter": party,
        "result_count": len(result),
        "first_member": result[0].dict() if result else None
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

@router.get("/members", response_model=List[dict])
async def get_members_new_version(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(50, ge=1, le=200, description="Items per page"),
    search: Optional[str] = Query(None, description="Search by name"),
    chamber: Optional[str] = Query(None, description="Filter by chamber (house/senate)"),
    state: Optional[str] = Query(None, description="Filter by state"),
    party: Optional[str] = Query(None, description="Filter by party"),
    sort_by: Optional[str] = Query("last_name", description="Sort by field (last_name, first_name, state, party)"),
    sort_order: Optional[str] = Query("asc", description="Sort order (asc/desc)"),
    include_committees: bool = Query(False, description="Include committee summary information"),
    db: Session = Depends(get_db)
):
    """
    Retrieve congressional members with search, filtering, and sorting
    Enhanced with optional committee information
    """
    logger.info(f"get_members called with params: page={page}, limit={limit}, search={search}, chamber={chamber}, state={state}, party={party}, sort_by={sort_by}, sort_order={sort_order}, include_committees={include_committees}")
    
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
    
    logger.info(f"Executing SQL with params: {params}")
    
    # Execute the query
    result = db.execute(sql, params).fetchall()
    
    logger.info(f"Raw SQL returned {len(result)} members")
    
    # Convert to response format
    members_response = []
    for row in result:
        member_data = {
            "id": row[0],
            "bioguide_id": row[1],
            "congress_gov_id": row[2],
            "first_name": row[3],
            "last_name": row[4],
            "middle_name": row[5],
            "suffix": row[6],
            "nickname": row[7],
            "party": row[8],
            "chamber": row[9],
            "state": row[10],
            "district": row[11],
            "term_start": row[12],
            "term_end": row[13],
            "is_current": row[14],
            "phone": row[15],
            "email": row[16],
            "website": row[17],
            "birth_date": row[18],
            "birth_state": row[19],
            "birth_city": row[20],
            "official_photo_url": row[21],
            "created_at": row[22],
            "updated_at": row[23],
            "last_scraped_at": row[24]
        }
        
        # Add committee information if requested
        if include_committees:
            # Get committee memberships for this member
            committee_sql = text("""
                SELECT c.id, c.name, c.chamber, c.committee_type, c.is_subcommittee, 
                       cm.position, cm.is_current
                FROM committee_memberships cm
                JOIN committees c ON cm.committee_id = c.id
                WHERE cm.member_id = :member_id AND cm.is_current = true
                ORDER BY c.name
            """)
            
            committee_result = db.execute(committee_sql, {"member_id": row[0]}).fetchall()
            
            committees = []
            leadership_count = 0
            
            for comm_row in committee_result:
                committee_info = {
                    "id": comm_row[0],
                    "name": comm_row[1],
                    "chamber": comm_row[2],
                    "committee_type": comm_row[3],
                    "is_subcommittee": comm_row[4],
                    "position": comm_row[5],
                    "is_current": comm_row[6]
                }
                committees.append(committee_info)
                
                # Count leadership positions
                if comm_row[5] and comm_row[5].lower() in ['chair', 'ranking member', 'chairwoman', 'chairman']:
                    leadership_count += 1
            
            member_data["committees"] = committees
            member_data["committee_summary"] = {
                "total_committees": len(committees),
                "leadership_positions": leadership_count,
                "standing_committees": len([c for c in committees if not c["is_subcommittee"]]),
                "subcommittees": len([c for c in committees if c["is_subcommittee"]])
            }
        
        members_response.append(member_data)
    
    if members_response:
        logger.info(f"First member: {members_response[0]['first_name']} {members_response[0]['last_name']} ({members_response[0]['party']}, {members_response[0]['chamber']}, {members_response[0]['state']})")
    
    return members_response

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

@router.get("/members/{member_id}/enhanced", response_model=dict)
async def get_member_enhanced(member_id: int, db: Session = Depends(get_db)):
    """
    Retrieve enhanced member information including committee memberships and leadership roles
    """
    from sqlalchemy.orm import joinedload
    from app.models.committee import CommitteeMembership
    
    # Get member with committee memberships
    member = db.query(Member).options(
        joinedload(Member.committee_memberships).joinedload(CommitteeMembership.committee)
    ).filter(Member.id == member_id).first()
    
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    # Build enhanced response
    committee_memberships = []
    leadership_positions = []
    
    for cm in member.committee_memberships:
        membership_data = {
            "id": cm.id,
            "committee": {
                "id": cm.committee.id,
                "name": cm.committee.name,
                "chamber": cm.committee.chamber,
                "committee_type": cm.committee.committee_type,
                "is_subcommittee": cm.committee.is_subcommittee,
                "parent_committee_id": cm.committee.parent_committee_id
            },
            "position": cm.position,
            "is_current": cm.is_current,
            "start_date": cm.start_date,
            "end_date": cm.end_date
        }
        committee_memberships.append(membership_data)
        
        # Track leadership positions
        if cm.position and cm.position.lower() in ['chair', 'ranking member', 'chairwoman', 'chairman']:
            leadership_positions.append({
                "committee_name": cm.committee.name,
                "position": cm.position,
                "is_current": cm.is_current
            })
    
    # Calculate term information
    term_info = {
        "current_term_start": member.term_start,
        "current_term_end": member.term_end,
        "is_current": member.is_current
    }
    
    # Add senate-specific term class information
    if member.chamber == "Senate":
        # Calculate term class based on term end year
        if member.term_end:
            year = member.term_end.year
            if year % 6 == 1:  # 2025, 2031, etc.
                term_class = "I"
                next_election = 2024
            elif year % 6 == 3:  # 2027, 2033, etc.
                term_class = "II"
                next_election = 2026
            else:  # 2029, 2035, etc.
                term_class = "III"
                next_election = 2028
            
            term_info.update({
                "senate_class": term_class,
                "next_election_year": next_election
            })
    
    # Build statistics
    stats = {
        "total_committees": len(committee_memberships),
        "current_committees": len([cm for cm in committee_memberships if cm["is_current"]]),
        "leadership_positions": len(leadership_positions),
        "current_leadership": len([lp for lp in leadership_positions if lp["is_current"]]),
        "standing_committees": len([cm for cm in committee_memberships if not cm["committee"]["is_subcommittee"]]),
        "subcommittees": len([cm for cm in committee_memberships if cm["committee"]["is_subcommittee"]])
    }
    
    return {
        "member": MemberResponse.from_orm(member).model_dump(),
        "committee_memberships": committee_memberships,
        "leadership_positions": leadership_positions,
        "term_information": term_info,
        "statistics": stats
    }

@router.get("/committees/{committee_id}", response_model=CommitteeResponse)
async def get_committee(committee_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific committee by ID
    """
    committee = db.query(Committee).filter(Committee.id == committee_id).first()
    if not committee:
        raise HTTPException(status_code=404, detail="Committee not found")
    
    return CommitteeResponse.from_orm(committee)

@router.get("/committees/{committee_id}/hierarchy", response_model=dict)
async def get_committee_hierarchy(committee_id: int, db: Session = Depends(get_db)):
    """
    Get complete committee hierarchy including subcommittees and member information
    """
    from sqlalchemy import text
    
    # Get the main committee
    main_committee_sql = text("""
        SELECT id, name, chamber, committee_type, is_subcommittee, parent_committee_id, 
               jurisdiction, chair_member_id, ranking_member_id, is_active
        FROM committees 
        WHERE id = :committee_id
    """)
    
    main_result = db.execute(main_committee_sql, {"committee_id": committee_id}).fetchone()
    
    if not main_result:
        raise HTTPException(status_code=404, detail="Committee not found")
    
    # Get subcommittees
    sub_sql = text("""
        SELECT id, name, chamber, committee_type, is_subcommittee, parent_committee_id, 
               jurisdiction, chair_member_id, ranking_member_id, is_active
        FROM committees 
        WHERE parent_committee_id = :committee_id
        ORDER BY name
    """)
    
    subcommittees = db.execute(sub_sql, {"committee_id": committee_id}).fetchall()
    
    # Get committee members
    members_sql = text("""
        SELECT m.id, m.first_name, m.last_name, m.party, m.state, m.chamber, m.district,
               cm.position, cm.is_current, m.official_photo_url
        FROM committee_memberships cm
        JOIN members m ON cm.member_id = m.id
        WHERE cm.committee_id = :committee_id AND cm.is_current = true
        ORDER BY 
            CASE 
                WHEN cm.position = 'Chair' THEN 1
                WHEN cm.position = 'Ranking Member' THEN 2
                ELSE 3
            END,
            m.last_name
    """)
    
    members = db.execute(members_sql, {"committee_id": committee_id}).fetchall()
    
    # Build response
    committee_data = {
        "id": main_result[0],
        "name": main_result[1],
        "chamber": main_result[2],
        "committee_type": main_result[3],
        "is_subcommittee": main_result[4],
        "parent_committee_id": main_result[5],
        "jurisdiction": main_result[6],
        "chair_member_id": main_result[7],
        "ranking_member_id": main_result[8],
        "is_active": main_result[9]
    }
    
    # Process subcommittees
    subcommittee_data = []
    for sub in subcommittees:
        # Get subcommittee members
        sub_members_sql = text("""
            SELECT m.id, m.first_name, m.last_name, m.party, m.state, m.chamber, m.district,
                   cm.position, cm.is_current, m.official_photo_url
            FROM committee_memberships cm
            JOIN members m ON cm.member_id = m.id
            WHERE cm.committee_id = :sub_committee_id AND cm.is_current = true
            ORDER BY 
                CASE 
                    WHEN cm.position = 'Chair' THEN 1
                    WHEN cm.position = 'Ranking Member' THEN 2
                    ELSE 3
                END,
                m.last_name
        """)
        
        sub_members = db.execute(sub_members_sql, {"sub_committee_id": sub[0]}).fetchall()
        
        subcommittee_data.append({
            "id": sub[0],
            "name": sub[1],
            "chamber": sub[2],
            "committee_type": sub[3],
            "is_subcommittee": sub[4],
            "parent_committee_id": sub[5],
            "jurisdiction": sub[6],
            "chair_member_id": sub[7],
            "ranking_member_id": sub[8],
            "is_active": sub[9],
            "members": [{
                "id": m[0],
                "first_name": m[1],
                "last_name": m[2],
                "party": m[3],
                "state": m[4],
                "chamber": m[5],
                "district": m[6],
                "position": m[7],
                "is_current": m[8],
                "official_photo_url": m[9]
            } for m in sub_members],
            "member_count": len(sub_members)
        })
    
    # Process main committee members
    member_data = []
    for m in members:
        member_data.append({
            "id": m[0],
            "first_name": m[1],
            "last_name": m[2],
            "party": m[3],
            "state": m[4],
            "chamber": m[5],
            "district": m[6],
            "position": m[7],
            "is_current": m[8],
            "official_photo_url": m[9]
        })
    
    # Calculate statistics
    party_breakdown = {}
    for member in member_data:
        party = member["party"]
        if party not in party_breakdown:
            party_breakdown[party] = 0
        party_breakdown[party] += 1
    
    leadership_positions = [m for m in member_data if m["position"] and m["position"].lower() in ['chair', 'ranking member', 'chairwoman', 'chairman']]
    
    return {
        "committee": committee_data,
        "members": member_data,
        "subcommittees": subcommittee_data,
        "statistics": {
            "total_members": len(member_data),
            "total_subcommittees": len(subcommittee_data),
            "party_breakdown": party_breakdown,
            "leadership_positions": len(leadership_positions),
            "total_subcommittee_members": sum(sub["member_count"] for sub in subcommittee_data)
        }
    }

@router.get("/hearings/{hearing_id}", response_model=HearingResponse)
async def get_hearing(hearing_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific hearing by ID
    """
    hearing = db.query(Hearing).filter(Hearing.id == hearing_id).first()
    if not hearing:
        raise HTTPException(status_code=404, detail="Hearing not found")
    
    return HearingResponse.from_orm(hearing)

@router.get("/senators/by-term-class", response_model=dict)
async def get_senators_by_term_class(db: Session = Depends(get_db)):
    """
    Get senators organized by term class for re-election timeline analysis
    """
    from sqlalchemy import text
    
    # Get all current senators with their term information
    sql = text("""
        SELECT id, bioguide_id, first_name, last_name, middle_name, party, state, 
               term_start, term_end, official_photo_url
        FROM members 
        WHERE chamber = 'Senate' AND is_current = true
        ORDER BY state, last_name
    """)
    
    result = db.execute(sql).fetchall()
    
    # Organize by term class
    class_i_senators = []  # Up for re-election in 2024 (term ends 2025)
    class_ii_senators = []  # Up for re-election in 2026 (term ends 2027)
    class_iii_senators = []  # Up for re-election in 2028 (term ends 2029)
    
    for row in result:
        senator_data = {
            "id": row[0],
            "bioguide_id": row[1],
            "first_name": row[2],
            "last_name": row[3],
            "middle_name": row[4],
            "party": row[5],
            "state": row[6],
            "term_start": row[7],
            "term_end": row[8],
            "official_photo_url": row[9]
        }
        
        # Determine term class based on term end year
        if row[8]:  # term_end
            year = row[8].year
            if year % 6 == 1:  # 2025, 2031, etc.
                senator_data["term_class"] = "I"
                senator_data["next_election_year"] = 2024
                class_i_senators.append(senator_data)
            elif year % 6 == 3:  # 2027, 2033, etc.
                senator_data["term_class"] = "II"
                senator_data["next_election_year"] = 2026
                class_ii_senators.append(senator_data)
            else:  # 2029, 2035, etc.
                senator_data["term_class"] = "III"
                senator_data["next_election_year"] = 2028
                class_iii_senators.append(senator_data)
    
    # Calculate statistics
    party_breakdown = {}
    for senator_list in [class_i_senators, class_ii_senators, class_iii_senators]:
        for senator in senator_list:
            party = senator["party"]
            if party not in party_breakdown:
                party_breakdown[party] = {"total": 0, "class_i": 0, "class_ii": 0, "class_iii": 0}
            party_breakdown[party]["total"] += 1
            
            if senator["term_class"] == "I":
                party_breakdown[party]["class_i"] += 1
            elif senator["term_class"] == "II":
                party_breakdown[party]["class_ii"] += 1
            elif senator["term_class"] == "III":
                party_breakdown[party]["class_iii"] += 1
    
    return {
        "term_classes": {
            "class_i": {
                "description": "Up for re-election in 2024 (term ends 2025)",
                "next_election_year": 2024,
                "senators": class_i_senators,
                "count": len(class_i_senators)
            },
            "class_ii": {
                "description": "Up for re-election in 2026 (term ends 2027)",
                "next_election_year": 2026,
                "senators": class_ii_senators,
                "count": len(class_ii_senators)
            },
            "class_iii": {
                "description": "Up for re-election in 2028 (term ends 2029)",
                "next_election_year": 2028,
                "senators": class_iii_senators,
                "count": len(class_iii_senators)
            }
        },
        "party_breakdown": party_breakdown,
        "statistics": {
            "total_senators": len(class_i_senators) + len(class_ii_senators) + len(class_iii_senators),
            "elections_2024": len(class_i_senators),
            "elections_2026": len(class_ii_senators),
            "elections_2028": len(class_iii_senators)
        }
    }