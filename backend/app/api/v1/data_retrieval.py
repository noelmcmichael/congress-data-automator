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
    chamber: Optional[str] = Query(None, description="Filter by chamber (house/senate)"),
    state: Optional[str] = Query(None, description="Filter by state"),
    party: Optional[str] = Query(None, description="Filter by party"),
    db: Session = Depends(get_db)
):
    """
    Retrieve congressional members with optional filtering
    """
    query = db.query(Member)
    
    # Apply filters
    if chamber:
        query = query.filter(Member.chamber.ilike(f"%{chamber}%"))
    if state:
        query = query.filter(Member.state.ilike(f"%{state}%"))
    if party:
        query = query.filter(Member.party.ilike(f"%{party}%"))
    
    # Apply pagination
    offset = (page - 1) * limit
    members = query.order_by(Member.last_name, Member.first_name).offset(offset).limit(limit).all()
    
    return [MemberResponse.from_orm(member) for member in members]

@router.get("/committees", response_model=List[CommitteeResponse])
async def get_committees(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(50, ge=1, le=200, description="Items per page"),
    chamber: Optional[str] = Query(None, description="Filter by chamber (house/senate)"),
    active_only: bool = Query(True, description="Only return active committees"),
    db: Session = Depends(get_db)
):
    """
    Retrieve congressional committees with optional filtering
    """
    query = db.query(Committee)
    
    # Apply filters
    if chamber:
        query = query.filter(Committee.chamber.ilike(f"%{chamber}%"))
    if active_only:
        query = query.filter(Committee.is_active == True)
    
    # Apply pagination
    offset = (page - 1) * limit
    committees = query.order_by(Committee.name).offset(offset).limit(limit).all()
    
    return [CommitteeResponse.from_orm(committee) for committee in committees]

@router.get("/hearings", response_model=List[HearingResponse])
async def get_hearings(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(50, ge=1, le=200, description="Items per page"),
    status: Optional[str] = Query(None, description="Filter by status (scheduled/completed)"),
    committee_id: Optional[int] = Query(None, description="Filter by committee ID"),
    db: Session = Depends(get_db)
):
    """
    Retrieve congressional hearings with optional filtering
    """
    query = db.query(Hearing)
    
    # Apply filters
    if status:
        query = query.filter(Hearing.status.ilike(f"%{status}%"))
    if committee_id:
        query = query.filter(Hearing.committee_id == committee_id)
    
    # Apply pagination
    offset = (page - 1) * limit
    hearings = query.order_by(desc(Hearing.created_at)).offset(offset).limit(limit).all()
    
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