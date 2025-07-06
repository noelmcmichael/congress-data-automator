"""
API endpoints for relationship and detail data.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from ...core.database import get_db
from ...models.member import Member
from ...models.committee import Committee, CommitteeMembership
from ...models.hearing import Hearing, Witness, HearingDocument
from ...schemas.relationships import (
    MemberDetailResponse,
    CommitteeDetailResponse,
    HearingDetailResponse,
    MemberCommitteeResponse,
    CommitteeMemberResponse,
    CommitteeHearingResponse
)
from ...schemas.committee import CommitteeResponse

router = APIRouter()

@router.get("/members/{member_id}/detail", response_model=MemberDetailResponse)
async def get_member_detail(
    member_id: int,
    db: Session = Depends(get_db)
):
    """
    Get detailed information about a specific member including committees and hearings.
    """
    member = db.query(Member).options(
        joinedload(Member.committee_memberships).joinedload(CommitteeMembership.committee)
    ).filter(Member.id == member_id).first()
    
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    # Get recent hearings for committees this member is on
    committee_ids = [cm.committee_id for cm in member.committee_memberships]
    recent_hearings = db.query(Hearing).filter(
        Hearing.committee_id.in_(committee_ids)
    ).order_by(Hearing.scheduled_date.desc()).limit(10).all()
    
    return MemberDetailResponse(
        member=member,
        committee_memberships=[
            MemberCommitteeResponse(
                committee=cm.committee,
                position=cm.position,
                is_current=cm.is_current,
                start_date=cm.start_date,
                end_date=cm.end_date
            )
            for cm in member.committee_memberships
        ],
        recent_hearings=recent_hearings,
        statistics={
            "total_committees": len(member.committee_memberships),
            "chair_positions": len([cm for cm in member.committee_memberships if cm.position == "Chair"]),
            "current_memberships": len([cm for cm in member.committee_memberships if cm.is_current])
        }
    )

@router.get("/committees/{committee_id}/detail", response_model=CommitteeDetailResponse)
async def get_committee_detail(
    committee_id: int,
    db: Session = Depends(get_db)
):
    """
    Get detailed information about a specific committee including members and hearings.
    """
    committee = db.query(Committee).options(
        joinedload(Committee.memberships).joinedload(CommitteeMembership.member),
        joinedload(Committee.subcommittees),
        joinedload(Committee.parent_committee),
        joinedload(Committee.chair),
        joinedload(Committee.ranking_member)
    ).filter(Committee.id == committee_id).first()
    
    if not committee:
        raise HTTPException(status_code=404, detail="Committee not found")
    
    # Get recent hearings
    recent_hearings = db.query(Hearing).filter(
        Hearing.committee_id == committee_id
    ).order_by(Hearing.scheduled_date.desc()).limit(20).all()
    
    return CommitteeDetailResponse(
        committee=committee,
        memberships=[
            CommitteeMemberResponse(
                member=cm.member,
                position=cm.position,
                is_current=cm.is_current,
                start_date=cm.start_date,
                end_date=cm.end_date
            )
            for cm in committee.memberships
        ],
        subcommittees=committee.subcommittees,
        recent_hearings=recent_hearings,
        statistics={
            "total_members": len(committee.memberships),
            "current_members": len([cm for cm in committee.memberships if cm.is_current]),
            "total_hearings": len(recent_hearings),
            "subcommittee_count": len(committee.subcommittees)
        }
    )

@router.get("/hearings/{hearing_id}/detail", response_model=HearingDetailResponse)
async def get_hearing_detail(
    hearing_id: int,
    db: Session = Depends(get_db)
):
    """
    Get detailed information about a specific hearing including committee and witnesses.
    """
    hearing = db.query(Hearing).options(
        joinedload(Hearing.committee),
        joinedload(Hearing.witnesses),
        joinedload(Hearing.documents)
    ).filter(Hearing.id == hearing_id).first()
    
    if not hearing:
        raise HTTPException(status_code=404, detail="Hearing not found")
    
    return HearingDetailResponse(
        hearing=hearing,
        committee=hearing.committee,
        witnesses=hearing.witnesses,
        documents=hearing.documents,
        statistics={
            "witness_count": len(hearing.witnesses),
            "document_count": len(hearing.documents)
        }
    )

@router.get("/members/{member_id}/committees", response_model=List[MemberCommitteeResponse])
async def get_member_committees(
    member_id: int,
    current_only: bool = Query(True, description="Only return current committee memberships"),
    db: Session = Depends(get_db)
):
    """
    Get all committee memberships for a specific member.
    """
    query = db.query(CommitteeMembership).options(
        joinedload(CommitteeMembership.committee)
    ).filter(CommitteeMembership.member_id == member_id)
    
    if current_only:
        query = query.filter(CommitteeMembership.is_current == True)
    
    memberships = query.all()
    
    return [
        MemberCommitteeResponse(
            committee=cm.committee,
            position=cm.position,
            is_current=cm.is_current,
            start_date=cm.start_date,
            end_date=cm.end_date
        )
        for cm in memberships
    ]

@router.get("/committees/{committee_id}/members", response_model=List[CommitteeMemberResponse])
async def get_committee_members(
    committee_id: int,
    current_only: bool = Query(True, description="Only return current committee members"),
    db: Session = Depends(get_db)
):
    """
    Get all members of a specific committee.
    """
    query = db.query(CommitteeMembership).options(
        joinedload(CommitteeMembership.member)
    ).filter(CommitteeMembership.committee_id == committee_id)
    
    if current_only:
        query = query.filter(CommitteeMembership.is_current == True)
    
    memberships = query.all()
    
    return [
        CommitteeMemberResponse(
            member=cm.member,
            position=cm.position,
            is_current=cm.is_current,
            start_date=cm.start_date,
            end_date=cm.end_date
        )
        for cm in memberships
    ]

@router.get("/committees/{committee_id}/hearings", response_model=List[CommitteeHearingResponse])
async def get_committee_hearings(
    committee_id: int,
    limit: int = Query(50, ge=1, le=100, description="Number of hearings to return"),
    db: Session = Depends(get_db)
):
    """
    Get all hearings for a specific committee.
    """
    hearings = db.query(Hearing).filter(
        Hearing.committee_id == committee_id
    ).order_by(Hearing.scheduled_date.desc()).limit(limit).all()
    
    return [
        CommitteeHearingResponse(
            hearing=hearing,
            witness_count=len(hearing.witnesses),
            document_count=len(hearing.documents)
        )
        for hearing in hearings
    ]

@router.get("/committees/{committee_id}/subcommittees", response_model=List[CommitteeResponse])
async def get_committee_subcommittees(
    committee_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all subcommittees of a specific committee.
    """
    subcommittees = db.query(Committee).filter(
        Committee.parent_committee_id == committee_id
    ).all()
    
    return subcommittees