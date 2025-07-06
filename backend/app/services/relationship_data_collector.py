"""
Service for collecting and populating relationship data between members, committees, and hearings.
"""
import logging
from typing import List, Dict, Optional, Tuple
from sqlalchemy.orm import Session
from ..models.member import Member
from ..models.committee import Committee, CommitteeMembership
from ..models.hearing import Hearing
from ..services.congress_api import CongressApiClient
from ..core.database import get_db
import asyncio

logger = logging.getLogger(__name__)

class RelationshipDataCollector:
    """Service for collecting and populating relationship data."""
    
    def __init__(self, db: Session):
        self.db = db
        self.congress_client = CongressApiClient()
        self.logger = logging.getLogger(__name__)
    
    async def populate_committee_memberships(self) -> Dict[str, int]:
        """
        Populate committee membership data for all members.
        
        Returns:
            Dictionary with statistics about memberships created.
        """
        stats = {
            "members_processed": 0,
            "memberships_created": 0,
            "memberships_updated": 0,
            "errors": 0
        }
        
        # Get all current members
        members = self.db.query(Member).filter(Member.is_current == True).all()
        
        for member in members:
            try:
                # Get committee memberships from Congress.gov API
                memberships = await self.congress_client.get_member_committees(member.bioguide_id)
                
                for membership_data in memberships:
                    # Find or create committee
                    committee = self._find_or_create_committee(membership_data)
                    
                    # Create or update membership
                    membership = self._create_or_update_membership(
                        member, committee, membership_data
                    )
                    
                    if membership:
                        stats["memberships_created"] += 1
                
                stats["members_processed"] += 1
                
                # Rate limiting
                await asyncio.sleep(0.1)
                
            except Exception as e:
                self.logger.error(f"Error processing member {member.bioguide_id}: {e}")
                stats["errors"] += 1
        
        self.db.commit()
        return stats
    
    def _find_or_create_committee(self, membership_data: Dict) -> Committee:
        """Find existing committee or create new one."""
        # Try to find by congress_gov_id first
        committee = None
        if membership_data.get("congress_gov_id"):
            committee = self.db.query(Committee).filter(
                Committee.congress_gov_id == membership_data["congress_gov_id"]
            ).first()
        
        # Try to find by name and chamber
        if not committee:
            committee = self.db.query(Committee).filter(
                Committee.name == membership_data["name"],
                Committee.chamber == membership_data["chamber"]
            ).first()
        
        # Create new committee if not found
        if not committee:
            committee = Committee(
                name=membership_data["name"],
                chamber=membership_data["chamber"],
                congress_gov_id=membership_data.get("congress_gov_id"),
                committee_code=membership_data.get("committee_code"),
                committee_type=membership_data.get("committee_type", "Standing"),
                is_subcommittee=membership_data.get("is_subcommittee", False),
                parent_committee_id=membership_data.get("parent_committee_id"),
                is_active=True
            )
            self.db.add(committee)
            self.db.flush()  # Get the ID
        
        return committee
    
    def _create_or_update_membership(
        self, member: Member, committee: Committee, membership_data: Dict
    ) -> Optional[CommitteeMembership]:
        """Create or update committee membership."""
        # Check if membership already exists
        existing = self.db.query(CommitteeMembership).filter(
            CommitteeMembership.member_id == member.id,
            CommitteeMembership.committee_id == committee.id
        ).first()
        
        if existing:
            # Update existing membership
            existing.position = membership_data.get("position", "Member")
            existing.is_current = membership_data.get("is_current", True)
            return existing
        
        # Create new membership
        membership = CommitteeMembership(
            member_id=member.id,
            committee_id=committee.id,
            position=membership_data.get("position", "Member"),
            is_current=membership_data.get("is_current", True),
            start_date=membership_data.get("start_date"),
            end_date=membership_data.get("end_date")
        )
        
        self.db.add(membership)
        return membership
    
    async def fix_committee_hierarchies(self) -> Dict[str, int]:
        """
        Fix committee parent-child relationships and subcommittee flags.
        
        Returns:
            Dictionary with statistics about hierarchies fixed.
        """
        stats = {
            "committees_processed": 0,
            "hierarchies_fixed": 0,
            "subcommittees_identified": 0,
            "errors": 0
        }
        
        committees = self.db.query(Committee).all()
        
        for committee in committees:
            try:
                # Identify subcommittees by common patterns
                is_subcommittee = self._is_subcommittee(committee.name)
                
                if is_subcommittee and not committee.is_subcommittee:
                    # Find parent committee
                    parent = self._find_parent_committee(committee)
                    
                    if parent:
                        committee.is_subcommittee = True
                        committee.parent_committee_id = parent.id
                        stats["hierarchies_fixed"] += 1
                        stats["subcommittees_identified"] += 1
                
                stats["committees_processed"] += 1
                
            except Exception as e:
                self.logger.error(f"Error processing committee {committee.name}: {e}")
                stats["errors"] += 1
        
        self.db.commit()
        return stats
    
    def _is_subcommittee(self, committee_name: str) -> bool:
        """Determine if a committee is a subcommittee based on name patterns."""
        subcommittee_indicators = [
            "subcommittee",
            "sub-committee",
            "task force",
            "working group",
            "panel"
        ]
        
        name_lower = committee_name.lower()
        return any(indicator in name_lower for indicator in subcommittee_indicators)
    
    def _find_parent_committee(self, subcommittee: Committee) -> Optional[Committee]:
        """Find the parent committee for a subcommittee."""
        # Look for committees in the same chamber with similar names
        parent_candidates = self.db.query(Committee).filter(
            Committee.chamber == subcommittee.chamber,
            Committee.is_subcommittee == False,
            Committee.id != subcommittee.id
        ).all()
        
        # Try to match by name similarity
        subcommittee_name = subcommittee.name.lower()
        
        for candidate in parent_candidates:
            candidate_name = candidate.name.lower()
            
            # Check if subcommittee name contains parent name
            if candidate_name in subcommittee_name:
                return candidate
            
            # Check common patterns like "Committee on X - Subcommittee on Y"
            if self._name_similarity_check(subcommittee_name, candidate_name):
                return candidate
        
        return None
    
    def _name_similarity_check(self, sub_name: str, parent_name: str) -> bool:
        """Check if two committee names are similar enough to be parent-child."""
        # Remove common words
        common_words = ["committee", "on", "the", "and", "of", "for", "in"]
        
        sub_words = set(sub_name.split()) - set(common_words)
        parent_words = set(parent_name.split()) - set(common_words)
        
        # Check if they share significant words
        shared_words = sub_words.intersection(parent_words)
        
        # If they share more than 50% of words, likely parent-child
        return len(shared_words) > 0 and len(shared_words) >= len(parent_words) * 0.5
    
    async def associate_hearings_with_committees(self) -> Dict[str, int]:
        """
        Associate hearings with their respective committees.
        
        Returns:
            Dictionary with statistics about associations created.
        """
        stats = {
            "hearings_processed": 0,
            "associations_created": 0,
            "errors": 0
        }
        
        # Get hearings without committee associations
        hearings = self.db.query(Hearing).filter(
            Hearing.committee_id.is_(None)
        ).all()
        
        for hearing in hearings:
            try:
                # Try to find committee based on hearing title/description
                committee = self._match_hearing_to_committee(hearing)
                
                if committee:
                    hearing.committee_id = committee.id
                    stats["associations_created"] += 1
                
                stats["hearings_processed"] += 1
                
            except Exception as e:
                self.logger.error(f"Error processing hearing {hearing.id}: {e}")
                stats["errors"] += 1
        
        self.db.commit()
        return stats
    
    def _match_hearing_to_committee(self, hearing: Hearing) -> Optional[Committee]:
        """Match a hearing to its committee based on title and description."""
        if not hearing.title:
            return None
        
        # Get all committees
        committees = self.db.query(Committee).all()
        
        hearing_text = (hearing.title + " " + (hearing.description or "")).lower()
        
        # Try to find committee name in hearing text
        for committee in committees:
            committee_name = committee.name.lower()
            
            # Check if committee name appears in hearing text
            if committee_name in hearing_text:
                return committee
            
            # Check individual words from committee name
            committee_words = set(committee_name.split()) - {"committee", "on", "the", "and", "of", "for", "in"}
            
            if committee_words and all(word in hearing_text for word in committee_words):
                return committee
        
        return None

# Utility functions for external use
async def populate_all_relationship_data(db: Session) -> Dict[str, Any]:
    """
    Populate all relationship data (memberships, hierarchies, hearing associations).
    
    Returns:
        Comprehensive statistics about all data populated.
    """
    collector = RelationshipDataCollector(db)
    
    # Step 1: Populate committee memberships
    membership_stats = await collector.populate_committee_memberships()
    
    # Step 2: Fix committee hierarchies
    hierarchy_stats = await collector.fix_committee_hierarchies()
    
    # Step 3: Associate hearings with committees
    hearing_stats = await collector.associate_hearings_with_committees()
    
    return {
        "membership_data": membership_stats,
        "hierarchy_data": hierarchy_stats,
        "hearing_associations": hearing_stats,
        "total_operations": (
            membership_stats["memberships_created"] + 
            hierarchy_stats["hierarchies_fixed"] + 
            hearing_stats["associations_created"]
        )
    }