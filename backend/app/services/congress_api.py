"""
Congress.gov API client with rate limiting and error handling.
"""
import asyncio
import time
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import httpx
import structlog
from ..core.config import settings

logger = structlog.get_logger()


class CongressApiClient:
    """
    Client for the Congress.gov API with rate limiting and error handling.
    """
    
    def __init__(self):
        self.base_url = settings.congress_api_base_url
        self.api_key = settings.congress_api_key
        self.request_delay = settings.congress_api_request_delay
        self.last_request_time = 0
        self.daily_request_count = 0
        self.daily_request_limit = settings.congress_api_rate_limit
        self.request_count_reset_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Default headers
        self.headers = {
            "X-API-Key": self.api_key,
            "User-Agent": settings.scraping_user_agent,
            "Accept": "application/json",
        }
    
    async def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make a rate-limited request to the Congress.gov API.
        
        Args:
            endpoint: API endpoint path
            params: Query parameters
            
        Returns:
            JSON response data
            
        Raises:
            httpx.HTTPError: If request fails
            ValueError: If daily rate limit exceeded
        """
        # Check and reset daily request count
        now = datetime.now()
        if now >= self.request_count_reset_time + timedelta(days=1):
            self.daily_request_count = 0
            self.request_count_reset_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Check daily rate limit
        if self.daily_request_count >= self.daily_request_limit:
            raise ValueError(f"Daily rate limit of {self.daily_request_limit} requests exceeded")
        
        # Rate limiting - ensure minimum delay between requests
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.request_delay:
            await asyncio.sleep(self.request_delay - time_since_last)
        
        # Make the request
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, headers=self.headers, params=params or {})
            
        self.last_request_time = time.time()
        self.daily_request_count += 1
        
        # Log request
        logger.info(
            "Congress API request",
            url=url,
            status_code=response.status_code,
            daily_count=self.daily_request_count,
        )
        
        response.raise_for_status()
        return response.json()
    
    async def get_members(self, chamber: Optional[str] = None, state: Optional[str] = None, 
                         current_only: bool = True, limit: int = 250) -> List[Dict[str, Any]]:
        """
        Get congressional members.
        
        Args:
            chamber: Filter by chamber (house, senate)
            state: Filter by state abbreviation
            current_only: Only return current members
            limit: Maximum number of members to return per request
            
        Returns:
            List of member data
        """
        params = {"limit": limit}
        if chamber:
            params["chamber"] = chamber.lower()
        if state:
            params["state"] = state.upper()
        if current_only:
            params["currentMember"] = "true"
        
        response = await self._make_request("/member", params)
        return response.get("members", [])
    
    async def get_all_members(self, current_only: bool = True) -> List[Dict[str, Any]]:
        """
        Get all congressional members using pagination to fetch complete dataset.
        
        Args:
            current_only: Only return current members
            
        Returns:
            List of all member data
        """
        all_members = []
        members_dict = {}
        
        # Use pagination to get all members
        offset = 0
        limit = 250
        
        logger.info("Starting comprehensive member collection with pagination...")
        
        while True:
            # Fetch batch of members
            params = {"limit": limit, "offset": offset}
            if current_only:
                params["currentMember"] = "true"
            
            logger.info(f"Fetching members batch (offset={offset}, limit={limit})...")
            response = await self._make_request("/member", params)
            batch_members = response.get("members", [])
            
            if not batch_members:
                logger.info(f"No more members found at offset {offset}")
                break
            
            # Add to collection and deduplicate
            for member in batch_members:
                bioguide_id = member.get("bioguideId")
                if bioguide_id and bioguide_id not in members_dict:
                    members_dict[bioguide_id] = member
            
            logger.info(f"Batch {offset//limit + 1}: Got {len(batch_members)} members, total unique: {len(members_dict)}")
            
            # If we got less than the limit, we've reached the end
            if len(batch_members) < limit:
                logger.info("Reached end of members data")
                break
            
            offset += limit
            
            # Safety check to prevent infinite loops
            if offset > 5000:  # Reasonable upper bound
                logger.warning(f"Reached safety limit at offset {offset}")
                break
        
        all_members = list(members_dict.values())
        logger.info(f"Comprehensive member collection completed: {len(all_members)} unique members")
        
        return all_members
    
    async def get_member_details(self, bioguide_id: str) -> Dict[str, Any]:
        """
        Get detailed information for a specific member.
        
        Args:
            bioguide_id: Member's bioguide ID
            
        Returns:
            Member details
        """
        response = await self._make_request(f"/member/{bioguide_id}")
        return response.get("member", {})
    
    async def get_committees(self, chamber: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get congressional committees.
        
        Args:
            chamber: Filter by chamber (house, senate, joint)
            
        Returns:
            List of committee data
        """
        params = {}
        if chamber:
            params["chamber"] = chamber.lower()
        
        response = await self._make_request("/committee", params)
        return response.get("committees", [])
    
    async def get_committee_details(self, committee_code: str) -> Dict[str, Any]:
        """
        Get detailed information for a specific committee.
        
        Args:
            committee_code: Committee code
            
        Returns:
            Committee details
        """
        response = await self._make_request(f"/committee/{committee_code}")
        return response.get("committee", {})
    
    async def get_committee_members(self, committee_code: str) -> List[Dict[str, Any]]:
        """
        Get members of a specific committee.
        
        Args:
            committee_code: Committee code
            
        Returns:
            List of committee members
        """
        response = await self._make_request(f"/committee/{committee_code}/member")
        return response.get("members", [])
    
    async def get_hearings(self, committee_code: Optional[str] = None, 
                          start_date: Optional[datetime] = None,
                          end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """
        Get congressional hearings.
        
        Args:
            committee_code: Filter by committee
            start_date: Filter by start date
            end_date: Filter by end date
            
        Returns:
            List of hearing data
        """
        params = {}
        if committee_code:
            params["committee"] = committee_code
        if start_date:
            params["fromDateTime"] = start_date.isoformat()
        if end_date:
            params["toDateTime"] = end_date.isoformat()
        
        response = await self._make_request("/hearing", params)
        return response.get("hearings", [])
    
    async def get_member_committees(self, bioguide_id: str) -> List[Dict[str, Any]]:
        """
        Get committee memberships for a specific member.
        
        Args:
            bioguide_id: Member's bioguide ID
            
        Returns:
            List of committee memberships
        """
        try:
            response = await self._make_request(f"/member/{bioguide_id}/committee-assignment")
            return response.get("committeeAssignments", [])
        except Exception as e:
            logger.warning(f"Could not get committee assignments for {bioguide_id}: {e}")
            return []
    
    async def get_all_committee_memberships(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get all committee memberships for all members.
        
        Returns:
            Dictionary mapping bioguide_id to list of committee memberships
        """
        all_memberships = {}
        
        # First, get all members
        members = await self.get_all_members()
        
        logger.info(f"Fetching committee memberships for {len(members)} members...")
        
        for i, member in enumerate(members):
            bioguide_id = member.get("bioguideId")
            if not bioguide_id:
                continue
            
            try:
                memberships = await self.get_member_committees(bioguide_id)
                all_memberships[bioguide_id] = memberships
                
                if (i + 1) % 50 == 0:
                    logger.info(f"Processed {i + 1}/{len(members)} members")
                
            except Exception as e:
                logger.error(f"Error getting committees for member {bioguide_id}: {e}")
                all_memberships[bioguide_id] = []
        
        logger.info(f"Committee membership collection completed for {len(all_memberships)} members")
        return all_memberships
    
    async def get_committee_hierarchy(self) -> Dict[str, Any]:
        """
        Get committee hierarchy information including parent-child relationships.
        
        Returns:
            Dictionary with committee hierarchy data
        """
        # Get all committees
        committees = await self.get_committees()
        
        hierarchy = {
            "committees": [],
            "subcommittees": [],
            "relationships": []
        }
        
        for committee in committees:
            committee_data = {
                "name": committee.get("name", ""),
                "chamber": committee.get("chamber", ""),
                "committee_code": committee.get("systemCode", ""),
                "congress_gov_id": committee.get("url", "").split("/")[-1] if committee.get("url") else None,
                "committee_type": committee.get("type", "Standing"),
                "is_subcommittee": committee.get("type", "").lower() == "subcommittee",
                "parent_code": committee.get("parentCommitteeCode")
            }
            
            if committee_data["is_subcommittee"]:
                hierarchy["subcommittees"].append(committee_data)
            else:
                hierarchy["committees"].append(committee_data)
            
            # Add parent-child relationship
            if committee_data["parent_code"]:
                hierarchy["relationships"].append({
                    "child": committee_data["committee_code"],
                    "parent": committee_data["parent_code"]
                })
        
        return hierarchy
    
    async def get_hearing_details(self, hearing_id: str) -> Dict[str, Any]:
        """
        Get detailed information for a specific hearing.
        
        Args:
            hearing_id: Hearing ID
            
        Returns:
            Hearing details
        """
        response = await self._make_request(f"/hearing/{hearing_id}")
        return response.get("hearing", {})
    
    async def search_bills(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Search for bills and resolutions.
        
        Args:
            query: Search query
            limit: Maximum number of results
            
        Returns:
            List of bill data
        """
        params = {
            "query": query,
            "limit": limit,
        }
        
        response = await self._make_request("/bill", params)
        return response.get("bills", [])
    
    def get_rate_limit_status(self) -> Dict[str, Any]:
        """
        Get current rate limit status.
        
        Returns:
            Rate limit information
        """
        return {
            "daily_limit": self.daily_request_limit,
            "daily_count": self.daily_request_count,
            "remaining": self.daily_request_limit - self.daily_request_count,
            "reset_time": self.request_count_reset_time.isoformat(),
        }