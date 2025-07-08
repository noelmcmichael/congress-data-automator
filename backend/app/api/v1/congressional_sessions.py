"""
Congressional sessions API endpoints.
"""
from datetime import date, datetime, timedelta
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc

from ...core.database import get_db
from ...models.congressional_session import CongressionalSession
from ...schemas.congressional_session import (
    CongressionalSession as CongressionalSessionSchema,
    CongressionalSessionCreate,
    CongressionalSessionUpdate,
    CongressionalSessionSummary,
    CurrentCongressInfo
)

router = APIRouter()


@router.get("/current", response_model=CurrentCongressInfo)
async def get_current_congress_info(db: Session = Depends(get_db)):
    """
    Get information about the current Congressional session.
    """
    current_session = CongressionalSession.get_current_session(db)
    if not current_session:
        raise HTTPException(
            status_code=404,
            detail="No current congressional session found"
        )
    
    # Calculate days remaining
    today = date.today()
    days_remaining = (current_session.end_date - today).days
    
    # Get previous and next sessions
    previous_session = db.query(CongressionalSession).filter(
        CongressionalSession.congress_number == current_session.congress_number - 1
    ).first()
    
    next_session = db.query(CongressionalSession).filter(
        CongressionalSession.congress_number == current_session.congress_number + 1
    ).first()
    
    return CurrentCongressInfo(
        current_session=current_session,
        days_remaining=max(0, days_remaining),
        next_election_year=current_session.election_year or (current_session.start_date.year + 2),
        house_majority=current_session.party_control_house or "Unknown",
        senate_majority=current_session.party_control_senate or "Unknown",
        unified_government=current_session.unified_control,
        previous_session=CongressionalSessionSummary.from_orm(previous_session) if previous_session else None,
        next_session=CongressionalSessionSummary.from_orm(next_session) if next_session else None
    )


@router.get("/", response_model=List[CongressionalSessionSummary])
async def list_congressional_sessions(
    limit: int = Query(default=10, le=100),
    offset: int = Query(default=0, ge=0),
    include_historical: bool = Query(default=True),
    db: Session = Depends(get_db)
):
    """
    List congressional sessions.
    """
    query = db.query(CongressionalSession)
    
    if not include_historical:
        # Only include recent sessions (last 5 congresses)
        current = CongressionalSession.get_current_session(db)
        if current:
            min_congress = max(1, current.congress_number - 4)
            query = query.filter(CongressionalSession.congress_number >= min_congress)
    
    sessions = query.order_by(desc(CongressionalSession.congress_number)).offset(offset).limit(limit).all()
    
    return [CongressionalSessionSummary.from_orm(session) for session in sessions]


@router.get("/{congress_number}", response_model=CongressionalSessionSchema)
async def get_congressional_session(
    congress_number: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific congressional session by number.
    """
    session = CongressionalSession.get_by_number(db, congress_number)
    if not session:
        raise HTTPException(
            status_code=404,
            detail=f"Congressional session {congress_number} not found"
        )
    
    return session


@router.post("/", response_model=CongressionalSessionSchema)
async def create_congressional_session(
    session_data: CongressionalSessionCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new congressional session.
    """
    # Check if session already exists
    existing = CongressionalSession.get_by_number(db, session_data.congress_number)
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Congressional session {session_data.congress_number} already exists"
        )
    
    # If this is marked as current, unmark other current sessions
    if session_data.is_current:
        db.query(CongressionalSession).filter(
            CongressionalSession.is_current == True
        ).update({"is_current": False})
    
    # Create session name if not provided
    if not session_data.session_name:
        ordinal = CongressionalSession.get_ordinal_suffix(session_data.congress_number)
        session_data.session_name = f"{session_data.congress_number}{ordinal} Congress"
    
    db_session = CongressionalSession(**session_data.dict())
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    
    return db_session


