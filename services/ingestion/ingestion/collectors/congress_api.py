"""
Congress.gov API collector with enterprise-grade reliability and observability.

This module provides a robust client for the Congress.gov API with:
- Comprehensive rate limiting and error handling
- Structured logging and metrics
- Type safety and data validation
- Retry logic and circuit breaker patterns
"""

import asyncio
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
import httpx
from pydantic import BaseModel, Field, validator
import structlog

from ..core.config import settings
from ..core.logging import LoggerMixin


class RateLimitStatus(BaseModel):
    """Rate limit status information."""
    daily_limit: int
    daily_count: int
    remaining: int
    reset_time: datetime
    last_request_time: float


class ApiResponse(BaseModel):
    """Standardized API response wrapper."""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    rate_limit: Optional[RateLimitStatus] = None
    response_time_ms: Optional[float] = None


class CongressApiCollector(LoggerMixin):
    """
    Enterprise-grade Congress.gov API client.
    
    Features:
    - Rate limiting (5000 requests/day)
    - Automatic retries with exponential backoff
    - Comprehensive error handling and logging
    - Request/response metrics
    - Type-safe data collection
    """
    
    def __init__(self):
        super().__init__()
        self.base_url = settings.congress_api_base_url
        self.api_key = settings.congress_api_key
        self.request_delay = settings.congress_api_request_delay
        self.timeout = settings.congress_api_timeout
        
        # Rate limiting state
        self.last_request_time = 0.0
        self.daily_request_count = 0
        self.daily_request_limit = settings.congress_api_rate_limit
        self.request_count_reset_time = datetime.now().replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        
        # Default headers
        self.headers = {
            "X-API-Key": self.api_key,
            "User-Agent": settings.scraping_user_agent,
            "Accept": "application/json",
        }
        
        # HTTP client with connection pooling
        self.client = httpx.AsyncClient(
            timeout=self.timeout,
            limits=httpx.Limits(max_keepalive_connections=5, max_connections=10)
        )
        
        self.logger.info(
            "Congress API collector initialized",
            base_url=self.base_url,
            rate_limit=self.daily_request_limit,
            request_delay=self.request_delay
        )

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit with cleanup."""
        await self.client.aclose()

    async def _make_request(
        self, 
        endpoint: str, 
        params: Optional[Dict[str, Any]] = None,
        max_retries: int = 3
    ) -> ApiResponse:
        """
        Make a rate-limited request to the Congress.gov API.
        
        Args:
            endpoint: API endpoint path
            params: Query parameters
            max_retries: Maximum number of retry attempts
            
        Returns:
            ApiResponse: Standardized response with data or error
        """
        start_time = time.time()
        
        # Check and reset daily request count
        await self._check_rate_limit_reset()
        
        # Check daily rate limit
        if self.daily_request_count >= self.daily_request_limit:
            error_msg = f"Daily rate limit of {self.daily_request_limit} requests exceeded"
            self.logger.error("Rate limit exceeded", daily_count=self.daily_request_count)
            return ApiResponse(success=False, error=error_msg)
        
        # Rate limiting - ensure minimum delay between requests
        await self._enforce_rate_limit()
        
        # Construct URL
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        # Retry logic with exponential backoff
        last_exception = None
        for attempt in range(max_retries + 1):
            try:
                self.log_operation_start(
                    "congress_api_request",
                    url=url,
                    attempt=attempt + 1,
                    params=params
                )
                
                response = await self.client.get(
                    url, 
                    headers=self.headers, 
                    params=params or {}
                )
                
                # Update rate limiting state
                self.last_request_time = time.time()
                self.daily_request_count += 1
                response_time_ms = (time.time() - start_time) * 1000
                
                # Handle HTTP errors
                if response.status_code == 429:  # Rate limited
                    self.logger.warning(
                        "Rate limited by API",
                        status_code=response.status_code,
                        attempt=attempt + 1
                    )
                    if attempt < max_retries:
                        await asyncio.sleep(2 ** attempt)  # Exponential backoff
                        continue
                
                response.raise_for_status()
                
                # Parse JSON response
                data = response.json()
                
                rate_limit_status = RateLimitStatus(
                    daily_limit=self.daily_request_limit,
                    daily_count=self.daily_request_count,
                    remaining=self.daily_request_limit - self.daily_request_count,
                    reset_time=self.request_count_reset_time,
                    last_request_time=self.last_request_time
                )
                
                self.log_operation_success(
                    "congress_api_request",
                    duration_ms=response_time_ms,
                    status_code=response.status_code,
                    daily_count=self.daily_request_count,
                    url=url
                )
                
                return ApiResponse(
                    success=True,
                    data=data,
                    rate_limit=rate_limit_status,
                    response_time_ms=response_time_ms
                )
                
            except httpx.HTTPError as e:
                last_exception = e
                self.logger.warning(
                    "HTTP error during API request",
                    error_type=type(e).__name__,
                    error_message=str(e),
                    attempt=attempt + 1,
                    url=url
                )
                
                if attempt < max_retries:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                    continue
                    
            except Exception as e:
                last_exception = e
                self.logger.error(
                    "Unexpected error during API request",
                    error_type=type(e).__name__,
                    error_message=str(e),
                    attempt=attempt + 1,
                    url=url,
                    exc_info=e
                )
                break
        
        # All retries failed
        response_time_ms = (time.time() - start_time) * 1000
        self.log_operation_error(
            "congress_api_request",
            last_exception or Exception("All retries failed"),
            duration_ms=response_time_ms,
            url=url,
            max_retries=max_retries
        )
        
        return ApiResponse(
            success=False,
            error=str(last_exception) if last_exception else "All retries failed",
            response_time_ms=response_time_ms
        )

    async def _check_rate_limit_reset(self) -> None:
        """Check if daily rate limit should be reset."""
        now = datetime.now()
        if now >= self.request_count_reset_time + timedelta(days=1):
            old_count = self.daily_request_count
            self.daily_request_count = 0
            self.request_count_reset_time = now.replace(
                hour=0, minute=0, second=0, microsecond=0
            )
            
            self.logger.info(
                "Daily rate limit reset",
                old_count=old_count,
                reset_time=self.request_count_reset_time.isoformat()
            )

    async def _enforce_rate_limit(self) -> None:
        """Enforce minimum delay between requests."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.request_delay:
            sleep_time = self.request_delay - time_since_last
            self.logger.debug(
                "Rate limiting delay",
                sleep_time_ms=sleep_time * 1000,
                time_since_last_ms=time_since_last * 1000
            )
            await asyncio.sleep(sleep_time)

    async def collect_all_members(self, current_only: bool = True) -> List[Dict[str, Any]]:
        """
        Collect all congressional members using pagination.
        
        Args:
            current_only: Only return current members
            
        Returns:
            List[Dict[str, Any]]: List of member data
        """
        self.log_operation_start(
            "collect_all_members",
            current_only=current_only
        )
        
        all_members = []
        members_dict = {}
        offset = 0
        limit = 250
        
        while True:
            params = {"limit": limit, "offset": offset}
            if current_only:
                params["currentMember"] = "true"
            
            self.logger.debug(
                "Fetching members batch",
                offset=offset,
                limit=limit,
                current_only=current_only
            )
            
            response = await self._make_request("/member", params)
            
            if not response.success:
                raise Exception(f"Failed to fetch members: {response.error}")
            
            batch_members = response.data.get("members", [])
            
            if not batch_members:
                self.logger.debug("No more members found", offset=offset)
                break
            
            # Deduplicate by bioguide_id
            for member in batch_members:
                bioguide_id = member.get("bioguideId")
                if bioguide_id and bioguide_id not in members_dict:
                    members_dict[bioguide_id] = member
            
            self.logger.debug(
                "Members batch processed",
                batch_size=len(batch_members),
                total_unique=len(members_dict),
                offset=offset
            )
            
            # Check if we reached the end
            if len(batch_members) < limit:
                break
            
            offset += limit
            
            # Safety check
            if offset > 10000:
                self.logger.warning("Reached safety limit", offset=offset)
                break
        
        all_members = list(members_dict.values())
        
        self.log_operation_success(
            "collect_all_members",
            total_members=len(all_members),
            unique_members=len(members_dict),
            current_only=current_only
        )
        
        return all_members

    async def collect_all_committees(
        self, 
        chamber: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Collect all congressional committees.
        
        Args:
            chamber: Filter by chamber (house, senate, joint)
            
        Returns:
            List[Dict[str, Any]]: List of committee data
        """
        self.log_operation_start(
            "collect_all_committees",
            chamber=chamber
        )
        
        params = {}
        if chamber:
            params["chamber"] = chamber.lower()
        
        response = await self._make_request("/committee", params)
        
        if not response.success:
            raise Exception(f"Failed to fetch committees: {response.error}")
        
        committees = response.data.get("committees", [])
        
        self.log_operation_success(
            "collect_all_committees",
            total_committees=len(committees),
            chamber=chamber
        )
        
        return committees

    async def collect_recent_hearings(
        self,
        days_back: int = 30,
        committee_code: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Collect recent congressional hearings.
        
        Args:
            days_back: Number of days to look back
            committee_code: Filter by specific committee
            
        Returns:
            List[Dict[str, Any]]: List of hearing data
        """
        self.log_operation_start(
            "collect_recent_hearings",
            days_back=days_back,
            committee_code=committee_code
        )
        
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        
        params = {
            "fromDateTime": start_date.isoformat(),
            "toDateTime": end_date.isoformat()
        }
        
        if committee_code:
            params["committee"] = committee_code
        
        response = await self._make_request("/hearing", params)
        
        if not response.success:
            raise Exception(f"Failed to fetch hearings: {response.error}")
        
        hearings = response.data.get("hearings", [])
        
        self.log_operation_success(
            "collect_recent_hearings",
            total_hearings=len(hearings),
            days_back=days_back,
            committee_code=committee_code
        )
        
        return hearings

    def get_rate_limit_status(self) -> RateLimitStatus:
        """
        Get current rate limit status.
        
        Returns:
            RateLimitStatus: Current rate limiting information
        """
        return RateLimitStatus(
            daily_limit=self.daily_request_limit,
            daily_count=self.daily_request_count,
            remaining=self.daily_request_limit - self.daily_request_count,
            reset_time=self.request_count_reset_time,
            last_request_time=self.last_request_time
        )