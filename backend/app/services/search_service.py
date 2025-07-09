"""
Enhanced search service for Congressional Data Automation Service.
Provides full-text search, autocomplete, and advanced filtering.
"""
from typing import List, Dict, Any, Optional, Tuple, Union
import re
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func, text
import structlog

from ..models.member import Member
from ..models.committee import Committee
from ..models.hearing import Hearing
from ..core.security import InputValidator

logger = structlog.get_logger()


class SearchService:
    """Enhanced search functionality for congressional data."""
    
    def __init__(self):
        # Common search terms for autocomplete
        self.search_suggestions = {
            'states': [
                'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado',
                'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho',
                'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana',
                'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota',
                'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada',
                'New Hampshire', 'New Jersey', 'New Mexico', 'New York',
                'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon',
                'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota',
                'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington',
                'West Virginia', 'Wisconsin', 'Wyoming'
            ],
            'parties': ['Republican', 'Democrat', 'Independent', 'Libertarian', 'Green'],
            'chambers': ['House', 'Senate'],
            'committee_types': ['Standing', 'Select', 'Special', 'Joint']
        }
    
    async def search_members(
        self,
        db: Session,
        query: str,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 50,
        offset: int = 0
    ) -> Tuple[List[Member], int]:
        """
        Search members with full-text search capabilities.
        
        Returns:
            tuple: (members_list, total_count)
        """
        # Validate search query
        is_valid, error, clean_query = InputValidator.validate_search_query(query)
        if not is_valid:
            raise ValueError(error)
        
        # Build base query
        base_query = db.query(Member)
        
        # Apply text search
        if clean_query:
            search_conditions = []
            
            # Search in names
            name_search = or_(
                Member.first_name.ilike(f'%{clean_query}%'),
                Member.last_name.ilike(f'%{clean_query}%'),
                func.concat(Member.first_name, ' ', Member.last_name).ilike(f'%{clean_query}%')
            )
            search_conditions.append(name_search)
            
            # Search in other fields
            search_conditions.extend([
                Member.state.ilike(f'%{clean_query}%'),
                Member.party.ilike(f'%{clean_query}%'),
                Member.bioguide_id.ilike(f'%{clean_query}%')
            ])
            
            base_query = base_query.filter(or_(*search_conditions))
        
        # Apply additional filters
        if filters:
            if 'state' in filters and filters['state']:
                base_query = base_query.filter(Member.state == filters['state'])
            if 'party' in filters and filters['party']:
                base_query = base_query.filter(Member.party == filters['party'])
            if 'chamber' in filters and filters['chamber']:
                base_query = base_query.filter(Member.chamber == filters['chamber'])
            if 'voting_status' in filters and filters['voting_status']:
                base_query = base_query.filter(Member.voting_status == filters['voting_status'])
        
        # Get total count
        total_count = base_query.count()
        
        # Apply pagination and ordering
        members = base_query.order_by(Member.last_name, Member.first_name)\
                           .offset(offset)\
                           .limit(limit)\
                           .all()
        
        return members, total_count
    
    async def search_committees(
        self,
        db: Session,
        query: str,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 50,
        offset: int = 0
    ) -> Tuple[List[Committee], int]:
        """
        Search committees with full-text search capabilities.
        
        Returns:
            tuple: (committees_list, total_count)
        """
        # Validate search query
        is_valid, error, clean_query = InputValidator.validate_search_query(query)
        if not is_valid:
            raise ValueError(error)
        
        # Build base query
        base_query = db.query(Committee)
        
        # Apply text search
        if clean_query:
            search_conditions = [
                Committee.name.ilike(f'%{clean_query}%'),
                Committee.committee_code.ilike(f'%{clean_query}%')
            ]
            base_query = base_query.filter(or_(*search_conditions))
        
        # Apply additional filters
        if filters:
            if 'chamber' in filters and filters['chamber']:
                base_query = base_query.filter(Committee.chamber == filters['chamber'])
            if 'committee_type' in filters and filters['committee_type']:
                base_query = base_query.filter(Committee.committee_type == filters['committee_type'])
            if 'parent_committee_id' in filters:
                if filters['parent_committee_id'] == 'null':
                    base_query = base_query.filter(Committee.parent_committee_id.is_(None))
                else:
                    base_query = base_query.filter(Committee.parent_committee_id == filters['parent_committee_id'])
        
        # Get total count
        total_count = base_query.count()
        
        # Apply pagination and ordering
        committees = base_query.order_by(Committee.name)\
                             .offset(offset)\
                             .limit(limit)\
                             .all()
        
        return committees, total_count
    
    async def search_hearings(
        self,
        db: Session,
        query: str,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 50,
        offset: int = 0
    ) -> Tuple[List[Hearing], int]:
        """
        Search hearings with full-text search capabilities.
        
        Returns:
            tuple: (hearings_list, total_count)
        """
        # Validate search query
        is_valid, error, clean_query = InputValidator.validate_search_query(query)
        if not is_valid:
            raise ValueError(error)
        
        # Build base query
        base_query = db.query(Hearing)
        
        # Apply text search
        if clean_query:
            search_conditions = [
                Hearing.title.ilike(f'%{clean_query}%')
            ]
            base_query = base_query.filter(or_(*search_conditions))
        
        # Apply additional filters
        if filters:
            if 'committee_id' in filters and filters['committee_id']:
                base_query = base_query.filter(Hearing.committee_id == filters['committee_id'])
            if 'date_from' in filters and filters['date_from']:
                base_query = base_query.filter(Hearing.date >= filters['date_from'])
            if 'date_to' in filters and filters['date_to']:
                base_query = base_query.filter(Hearing.date <= filters['date_to'])
        
        # Get total count
        total_count = base_query.count()
        
        # Apply pagination and ordering
        hearings = base_query.order_by(Hearing.date.desc())\
                           .offset(offset)\
                           .limit(limit)\
                           .all()
        
        return hearings, total_count
    
    async def global_search(
        self,
        db: Session,
        query: str,
        search_types: Optional[List[str]] = None,
        limit_per_type: int = 10
    ) -> Dict[str, Any]:
        """
        Perform global search across all data types.
        
        Args:
            query: Search query string
            search_types: List of types to search ('members', 'committees', 'hearings')
            limit_per_type: Maximum results per type
        
        Returns:
            Dictionary with search results by type
        """
        # Validate search query
        is_valid, error, clean_query = InputValidator.validate_search_query(query)
        if not is_valid:
            raise ValueError(error)
        
        if not search_types:
            search_types = ['members', 'committees', 'hearings']
        
        results = {
            'query': clean_query,
            'results': {},
            'total_results': 0
        }
        
        # Search members
        if 'members' in search_types:
            try:
                members, member_count = await self.search_members(
                    db, clean_query, limit=limit_per_type
                )
                results['results']['members'] = {
                    'items': [self._serialize_member(m) for m in members],
                    'total': member_count,
                    'displayed': len(members)
                }
                results['total_results'] += member_count
            except Exception as e:
                logger.warning(f"Member search failed: {e}")
                results['results']['members'] = {'items': [], 'total': 0, 'displayed': 0}
        
        # Search committees
        if 'committees' in search_types:
            try:
                committees, committee_count = await self.search_committees(
                    db, clean_query, limit=limit_per_type
                )
                results['results']['committees'] = {
                    'items': [self._serialize_committee(c) for c in committees],
                    'total': committee_count,
                    'displayed': len(committees)
                }
                results['total_results'] += committee_count
            except Exception as e:
                logger.warning(f"Committee search failed: {e}")
                results['results']['committees'] = {'items': [], 'total': 0, 'displayed': 0}
        
        # Search hearings
        if 'hearings' in search_types:
            try:
                hearings, hearing_count = await self.search_hearings(
                    db, clean_query, limit=limit_per_type
                )
                results['results']['hearings'] = {
                    'items': [self._serialize_hearing(h) for h in hearings],
                    'total': hearing_count,
                    'displayed': len(hearings)
                }
                results['total_results'] += hearing_count
            except Exception as e:
                logger.warning(f"Hearing search failed: {e}")
                results['results']['hearings'] = {'items': [], 'total': 0, 'displayed': 0}
        
        return results
    
    async def get_search_suggestions(
        self,
        db: Session,
        query: str,
        suggestion_type: Optional[str] = None,
        limit: int = 10
    ) -> List[str]:
        """
        Get search suggestions/autocomplete results.
        
        Args:
            query: Partial search query
            suggestion_type: Type of suggestions ('members', 'committees', 'states', 'parties')
            limit: Maximum number of suggestions
        
        Returns:
            List of suggestion strings
        """
        suggestions = []
        
        if not query or len(query) < 2:
            return suggestions
        
        # Validate and clean query
        clean_query = re.sub(r'[^\w\s-]', '', query).strip().lower()
        
        if suggestion_type == 'states' or not suggestion_type:
            # State suggestions
            state_matches = [
                state for state in self.search_suggestions['states']
                if clean_query in state.lower()
            ]
            suggestions.extend(state_matches[:limit//4 if not suggestion_type else limit])
        
        if suggestion_type == 'parties' or not suggestion_type:
            # Party suggestions
            party_matches = [
                party for party in self.search_suggestions['parties']
                if clean_query in party.lower()
            ]
            suggestions.extend(party_matches[:limit//4 if not suggestion_type else limit])
        
        if suggestion_type == 'members' or not suggestion_type:
            # Member name suggestions from database
            try:
                member_names = db.query(
                    func.concat(Member.first_name, ' ', Member.last_name).label('full_name')
                ).filter(
                    or_(
                        Member.first_name.ilike(f'%{clean_query}%'),
                        Member.last_name.ilike(f'%{clean_query}%')
                    )
                ).limit(limit//2 if not suggestion_type else limit).all()
                
                suggestions.extend([name.full_name for name in member_names])
            except Exception as e:
                logger.warning(f"Database member suggestions failed: {e}")
        
        if suggestion_type == 'committees' or not suggestion_type:
            # Committee name suggestions from database
            try:
                committee_names = db.query(Committee.name).filter(
                    Committee.name.ilike(f'%{clean_query}%')
                ).limit(limit//4 if not suggestion_type else limit).all()
                
                suggestions.extend([name.name for name in committee_names])
            except Exception as e:
                logger.warning(f"Database committee suggestions failed: {e}")
        
        # Remove duplicates and limit results
        unique_suggestions = list(dict.fromkeys(suggestions))  # Preserves order
        return unique_suggestions[:limit]
    
    def _serialize_member(self, member: Member) -> Dict[str, Any]:
        """Serialize member for search results."""
        return {
            'id': member.id,
            'bioguide_id': member.bioguide_id,
            'name': f"{member.first_name} {member.last_name}",
            'party': member.party,
            'state': member.state,
            'chamber': member.chamber,
            'url': member.url
        }
    
    def _serialize_committee(self, committee: Committee) -> Dict[str, Any]:
        """Serialize committee for search results."""
        return {
            'id': committee.id,
            'committee_code': committee.committee_code,
            'name': committee.name,
            'chamber': committee.chamber,
            'committee_type': committee.committee_type,
            'url': committee.url
        }
    
    def _serialize_hearing(self, hearing: Hearing) -> Dict[str, Any]:
        """Serialize hearing for search results."""
        return {
            'id': hearing.id,
            'title': hearing.title,
            'date': hearing.date.strftime('%Y-%m-%d') if hearing.date else None,
            'committee_id': hearing.committee_id,
            'url': hearing.url
        }
    
    async def get_advanced_filters(self, db: Session) -> Dict[str, Any]:
        """Get available filter options for advanced search."""
        try:
            # Get unique values for filter options
            states = db.query(Member.state).distinct().all()
            parties = db.query(Member.party).distinct().all()
            chambers = db.query(Committee.chamber).distinct().all()
            committee_types = db.query(Committee.committee_type).distinct().all()
            
            return {
                'states': [s.state for s in states if s.state],
                'parties': [p.party for p in parties if p.party],
                'chambers': [c.chamber for c in chambers if c.chamber],
                'committee_types': [ct.committee_type for ct in committee_types if ct.committee_type]
            }
        except Exception as e:
            logger.warning(f"Failed to get filter options: {e}")
            return {
                'states': self.search_suggestions['states'],
                'parties': self.search_suggestions['parties'],
                'chambers': self.search_suggestions['chambers'],
                'committee_types': self.search_suggestions['committee_types']
            }


# Global search service instance
search_service = SearchService()