@router.put("/{congress_number}", response_model=CongressionalSessionSchema)
async def update_congressional_session(
    congress_number: int,
    session_update: CongressionalSessionUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a congressional session.
    """
    session = CongressionalSession.get_by_number(db, congress_number)
    if not session:
        raise HTTPException(
            status_code=404,
            detail=f"Congressional session {congress_number} not found"
        )
    
    # If setting as current, unmark other current sessions
    if session_update.is_current:
        db.query(CongressionalSession).filter(
            CongressionalSession.is_current == True,
            CongressionalSession.congress_number != congress_number
        ).update({"is_current": False})
    
    # Update fields
    update_data = session_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(session, field, value)
    
    db.commit()
    db.refresh(session)
    
    return session


@router.get("/history/transitions")
async def get_congressional_transitions(
    limit: int = Query(default=10, le=50),
    db: Session = Depends(get_db)
):
    """
    Get information about Congressional transitions and party control changes.
    """
    sessions = db.query(CongressionalSession).order_by(
        desc(CongressionalSession.congress_number)
    ).limit(limit).all()
    
    transitions = []
    for i, session in enumerate(sessions):
        if i < len(sessions) - 1:
            prev_session = sessions[i + 1]
            
            # Check for party control changes
            house_change = (session.party_control_house != prev_session.party_control_house 
                          if session.party_control_house and prev_session.party_control_house else False)
            senate_change = (session.party_control_senate != prev_session.party_control_senate
                           if session.party_control_senate and prev_session.party_control_senate else False)
            
            if house_change or senate_change:
                transitions.append({
                    "from_congress": prev_session.congress_number,
                    "to_congress": session.congress_number,
                    "transition_date": session.start_date,
                    "house_control_change": {
                        "changed": house_change,
                        "from": prev_session.party_control_house,
                        "to": session.party_control_house
                    } if house_change else None,
                    "senate_control_change": {
                        "changed": senate_change,
                        "from": prev_session.party_control_senate,
                        "to": session.party_control_senate
                    } if senate_change else None
                })
    
    return {
        "transitions": transitions,
        "total_sessions": len(sessions)
    }


@router.get("/validate/current-data")
async def validate_current_congressional_data(db: Session = Depends(get_db)):
    """
    Validate that current data matches the current Congressional session.
    """
    current_session = CongressionalSession.get_current_session(db)
    if not current_session:
        return {
            "status": "error",
            "message": "No current congressional session defined",
            "recommendations": ["Create or mark a congressional session as current"]
        }
    
    # Import here to avoid circular imports
    from ...models.member import Member
    from ...models.committee import Committee
    
    # Check member data currency
    current_members = db.query(Member).filter(
        Member.is_current == True,
        Member.congress_session == current_session.congress_number
    ).count()
    
    total_current_members = db.query(Member).filter(Member.is_current == True).count()
    
    # Check committee data currency
    current_committees = db.query(Committee).filter(
        Committee.is_active == True,
        Committee.congress_session == current_session.congress_number
    ).count()
    
    total_current_committees = db.query(Committee).filter(Committee.is_active == True).count()
    
    issues = []
    recommendations = []
    
    if current_members == 0:
        issues.append("No members found for current congressional session")
        recommendations.append(f"Update member data to include {current_session.congress_number}th Congress")
    elif current_members < total_current_members:
        issues.append(f"Only {current_members}/{total_current_members} current members are from {current_session.congress_number}th Congress")
        recommendations.append("Migrate remaining current members to current congressional session")
    
    if current_committees == 0:
        issues.append("No committees found for current congressional session")
        recommendations.append(f"Update committee data to include {current_session.congress_number}th Congress")
    elif current_committees < total_current_committees:
        issues.append(f"Only {current_committees}/{total_current_committees} current committees are from {current_session.congress_number}th Congress")
        recommendations.append("Migrate remaining current committees to current congressional session")
    
    status = "healthy" if not issues else "warning"
    
    return {
        "status": status,
        "current_session": {
            "congress_number": current_session.congress_number,
            "display_name": current_session.display_name,
            "years": current_session.years_display
        },
        "data_summary": {
            "members_current_session": current_members,
            "members_total_current": total_current_members,
            "committees_current_session": current_committees,
            "committees_total_current": total_current_committees
        },
        "issues": issues,
        "recommendations": recommendations
    }