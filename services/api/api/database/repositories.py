"""Repository layer for data access."""

from typing import List, Optional, Tuple
from sqlalchemy import and_, func, or_
from sqlalchemy.orm import Session, joinedload

from ..models.congress import (
    Chamber,
    Party,
    MemberFilterParams,
    CommitteeFilterParams,
    HearingFilterParams,
    PaginationParams,
)
from .models import Member, Committee, Hearing, CommitteeMembership


class BaseRepository:
    """Base repository class."""
    
    def __init__(self, session: Session):
        self.session = session
    
    def _apply_pagination(self, query, pagination: PaginationParams):
        """Apply pagination to query."""
        return query.offset(pagination.offset).limit(pagination.limit)
    
    def _apply_search(self, query, search_term: Optional[str], search_fields: List[str]):
        """Apply search to query."""
        if not search_term:
            return query
        
        search_conditions = []
        for field in search_fields:
            if hasattr(field, 'ilike'):
                search_conditions.append(field.ilike(f"%{search_term}%"))
            else:
                search_conditions.append(field.contains(search_term))
        
        return query.filter(or_(*search_conditions))
    
    def _apply_sort(self, query, sort_by: Optional[str], sort_order: Optional[str], model_class):
        """Apply sorting to query."""
        if not sort_by:
            return query
        
        if hasattr(model_class, sort_by):
            field = getattr(model_class, sort_by)
            if sort_order == "desc":
                return query.order_by(field.desc())
            else:
                return query.order_by(field)
        
        return query


class MemberRepository(BaseRepository):
    """Repository for Member operations."""
    
    def get_by_id(self, member_id: int) -> Optional[Member]:
        """Get member by ID."""
        return self.session.query(Member).filter(Member.id == member_id).first()
    
    def get_by_bioguide_id(self, bioguide_id: str) -> Optional[Member]:
        """Get member by bioguide ID."""
        return self.session.query(Member).filter(Member.bioguide_id == bioguide_id).first()
    
    def get_all(
        self,
        filters: MemberFilterParams,
        pagination: PaginationParams,
    ) -> Tuple[List[Member], int]:
        """Get all members with filtering and pagination."""
        query = self.session.query(Member)
        
        # Apply filters
        if filters.chamber:
            query = query.filter(Member.chamber == filters.chamber.value)
        
        if filters.party:
            query = query.filter(Member.party == filters.party.value)
        
        if filters.state:
            query = query.filter(Member.state == filters.state)
        
        if filters.is_current is not None:
            query = query.filter(Member.is_current == filters.is_current)
        
        # Apply search
        if filters.search:
            query = self._apply_search(
                query,
                filters.search,
                [Member.name, Member.first_name, Member.last_name]
            )
        
        # Get total count before pagination
        total = query.count()
        
        # Apply sorting
        query = self._apply_sort(query, filters.sort_by, filters.sort_order, Member)
        
        # Apply pagination
        query = self._apply_pagination(query, pagination)
        
        return query.all(), total
    
    def get_member_committees(self, member_id: int) -> List[Committee]:
        """Get committees for a member."""
        return (
            self.session.query(Committee)
            .join(CommitteeMembership)
            .filter(
                and_(
                    CommitteeMembership.member_id == member_id,
                    CommitteeMembership.is_current == True,
                )
            )
            .all()
        )
    
    def get_member_with_committees(self, member_id: int) -> Optional[Member]:
        """Get member with their committee assignments."""
        return (
            self.session.query(Member)
            .options(
                joinedload(Member.committee_memberships).joinedload(
                    CommitteeMembership.committee
                )
            )
            .filter(Member.id == member_id)
            .first()
        )
    
    def get_statistics(self) -> dict:
        """Get member statistics."""
        total_members = self.session.query(Member).count()
        current_members = self.session.query(Member).filter(Member.is_current == True).count()
        
        # Party breakdown
        party_stats = (
            self.session.query(Member.party, func.count(Member.id))
            .filter(Member.is_current == True)
            .group_by(Member.party)
            .all()
        )
        
        # Chamber breakdown
        chamber_stats = (
            self.session.query(Member.chamber, func.count(Member.id))
            .filter(Member.is_current == True)
            .group_by(Member.chamber)
            .all()
        )
        
        # State breakdown
        state_stats = (
            self.session.query(Member.state, func.count(Member.id))
            .filter(Member.is_current == True)
            .group_by(Member.state)
            .order_by(func.count(Member.id).desc())
            .all()
        )
        
        return {
            "total_members": total_members,
            "current_members": current_members,
            "party_breakdown": {party: count for party, count in party_stats},
            "chamber_breakdown": {chamber: count for chamber, count in chamber_stats},
            "state_breakdown": {state: count for state, count in state_stats},
        }


