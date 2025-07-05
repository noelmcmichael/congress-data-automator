"""
Base scraper class with common functionality.
"""
import asyncio
import time
from typing import Dict, List, Optional, Any, Union
from urllib.parse import urljoin, urlparse
import httpx
from bs4 import BeautifulSoup
import structlog
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'app'))
from core.config import settings

logger = structlog.get_logger()


class BaseScraper:
    """
    Base class for web scrapers with rate limiting and error handling.
    """
    
    def __init__(self, base_url: str, name: str):
        self.base_url = base_url
        self.name = name
        self.last_request_time = 0
        self.request_delay = settings.scraping_delay
        self.timeout = settings.scraping_timeout
        
        # Default headers
        self.headers = {
            "User-Agent": settings.scraping_user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }
    
    async def _make_request(self, url: str, **kwargs) -> httpx.Response:
        """
        Make a rate-limited HTTP request.
        
        Args:
            url: URL to request
            **kwargs: Additional arguments for httpx.get
            
        Returns:
            HTTP response
            
        Raises:
            httpx.HTTPError: If request fails
        """
        # Rate limiting
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.request_delay:
            await asyncio.sleep(self.request_delay - time_since_last)
        
        # Make the request
        async with httpx.AsyncClient(
            timeout=self.timeout,
            headers=self.headers,
            **kwargs
        ) as client:
            response = await client.get(url)
            
        self.last_request_time = time.time()
        
        # Log request
        logger.info(
            "Scraper request",
            scraper=self.name,
            url=url,
            status_code=response.status_code,
            content_length=len(response.content),
        )
        
        response.raise_for_status()
        return response
    
    async def fetch_page(self, url: str) -> BeautifulSoup:
        """
        Fetch a web page and return BeautifulSoup object.
        
        Args:
            url: URL to fetch
            
        Returns:
            BeautifulSoup object
        """
        response = await self._make_request(url)
        return BeautifulSoup(response.content, 'html.parser')
    
    def make_absolute_url(self, url: str) -> str:
        """
        Convert relative URL to absolute URL.
        
        Args:
            url: Relative or absolute URL
            
        Returns:
            Absolute URL
        """
        return urljoin(self.base_url, url)
    
    def extract_text(self, element, strip: bool = True) -> str:
        """
        Extract text from BeautifulSoup element.
        
        Args:
            element: BeautifulSoup element
            strip: Whether to strip whitespace
            
        Returns:
            Extracted text
        """
        if element is None:
            return ""
        
        text = element.get_text()
        if strip:
            text = text.strip()
        
        return text
    
    def extract_links(self, soup: BeautifulSoup, selector: str = "a") -> List[Dict[str, str]]:
        """
        Extract links from page.
        
        Args:
            soup: BeautifulSoup object
            selector: CSS selector for links
            
        Returns:
            List of link dictionaries
        """
        links = []
        
        for link in soup.select(selector):
            href = link.get("href")
            if href:
                links.append({
                    "url": self.make_absolute_url(href),
                    "text": self.extract_text(link),
                    "title": link.get("title", ""),
                })
        
        return links
    
    def find_video_urls(self, soup: BeautifulSoup) -> List[str]:
        """
        Find video URLs in page content.
        
        Args:
            soup: BeautifulSoup object
            
        Returns:
            List of video URLs
        """
        video_urls = []
        
        # Check for video tags
        for video in soup.find_all("video"):
            src = video.get("src")
            if src:
                video_urls.append(self.make_absolute_url(src))
            
            # Check for source tags within video
            for source in video.find_all("source"):
                src = source.get("src")
                if src:
                    video_urls.append(self.make_absolute_url(src))
        
        # Check for iframe embeds
        for iframe in soup.find_all("iframe"):
            src = iframe.get("src")
            if src and any(domain in src for domain in [
                "youtube.com", "youtu.be", "vimeo.com", "house.gov", "senate.gov"
            ]):
                video_urls.append(src)
        
        # Check for object/embed tags
        for obj in soup.find_all(["object", "embed"]):
            src = obj.get("src") or obj.get("data")
            if src:
                video_urls.append(self.make_absolute_url(src))
        
        return list(set(video_urls))  # Remove duplicates
    
    def extract_committee_info(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """
        Extract committee information from page.
        Override in subclasses for site-specific extraction.
        
        Args:
            soup: BeautifulSoup object
            
        Returns:
            Committee information dictionary
        """
        return {}
    
    def extract_hearing_info(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """
        Extract hearing information from page.
        Override in subclasses for site-specific extraction.
        
        Args:
            soup: BeautifulSoup object
            
        Returns:
            Hearing information dictionary
        """
        return {}
    
    async def scrape_robots_txt(self) -> Dict[str, List[str]]:
        """
        Scrape and parse robots.txt file.
        
        Returns:
            Dictionary of robots.txt rules
        """
        try:
            robots_url = urljoin(self.base_url, "/robots.txt")
            response = await self._make_request(robots_url)
            
            rules = {"allowed": [], "disallowed": []}
            
            for line in response.text.split("\n"):
                line = line.strip()
                if line.startswith("Disallow:"):
                    path = line.split(":", 1)[1].strip()
                    if path:
                        rules["disallowed"].append(path)
                elif line.startswith("Allow:"):
                    path = line.split(":", 1)[1].strip()
                    if path:
                        rules["allowed"].append(path)
            
            return rules
            
        except Exception as e:
            logger.warning("Could not fetch robots.txt", url=robots_url, error=str(e))
            return {"allowed": [], "disallowed": []}
    
    def is_allowed_by_robots(self, url: str, robots_rules: Dict[str, List[str]]) -> bool:
        """
        Check if URL is allowed by robots.txt rules.
        
        Args:
            url: URL to check
            robots_rules: Robots.txt rules
            
        Returns:
            True if allowed, False otherwise
        """
        path = urlparse(url).path
        
        # Check disallowed paths
        for disallowed in robots_rules.get("disallowed", []):
            if path.startswith(disallowed):
                return False
        
        return True