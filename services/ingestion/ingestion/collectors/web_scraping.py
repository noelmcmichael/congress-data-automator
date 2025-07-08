"""
Web scraping collector for congressional websites.

This module provides enterprise-grade web scraping capabilities for:
- House.gov committee pages
- Senate.gov committee pages  
- Individual committee websites
- Hearing information and documents
"""

import asyncio
import time
from typing import Dict, List, Optional, Any, Set
from urllib.parse import urljoin, urlparse
import httpx
from bs4 import BeautifulSoup, Tag
from pydantic import BaseModel, Field, HttpUrl
import structlog

from ..core.config import settings
from ..core.logging import LoggerMixin


class ScrapingResult(BaseModel):
    """Result of a web scraping operation."""
    success: bool
    url: str
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    response_time_ms: Optional[float] = None
    status_code: Optional[int] = None


class WebScrapingCollector(LoggerMixin):
    """
    Enterprise-grade web scraping collector for congressional websites.
    
    Features:
    - Rate limiting and respectful crawling
    - Retry logic with exponential backoff
    - Robust HTML parsing and error handling
    - Structured logging and metrics
    - Circuit breaker for failed domains
    """
    
    def __init__(self):
        super().__init__()
        self.request_delay = settings.scraping_delay
        self.timeout = settings.scraping_timeout
        self.max_retries = settings.scraping_max_retries
        
        # Rate limiting state
        self.last_request_time = 0.0
        self.failed_domains: Set[str] = set()
        self.domain_failure_counts: Dict[str, int] = {}
        
        # Headers for respectful scraping
        self.headers = {
            "User-Agent": settings.scraping_user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }
        
        # HTTP client with connection pooling
        self.client = httpx.AsyncClient(
            timeout=self.timeout,
            follow_redirects=True,
            limits=httpx.Limits(max_keepalive_connections=10, max_connections=20),
            headers=self.headers
        )
        
        self.logger.info(
            "Web scraping collector initialized",
            request_delay=self.request_delay,
            timeout=self.timeout,
            max_retries=self.max_retries
        )

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit with cleanup."""
        await self.client.aclose()

    async def _make_request(self, url: str) -> ScrapingResult:
        """
        Make a rate-limited HTTP request with error handling.
        
        Args:
            url: URL to scrape
            
        Returns:
            ScrapingResult: Result with HTML content or error
        """
        start_time = time.time()
        domain = urlparse(url).netloc
        
        # Check if domain is in circuit breaker mode
        if domain in self.failed_domains:
            return ScrapingResult(
                success=False,
                url=url,
                error=f"Domain {domain} is in circuit breaker mode"
            )
        
        # Rate limiting
        await self._enforce_rate_limit()
        
        # Retry logic
        last_exception = None
        for attempt in range(self.max_retries + 1):
            try:
                self.log_operation_start(
                    "web_scraping_request",
                    url=url,
                    attempt=attempt + 1,
                    domain=domain
                )
                
                response = await self.client.get(url)
                response_time_ms = (time.time() - start_time) * 1000
                
                # Check for successful response
                if response.status_code == 200:
                    # Reset failure count on success
                    self.domain_failure_counts.pop(domain, None)
                    
                    self.log_operation_success(
                        "web_scraping_request",
                        duration_ms=response_time_ms,
                        status_code=response.status_code,
                        content_length=len(response.content),
                        url=url
                    )
                    
                    return ScrapingResult(
                        success=True,
                        url=url,
                        data={"html": response.text, "headers": dict(response.headers)},
                        response_time_ms=response_time_ms,
                        status_code=response.status_code
                    )
                
                # Handle non-200 status codes
                self.logger.warning(
                    "Non-200 status code",
                    url=url,
                    status_code=response.status_code,
                    attempt=attempt + 1
                )
                
                if attempt < self.max_retries and response.status_code >= 500:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                    continue
                
                return ScrapingResult(
                    success=False,
                    url=url,
                    error=f"HTTP {response.status_code}",
                    status_code=response.status_code,
                    response_time_ms=response_time_ms
                )
                
            except Exception as e:
                last_exception = e
                self.logger.warning(
                    "Error during web scraping request",
                    error_type=type(e).__name__,
                    error_message=str(e),
                    attempt=attempt + 1,
                    url=url
                )
                
                if attempt < self.max_retries:
                    await asyncio.sleep(2 ** attempt)
                    continue
        
        # All retries failed - update failure tracking
        self._track_domain_failure(domain)
        response_time_ms = (time.time() - start_time) * 1000
        
        self.log_operation_error(
            "web_scraping_request",
            last_exception or Exception("All retries failed"),
            duration_ms=response_time_ms,
            url=url
        )
        
        return ScrapingResult(
            success=False,
            url=url,
            error=str(last_exception) if last_exception else "All retries failed",
            response_time_ms=response_time_ms
        )

    async def _enforce_rate_limit(self) -> None:
        """Enforce minimum delay between requests."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.request_delay:
            sleep_time = self.request_delay - time_since_last
            self.logger.debug(
                "Rate limiting delay",
                sleep_time_ms=sleep_time * 1000
            )
            await asyncio.sleep(sleep_time)
        
        self.last_request_time = time.time()

    def _track_domain_failure(self, domain: str) -> None:
        """Track domain failures and implement circuit breaker."""
        failure_count = self.domain_failure_counts.get(domain, 0) + 1
        self.domain_failure_counts[domain] = failure_count
        
        # Circuit breaker: disable domain after 5 consecutive failures
        if failure_count >= 5:
            self.failed_domains.add(domain)
            self.logger.warning(
                "Domain added to circuit breaker",
                domain=domain,
                failure_count=failure_count
            )

    def _parse_html(self, html: str, url: str) -> BeautifulSoup:
        """
        Parse HTML content with error handling.
        
        Args:
            html: Raw HTML content
            url: Source URL for error reporting
            
        Returns:
            BeautifulSoup: Parsed HTML document
        """
        try:
            soup = BeautifulSoup(html, 'lxml')
            return soup
        except Exception as e:
            self.logger.error(
                "HTML parsing failed",
                url=url,
                error_type=type(e).__name__,
                error_message=str(e)
            )
            # Fallback to html.parser
            return BeautifulSoup(html, 'html.parser')

    async def scrape_committee_hearings(
        self, 
        committee_url: str
    ) -> List[Dict[str, Any]]:
        """
        Scrape hearing information from a committee page.
        
        Args:
            committee_url: URL of the committee page
            
        Returns:
            List[Dict[str, Any]]: List of hearing data
        """
        self.log_operation_start(
            "scrape_committee_hearings",
            committee_url=committee_url
        )
        
        result = await self._make_request(committee_url)
        
        if not result.success:
            self.logger.error(
                "Failed to fetch committee page",
                url=committee_url,
                error=result.error
            )
            return []
        
        soup = self._parse_html(result.data["html"], committee_url)
        hearings = []
        
        try:
            # House.gov hearing patterns
            if "house.gov" in committee_url:
                hearings = self._parse_house_hearings(soup, committee_url)
            
            # Senate.gov hearing patterns
            elif "senate.gov" in committee_url:
                hearings = self._parse_senate_hearings(soup, committee_url)
            
            # Generic hearing patterns for other sites
            else:
                hearings = self._parse_generic_hearings(soup, committee_url)
            
            self.log_operation_success(
                "scrape_committee_hearings",
                committee_url=committee_url,
                hearings_found=len(hearings)
            )
            
        except Exception as e:
            self.log_operation_error(
                "scrape_committee_hearings",
                e,
                committee_url=committee_url
            )
        
        return hearings

    def _parse_house_hearings(
        self, 
        soup: BeautifulSoup, 
        base_url: str
    ) -> List[Dict[str, Any]]:
        """Parse hearings from House.gov committee pages."""
        hearings = []
        
        # Common House.gov hearing selectors
        hearing_selectors = [
            '.hearing-item',
            '.hearing',
            '.event-item',
            '[class*="hearing"]',
            '[class*="event"]'
        ]
        
        for selector in hearing_selectors:
            elements = soup.select(selector)
            if elements:
                break
        
        for element in elements:
            try:
                hearing = self._extract_hearing_data(element, base_url)
                if hearing:
                    hearings.append(hearing)
            except Exception as e:
                self.logger.debug(
                    "Failed to parse hearing element",
                    selector=selector,
                    error=str(e)
                )
        
        return hearings

    def _parse_senate_hearings(
        self, 
        soup: BeautifulSoup, 
        base_url: str
    ) -> List[Dict[str, Any]]:
        """Parse hearings from Senate.gov committee pages."""
        hearings = []
        
        # Common Senate.gov hearing selectors
        hearing_selectors = [
            '.hearing',
            '.event',
            '.schedule-item',
            '[class*="hearing"]',
            '[class*="schedule"]'
        ]
        
        for selector in hearing_selectors:
            elements = soup.select(selector)
            if elements:
                break
        
        for element in elements:
            try:
                hearing = self._extract_hearing_data(element, base_url)
                if hearing:
                    hearings.append(hearing)
            except Exception as e:
                self.logger.debug(
                    "Failed to parse hearing element",
                    selector=selector,
                    error=str(e)
                )
        
        return hearings

    def _parse_generic_hearings(
        self, 
        soup: BeautifulSoup, 
        base_url: str
    ) -> List[Dict[str, Any]]:
        """Parse hearings using generic patterns."""
        hearings = []
        
        # Generic selectors for hearing-related content
        selectors = [
            'a[href*="hearing"]',
            'a[href*="event"]',
            'a[href*="schedule"]',
            '[class*="hearing"]',
            '[class*="event"]'
        ]
        
        for selector in selectors:
            elements = soup.select(selector)
            for element in elements[:10]:  # Limit to avoid noise
                try:
                    hearing = self._extract_hearing_data(element, base_url)
                    if hearing and hearing not in hearings:
                        hearings.append(hearing)
                except Exception:
                    continue
        
        return hearings

    def _extract_hearing_data(
        self, 
        element: Tag, 
        base_url: str
    ) -> Optional[Dict[str, Any]]:
        """
        Extract hearing data from an HTML element.
        
        Args:
            element: BeautifulSoup element containing hearing info
            base_url: Base URL for resolving relative links
            
        Returns:
            Optional[Dict[str, Any]]: Hearing data or None if extraction fails
        """
        try:
            # Extract title
            title = None
            title_selectors = ['h1', 'h2', 'h3', 'h4', '.title', '.heading']
            for selector in title_selectors:
                title_elem = element.select_one(selector)
                if title_elem and title_elem.get_text(strip=True):
                    title = title_elem.get_text(strip=True)
                    break
            
            # Fallback: use element text or link text
            if not title:
                title = element.get_text(strip=True)
                if len(title) > 200:  # Too long, likely not a title
                    title = title[:200] + "..."
            
            # Extract URL
            url = None
            if element.name == 'a' and element.get('href'):
                url = urljoin(base_url, element.get('href'))
            else:
                link = element.find('a')
                if link and link.get('href'):
                    url = urljoin(base_url, link.get('href'))
            
            # Extract date/time if available
            date_time = None
            date_selectors = ['.date', '.time', '.datetime', '[class*="date"]']
            for selector in date_selectors:
                date_elem = element.select_one(selector)
                if date_elem:
                    date_time = date_elem.get_text(strip=True)
                    break
            
            # Extract location if available
            location = None
            location_selectors = ['.location', '.room', '.venue', '[class*="location"]']
            for selector in location_selectors:
                location_elem = element.select_one(selector)
                if location_elem:
                    location = location_elem.get_text(strip=True)
                    break
            
            # Only return if we have meaningful data
            if title and len(title.strip()) > 3:
                return {
                    "title": title,
                    "url": url,
                    "date_time": date_time,
                    "location": location,
                    "source_url": base_url,
                    "scraped_at": time.time()
                }
        
        except Exception as e:
            self.logger.debug(
                "Failed to extract hearing data",
                error=str(e),
                element_tag=element.name if hasattr(element, 'name') else 'unknown'
            )
        
        return None

    async def validate_url(self, url: str) -> bool:
        """
        Validate if a URL is accessible.
        
        Args:
            url: URL to validate
            
        Returns:
            bool: True if URL is accessible, False otherwise
        """
        try:
            result = await self._make_request(url)
            return result.success and result.status_code == 200
        except Exception:
            return False

    def get_failed_domains(self) -> Set[str]:
        """Get set of domains in circuit breaker mode."""
        return self.failed_domains.copy()

    def reset_circuit_breaker(self, domain: Optional[str] = None) -> None:
        """
        Reset circuit breaker for a domain or all domains.
        
        Args:
            domain: Specific domain to reset, or None for all domains
        """
        if domain:
            self.failed_domains.discard(domain)
            self.domain_failure_counts.pop(domain, None)
            self.logger.info("Circuit breaker reset for domain", domain=domain)
        else:
            self.failed_domains.clear()
            self.domain_failure_counts.clear()
            self.logger.info("Circuit breaker reset for all domains")