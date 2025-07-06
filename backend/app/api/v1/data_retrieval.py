"""
Data retrieval endpoints for Congressional Data API
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.core.database import get_db
from app.models.member import Member
from app.models.committee import Committee
from app.models.hearing import Hearing
from app.schemas.member import MemberResponse
from app.schemas.committee import CommitteeResponse
from app.schemas.hearing import HearingResponse

router = APIRouter()

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
    # Debug logging to verify parameters are received
    print(f"DEBUG: get_members called with params: page={page}, limit={limit}, search={search}, chamber={chamber}, state={state}, party={party}, sort_by={sort_by}, sort_order={sort_order}")
    
    query = db.query(Member)
    
    # Apply search
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (Member.first_name.ilike(search_term)) |
            (Member.last_name.ilike(search_term)) |
            (Member.middle_name.ilike(search_term)) |
            (Member.nickname.ilike(search_term))
        )
    
    # Apply filters (exact match for better accuracy)
    if chamber:
        print(f"DEBUG: Applying chamber filter: {chamber}")
        query = query.filter(Member.chamber == chamber)
    if state:
        print(f"DEBUG: Applying state filter: {state}")
        query = query.filter(Member.state == state)
    if party:
        print(f"DEBUG: Applying party filter: {party}")
        query = query.filter(Member.party == party)
    
    # Apply sorting
    sort_column = getattr(Member, sort_by, Member.last_name)
    if sort_order.lower() == "desc":
        query = query.order_by(desc(sort_column))
    else:
        query = query.order_by(sort_column)
    
    # Apply pagination
    offset = (page - 1) * limit
    members = query.offset(offset).limit(limit).all()
    
    print(f"DEBUG: Returning {len(members)} members")
    if members:
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