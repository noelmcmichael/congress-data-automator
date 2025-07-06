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
        Get all congressional members by fetching from both chambers.
        
        Args:
            current_only: Only return current members
            
        Returns:
            List of all member data
        """
        all_members = []
        
        # Get House members
        logger.info("Fetching House members...")
        house_members = await self.get_members(chamber="house", current_only=current_only)
        all_members.extend(house_members)
        logger.info(f"Fetched {len(house_members)} House members")
        
        # Get Senate members
        logger.info("Fetching Senate members...")
        senate_members = await self.get_members(chamber="senate", current_only=current_only)
        all_members.extend(senate_members)
        logger.info(f"Fetched {len(senate_members)} Senate members")
        
        # Deduplicate by bioguide_id
        members_dict = {}
        for member in all_members:
            bioguide_id = member.get("bioguideId")
            if bioguide_id and bioguide_id not in members_dict:
                members_dict[bioguide_id] = member
        
        deduplicated_members = list(members_dict.values())
        logger.info(f"Total members after deduplication: {len(deduplicated_members)}")
        
        return deduplicated_members
    
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