class CommitteeRepository(BaseRepository):
    """Repository for Committee operations."""
    
    def get_by_id(self, committee_id: int) -> Optional[Committee]:
        """Get committee by ID."""
        return self.session.query(Committee).filter(Committee.id == committee_id).first()
    
    def get_by_code(self, code: str) -> Optional[Committee]:
        """Get committee by code."""
        return self.session.query(Committee).filter(Committee.code == code).first()
    
    def get_all(
        self,
        filters: CommitteeFilterParams,
        pagination: PaginationParams,
    ) -> Tuple[List[Committee], int]:
        """Get all committees with filtering and pagination."""
        query = self.session.query(Committee)
        
        # Apply filters
        if filters.chamber:
            query = query.filter(Committee.chamber == filters.chamber.value)
        
        if filters.committee_type:
            query = query.filter(Committee.committee_type == filters.committee_type.value)
        
        if filters.is_current is not None:
            query = query.filter(Committee.is_current == filters.is_current)
        
        # Apply search
        if filters.search:
            query = self._apply_search(
                query,
                filters.search,
                [Committee.name, Committee.description]
            )
        
        # Get total count before pagination
        total = query.count()
        
        # Apply sorting
        query = self._apply_sort(query, filters.sort_by, filters.sort_order, Committee)
        
        # Apply pagination
        query = self._apply_pagination(query, pagination)
        
        return query.all(), total
    
    def get_committee_members(self, committee_id: int) -> List[Member]:
        """Get members of a committee."""
        return (
            self.session.query(Member)
            .join(CommitteeMembership)
            .filter(
                and_(
                    CommitteeMembership.committee_id == committee_id,
                    CommitteeMembership.is_current == True,
                )
            )
            .all()
        )
    
    def get_committee_with_members(self, committee_id: int) -> Optional[Committee]:
        """Get committee with its members."""
        return (
            self.session.query(Committee)
            .options(
                joinedload(Committee.committee_memberships).joinedload(
                    CommitteeMembership.member
                )
            )
            .filter(Committee.id == committee_id)
            .first()
        )
    
    def get_subcommittees(self, committee_id: int) -> List[Committee]:
        """Get subcommittees of a committee."""
        return (
            self.session.query(Committee)
            .filter(Committee.parent_committee_id == committee_id)
            .all()
        )
    
    def get_statistics(self) -> dict:
        """Get committee statistics."""
        total_committees = self.session.query(Committee).count()
        current_committees = self.session.query(Committee).filter(Committee.is_current == True).count()
        
        # Chamber breakdown
        chamber_stats = (
            self.session.query(Committee.chamber, func.count(Committee.id))
            .filter(Committee.is_current == True)
            .group_by(Committee.chamber)
            .all()
        )
        
        # Type breakdown
        type_stats = (
            self.session.query(Committee.committee_type, func.count(Committee.id))
            .filter(Committee.is_current == True)
            .group_by(Committee.committee_type)
            .all()
        )
        
        return {
            "total_committees": total_committees,
            "current_committees": current_committees,
            "chamber_breakdown": {chamber: count for chamber, count in chamber_stats},
            "type_breakdown": {type_: count for type_, count in type_stats},
        }


class HearingRepository(BaseRepository):
    """Repository for Hearing operations."""
    
    def get_by_id(self, hearing_id: int) -> Optional[Hearing]:
        """Get hearing by ID."""
        return self.session.query(Hearing).filter(Hearing.id == hearing_id).first()
    
    def get_all(
        self,
        filters: HearingFilterParams,
        pagination: PaginationParams,
    ) -> Tuple[List[Hearing], int]:
        """Get all hearings with filtering and pagination."""
        query = self.session.query(Hearing)
        
        # Apply filters
        if filters.committee_id:
            query = query.filter(Hearing.committee_id == filters.committee_id)
        
        if filters.status:
            query = query.filter(Hearing.status == filters.status.value)
        
        if filters.date_from:
            query = query.filter(Hearing.date >= filters.date_from)
        
        if filters.date_to:
            query = query.filter(Hearing.date <= filters.date_to)
        
        # Apply search
        if filters.search:
            query = self._apply_search(
                query,
                filters.search,
                [Hearing.title, Hearing.description]
            )
        
        # Get total count before pagination
        total = query.count()
        
        # Apply sorting
        query = self._apply_sort(query, filters.sort_by, filters.sort_order, Hearing)
        
        # Apply pagination
        query = self._apply_pagination(query, pagination)
        
        return query.all(), total
    
    def get_hearing_with_committee(self, hearing_id: int) -> Optional[Hearing]:
        """Get hearing with committee information."""
        return (
            self.session.query(Hearing)
            .options(joinedload(Hearing.committee))
            .filter(Hearing.id == hearing_id)
            .first()
        )
    
    def get_statistics(self) -> dict:
        """Get hearing statistics."""
        total_hearings = self.session.query(Hearing).count()
        
        # Status breakdown
        status_stats = (
            self.session.query(Hearing.status, func.count(Hearing.id))
            .group_by(Hearing.status)
            .all()
        )
        
        return {
            "total_hearings": total_hearings,
            "status_breakdown": {status: count for status, count in status_stats},
        }