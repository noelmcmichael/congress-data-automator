"""
Data processing service for collecting and storing congressional data.
"""
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime
from sqlalchemy.orm import Session
import structlog
from ..core.database import SessionLocal
from ..models import Member, Committee, CommitteeMembership, Hearing, Witness, HearingDocument
from ..core.utils import get_state_abbreviation, get_chamber_name
from .congress_api import CongressApiClient
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from scrapers import HouseScraper, SenateScraper

logger = structlog.get_logger()


class DataProcessor:
    """
    Service for processing congressional data from multiple sources.
    """
    
    def __init__(self):
        self.congress_api = CongressApiClient()
        self.house_scraper = HouseScraper()
        self.senate_scraper = SenateScraper()
    
    async def update_members(self, force_refresh: bool = False) -> Dict[str, Any]:
        """
        Update congressional members from Congress.gov API.
        
        Args:
            force_refresh: Force refresh even if recently updated
            
        Returns:
            Update summary
        """
        logger.info("Starting members update")
        
        db = SessionLocal()
        try:
            # Get current members from API
            house_members = await self.congress_api.get_members(chamber="house")
            senate_members = await self.congress_api.get_members(chamber="senate")
            
            # Combine and deduplicate by bioguide_id
            all_members_raw = house_members + senate_members
            members_dict = {}
            for member in all_members_raw:
                bioguide_id = member.get("bioguideId")
                if bioguide_id and bioguide_id not in members_dict:
                    members_dict[bioguide_id] = member
            
            all_members = list(members_dict.values())
            logger.info("Members data collected", total_raw=len(all_members_raw), deduplicated=len(all_members))
            
            updated_count = 0
            created_count = 0
            
            for member_data in all_members:
                # Check if member exists
                bioguide_id = member_data.get("bioguideId")
                if not bioguide_id:
                    continue
                
                existing_member = db.query(Member).filter(
                    Member.bioguide_id == bioguide_id
                ).first()
                
                if existing_member:
                    # Update existing member
                    self._update_member_from_api(existing_member, member_data)
                    updated_count += 1
                else:
                    # Create new member
                    new_member = self._create_member_from_api(member_data)
                    db.add(new_member)
                    created_count += 1
            
            db.commit()
            
            summary = {
                "total_processed": len(all_members),
                "created": created_count,
                "updated": updated_count,
                "timestamp": datetime.now().isoformat(),
            }
            
            logger.info("Members update completed", **summary)
            return summary
            
        except Exception as e:
            db.rollback()
            logger.error("Error updating members", error=str(e))
            raise
        finally:
            db.close()
    
    def _parse_member_name(self, full_name: str) -> Dict[str, str]:
        """
        Parse full name into components.
        
        Args:
            full_name: Full name like "Ramirez, Delia C."
            
        Returns:
            Dictionary with name components
        """
        result = {
            "first_name": "",
            "last_name": "",
            "middle_name": None,
            "suffix": None,
            "nickname": None
        }
        
        if not full_name:
            return result
        
        # Handle format like "Ramirez, Delia C."
        if ", " in full_name:
            parts = full_name.split(", ")
            result["last_name"] = parts[0].strip()
            if len(parts) > 1:
                first_parts = parts[1].strip().split()
                if first_parts:
                    result["first_name"] = first_parts[0]
                    if len(first_parts) > 1:
                        result["middle_name"] = " ".join(first_parts[1:])
        else:
            # Handle other formats
            parts = full_name.split()
            if parts:
                result["first_name"] = parts[0]
                if len(parts) > 1:
                    result["last_name"] = parts[-1]
                    if len(parts) > 2:
                        result["middle_name"] = " ".join(parts[1:-1])
        
        return result
    
    def _create_member_from_api(self, member_data: Dict[str, Any]) -> Member:
        """
        Create Member object from API data.
        
        Args:
            member_data: Member data from API
            
        Returns:
            Member object
        """
        # Parse name from full name field
        full_name = member_data.get("name", "")
        name_parts = self._parse_member_name(full_name)
        
        # Get chamber from terms
        chamber = ""
        terms = member_data.get("terms", {})
        if isinstance(terms, dict) and "item" in terms:
            term_items = terms["item"]
            if term_items and len(term_items) > 0:
                chamber = term_items[0].get("chamber", "")
        
        # Get image URL from depiction
        image_url = None
        depiction = member_data.get("depiction", {})
        if isinstance(depiction, dict):
            image_url = depiction.get("imageUrl")
        
        return Member(
            bioguide_id=member_data.get("bioguideId"),
            congress_gov_id=member_data.get("url", "").split("/")[-1],
            first_name=name_parts["first_name"],
            last_name=name_parts["last_name"],
            middle_name=name_parts["middle_name"],
            suffix=name_parts["suffix"],
            nickname=name_parts["nickname"],
            party=member_data.get("partyName", ""),
            chamber=get_chamber_name(chamber),
            state=get_state_abbreviation(member_data.get("state", "")) or "XX",
            district=member_data.get("district"),
            is_current=True,
            official_photo_url=image_url,
            last_scraped_at=datetime.now(),
        )
    
    def _update_member_from_api(self, member: Member, member_data: Dict[str, Any]) -> None:
        """
        Update existing Member object with API data.
        
        Args:
            member: Existing Member object
            member_data: Member data from API
        """
        member.party = member_data.get("partyName", member.party)
        member.chamber = get_chamber_name(member_data.get("chamber", member.chamber))
        member.state = get_state_abbreviation(member_data.get("state", member.state)) or member.state
        member.district = member_data.get("district", member.district)
        member.official_photo_url = member_data.get("imageUrl", member.official_photo_url)
        member.last_scraped_at = datetime.now()
    
    async def update_committees(self, force_refresh: bool = False) -> Dict[str, Any]:
        """
        Update committees from Congress.gov API and web scraping.
        
        Args:
            force_refresh: Force refresh even if recently updated
            
        Returns:
            Update summary
        """
        logger.info("Starting committees update")
        
        db = SessionLocal()
        try:
            # Get committees from API
            house_committees_api = await self.congress_api.get_committees(chamber="house")
            senate_committees_api = await self.congress_api.get_committees(chamber="senate")
            
            # Get committees from web scraping
            house_committees_scraped = await self.house_scraper.scrape_committees()
            senate_committees_scraped = await self.senate_scraper.scrape_committees()
            
            all_committees = (
                house_committees_api + senate_committees_api +
                house_committees_scraped + senate_committees_scraped
            )
            
            updated_count = 0
            created_count = 0
            
            for committee_data in all_committees:
                # Try to find existing committee
                existing_committee = self._find_existing_committee(db, committee_data)
                
                if existing_committee:
                    # Update existing committee
                    self._update_committee_from_data(existing_committee, committee_data)
                    updated_count += 1
                else:
                    # Create new committee
                    new_committee = self._create_committee_from_data(committee_data)
                    db.add(new_committee)
                    created_count += 1
            
            db.commit()
            
            summary = {
                "total_processed": len(all_committees),
                "created": created_count,
                "updated": updated_count,
                "timestamp": datetime.now().isoformat(),
            }
            
            logger.info("Committees update completed", **summary)
            return summary
            
        except Exception as e:
            db.rollback()
            logger.error("Error updating committees", error=str(e))
            raise
        finally:
            db.close()
    
    def _find_existing_committee(self, db: Session, committee_data: Dict[str, Any]) -> Optional[Committee]:
        """
        Find existing committee by various identifiers.
        
        Args:
            db: Database session
            committee_data: Committee data
            
        Returns:
            Existing Committee object or None
        """
        # Try by congress_gov_id first
        congress_gov_id = committee_data.get("congress_gov_id")
        if congress_gov_id:
            committee = db.query(Committee).filter(
                Committee.congress_gov_id == congress_gov_id
            ).first()
            if committee:
                return committee
        
        # Try by committee code
        committee_code = committee_data.get("committee_code")
        if committee_code:
            committee = db.query(Committee).filter(
                Committee.committee_code == committee_code
            ).first()
            if committee:
                return committee
        
        # Try by name and chamber
        name = committee_data.get("name")
        chamber = committee_data.get("chamber")
        if name and chamber:
            committee = db.query(Committee).filter(
                Committee.name == name,
                Committee.chamber == chamber
            ).first()
            if committee:
                return committee
        
        return None
    
    def _create_committee_from_data(self, committee_data: Dict[str, Any]) -> Committee:
        """
        Create Committee object from data.
        
        Args:
            committee_data: Committee data
            
        Returns:
            Committee object
        """
        return Committee(
            congress_gov_id=committee_data.get("congress_gov_id"),
            committee_code=committee_data.get("committee_code"),
            name=committee_data.get("name", ""),
            chamber=committee_data.get("chamber", ""),
            committee_type=committee_data.get("committee_type", "Standing"),
            is_subcommittee=committee_data.get("is_subcommittee", False),
            description=committee_data.get("description"),
            jurisdiction=committee_data.get("jurisdiction"),
            phone=committee_data.get("phone"),
            email=committee_data.get("email"),
            website=committee_data.get("url"),
            office_location=committee_data.get("office_location"),
            is_active=True,
            last_scraped_at=datetime.now(),
        )
    
    def _update_committee_from_data(self, committee: Committee, committee_data: Dict[str, Any]) -> None:
        """
        Update existing Committee object with data.
        
        Args:
            committee: Existing Committee object
            committee_data: Committee data
        """
        committee.description = committee_data.get("description", committee.description)
        committee.jurisdiction = committee_data.get("jurisdiction", committee.jurisdiction)
        committee.phone = committee_data.get("phone", committee.phone)
        committee.email = committee_data.get("email", committee.email)
        committee.website = committee_data.get("url", committee.website)
        committee.office_location = committee_data.get("office_location", committee.office_location)
        committee.last_scraped_at = datetime.now()
    
    async def update_hearings(self, force_refresh: bool = False) -> Dict[str, Any]:
        """
        Update hearings from Congress.gov API and web scraping.
        
        Args:
            force_refresh: Force refresh even if recently updated
            
        Returns:
            Update summary
        """
        logger.info("Starting hearings update")
        
        db = SessionLocal()
        try:
            # Get hearings from API
            hearings_api = await self.congress_api.get_hearings()
            
            # Get hearings from web scraping
            house_hearings_scraped = await self.house_scraper.scrape_hearings()
            senate_hearings_scraped = await self.senate_scraper.scrape_hearings()
            
            all_hearings = hearings_api + house_hearings_scraped + senate_hearings_scraped
            
            updated_count = 0
            created_count = 0
            
            for hearing_data in all_hearings:
                # Try to find existing hearing
                existing_hearing = self._find_existing_hearing(db, hearing_data)
                
                if existing_hearing:
                    # Update existing hearing
                    self._update_hearing_from_data(existing_hearing, hearing_data)
                    updated_count += 1
                else:
                    # Create new hearing
                    new_hearing = self._create_hearing_from_data(hearing_data)
                    db.add(new_hearing)
                    created_count += 1
            
            db.commit()
            
            summary = {
                "total_processed": len(all_hearings),
                "created": created_count,
                "updated": updated_count,
                "timestamp": datetime.now().isoformat(),
            }
            
            logger.info("Hearings update completed", **summary)
            return summary
            
        except Exception as e:
            db.rollback()
            logger.error("Error updating hearings", error=str(e))
            raise
        finally:
            db.close()
    
    def _find_existing_hearing(self, db: Session, hearing_data: Dict[str, Any]) -> Optional[Hearing]:
        """
        Find existing hearing by various identifiers.
        
        Args:
            db: Database session
            hearing_data: Hearing data
            
        Returns:
            Existing Hearing object or None
        """
        # Try by congress_gov_id first
        congress_gov_id = hearing_data.get("congress_gov_id")
        if congress_gov_id:
            hearing = db.query(Hearing).filter(
                Hearing.congress_gov_id == congress_gov_id
            ).first()
            if hearing:
                return hearing
        
        # Try by title and date
        title = hearing_data.get("title")
        scheduled_date = hearing_data.get("scheduled_date")
        if title and scheduled_date:
            hearing = db.query(Hearing).filter(
                Hearing.title == title,
                Hearing.scheduled_date == scheduled_date
            ).first()
            if hearing:
                return hearing
        
        return None
    
    def _create_hearing_from_data(self, hearing_data: Dict[str, Any]) -> Hearing:
        """
        Create Hearing object from data.
        
        Args:
            hearing_data: Hearing data
            
        Returns:
            Hearing object
        """
        return Hearing(
            congress_gov_id=hearing_data.get("congress_gov_id"),
            title=hearing_data.get("title", ""),
            description=hearing_data.get("description"),
            scheduled_date=hearing_data.get("scheduled_date"),
            location=hearing_data.get("location"),
            hearing_type=hearing_data.get("hearing_type"),
            status=hearing_data.get("status", "Scheduled"),
            video_url=hearing_data.get("video_url"),
            webcast_url=hearing_data.get("webcast_url"),
            scraped_video_urls=hearing_data.get("video_urls", []),
            last_scraped_at=datetime.now(),
        )
    
    def _update_hearing_from_data(self, hearing: Hearing, hearing_data: Dict[str, Any]) -> None:
        """
        Update existing Hearing object with data.
        
        Args:
            hearing: Existing Hearing object
            hearing_data: Hearing data
        """
        hearing.description = hearing_data.get("description", hearing.description)
        hearing.location = hearing_data.get("location", hearing.location)
        hearing.status = hearing_data.get("status", hearing.status)
        hearing.video_url = hearing_data.get("video_url", hearing.video_url)
        hearing.webcast_url = hearing_data.get("webcast_url", hearing.webcast_url)
        
        # Update scraped video URLs
        new_video_urls = hearing_data.get("video_urls", [])
        if new_video_urls:
            existing_urls = hearing.scraped_video_urls or []
            hearing.scraped_video_urls = list(set(existing_urls + new_video_urls))
        
        hearing.last_scraped_at = datetime.now()
    
    async def full_update(self) -> Dict[str, Any]:
        """
        Perform full update of all data sources.
        
        Returns:
            Summary of all updates
        """
        logger.info("Starting full data update")
        
        results = {}
        
        try:
            # Update members
            results["members"] = await self.update_members()
            
            # Update committees
            results["committees"] = await self.update_committees()
            
            # Update hearings
            results["hearings"] = await self.update_hearings()
            
            results["full_update_completed"] = datetime.now().isoformat()
            
            logger.info("Full data update completed", **results)
            return results
            
        except Exception as e:
            logger.error("Error during full data update", error=str(e))
            raise