"""
Web scraper for House.gov websites.
"""
import re
from typing import Dict, List, Optional, Any
from datetime import datetime
from bs4 import BeautifulSoup
import structlog
import sys
import os
sys.path.append(os.path.dirname(__file__))
from base_scraper import BaseScraper

logger = structlog.get_logger()


class HouseScraper(BaseScraper):
    """
    Scraper for House.gov websites.
    """
    
    def __init__(self):
        super().__init__("https://www.house.gov", "HouseScraper")
        
        # Common House.gov URL patterns
        self.committee_list_url = "https://www.house.gov/committees"
        self.hearing_calendar_url = "https://www.house.gov/legislative-activity/committee-hearings"
    
    async def scrape_committees(self) -> List[Dict[str, Any]]:
        """
        Scrape House committees from the committees page.
        
        Returns:
            List of committee information dictionaries
        """
        try:
            soup = await self.fetch_page(self.committee_list_url)
            committees = []
            
            # Find committee links
            committee_links = soup.select("a[href*='/committees/']")
            
            for link in committee_links:
                committee_url = self.make_absolute_url(link.get("href"))
                committee_name = self.extract_text(link)
                
                if committee_name and committee_url:
                    committee_info = {
                        "name": committee_name,
                        "url": committee_url,
                        "chamber": "House",
                        "source": "house.gov",
                    }
                    
                    # Try to get detailed information
                    try:
                        committee_details = await self.scrape_committee_details(committee_url)
                        committee_info.update(committee_details)
                    except Exception as e:
                        logger.warning(
                            "Could not scrape committee details",
                            committee=committee_name,
                            url=committee_url,
                            error=str(e)
                        )
                    
                    committees.append(committee_info)
            
            logger.info(f"Scraped {len(committees)} House committees")
            return committees
            
        except Exception as e:
            logger.error("Error scraping House committees", error=str(e))
            return []
    
    async def scrape_committee_details(self, committee_url: str) -> Dict[str, Any]:
        """
        Scrape detailed information for a specific committee.
        
        Args:
            committee_url: URL of the committee page
            
        Returns:
            Committee details dictionary
        """
        soup = await self.fetch_page(committee_url)
        details = {}
        
        # Extract committee information
        details.update(self.extract_committee_info(soup))
        
        # Look for subcommittees
        subcommittees = []
        subcommittee_links = soup.select("a[href*='subcommittee']")
        
        for link in subcommittee_links:
            subcommittee_url = self.make_absolute_url(link.get("href"))
            subcommittee_name = self.extract_text(link)
            
            if subcommittee_name and subcommittee_url:
                subcommittees.append({
                    "name": subcommittee_name,
                    "url": subcommittee_url,
                    "is_subcommittee": True,
                })
        
        details["subcommittees"] = subcommittees
        
        # Extract contact information
        details.update(self.extract_contact_info(soup))
        
        # Look for hearing information
        details["hearings_url"] = self.find_hearings_url(soup)
        
        return details
    
    def extract_committee_info(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """
        Extract committee information from committee page.
        
        Args:
            soup: BeautifulSoup object
            
        Returns:
            Committee information dictionary
        """
        info = {}
        
        # Try to find committee description
        description_selectors = [
            ".committee-description",
            ".committee-about",
            ".description",
            "p:contains('committee')",
        ]
        
        for selector in description_selectors:
            description_elem = soup.select_one(selector)
            if description_elem:
                info["description"] = self.extract_text(description_elem)
                break
        
        # Try to find jurisdiction information
        jurisdiction_selectors = [
            ".jurisdiction",
            ".committee-jurisdiction",
            "*:contains('jurisdiction')",
        ]
        
        for selector in jurisdiction_selectors:
            jurisdiction_elem = soup.select_one(selector)
            if jurisdiction_elem:
                info["jurisdiction"] = self.extract_text(jurisdiction_elem)
                break
        
        # Try to find leadership information
        leadership = self.extract_leadership(soup)
        if leadership:
            info.update(leadership)
        
        return info
    
    def extract_leadership(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """
        Extract committee leadership information.
        
        Args:
            soup: BeautifulSoup object
            
        Returns:
            Leadership information dictionary
        """
        leadership = {}
        
        # Look for chair information
        chair_selectors = [
            ".chair",
            ".committee-chair",
            "*:contains('Chair')",
            "*:contains('Chairman')",
        ]
        
        for selector in chair_selectors:
            chair_elem = soup.select_one(selector)
            if chair_elem:
                chair_text = self.extract_text(chair_elem)
                leadership["chair_info"] = chair_text
                break
        
        # Look for ranking member information
        ranking_selectors = [
            ".ranking-member",
            ".committee-ranking-member",
            "*:contains('Ranking Member')",
        ]
        
        for selector in ranking_selectors:
            ranking_elem = soup.select_one(selector)
            if ranking_elem:
                ranking_text = self.extract_text(ranking_elem)
                leadership["ranking_member_info"] = ranking_text
                break
        
        return leadership
    
    def extract_contact_info(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """
        Extract contact information from page.
        
        Args:
            soup: BeautifulSoup object
            
        Returns:
            Contact information dictionary
        """
        contact = {}
        
        # Look for phone numbers
        phone_pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        phone_matches = re.findall(phone_pattern, soup.get_text())
        if phone_matches:
            contact["phone"] = phone_matches[0]
        
        # Look for email addresses
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_matches = re.findall(email_pattern, soup.get_text())
        if email_matches:
            contact["email"] = email_matches[0]
        
        # Look for office location
        office_selectors = [
            ".office",
            ".location",
            "*:contains('Room')",
            "*:contains('Office')",
        ]
        
        for selector in office_selectors:
            office_elem = soup.select_one(selector)
            if office_elem:
                office_text = self.extract_text(office_elem)
                if "room" in office_text.lower() or "office" in office_text.lower():
                    contact["office_location"] = office_text
                    break
        
        return contact
    
    def find_hearings_url(self, soup: BeautifulSoup) -> Optional[str]:
        """
        Find URL for committee hearings page.
        
        Args:
            soup: BeautifulSoup object
            
        Returns:
            Hearings URL or None
        """
        hearing_selectors = [
            "a[href*='hearing']",
            "a[href*='schedule']",
            "a[href*='calendar']",
        ]
        
        for selector in hearing_selectors:
            hearing_link = soup.select_one(selector)
            if hearing_link:
                return self.make_absolute_url(hearing_link.get("href"))
        
        return None
    
    async def scrape_hearings(self, committee_url: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Scrape hearing information from House calendar or committee page.
        
        Args:
            committee_url: Specific committee URL to scrape hearings from
            
        Returns:
            List of hearing information dictionaries
        """
        hearings = []
        
        # If no specific committee URL provided, scrape general calendar
        if not committee_url:
            committee_url = self.hearing_calendar_url
        
        try:
            soup = await self.fetch_page(committee_url)
            
            # Look for hearing entries
            hearing_selectors = [
                ".hearing",
                ".event",
                ".committee-hearing",
                "*[class*='hearing']",
            ]
            
            for selector in hearing_selectors:
                hearing_elements = soup.select(selector)
                
                for element in hearing_elements:
                    hearing_info = self.extract_hearing_info(element)
                    if hearing_info:
                        # Find video URLs
                        video_urls = self.find_video_urls(element)
                        if video_urls:
                            hearing_info["video_urls"] = video_urls
                        
                        hearings.append(hearing_info)
            
            logger.info(f"Scraped {len(hearings)} House hearings")
            return hearings
            
        except Exception as e:
            logger.error("Error scraping House hearings", error=str(e))
            return []
    
    def extract_hearing_info(self, element) -> Dict[str, Any]:
        """
        Extract hearing information from a hearing element.
        
        Args:
            element: BeautifulSoup element containing hearing information
            
        Returns:
            Hearing information dictionary
        """
        info = {}
        
        # Extract title
        title_selectors = [
            ".title",
            ".hearing-title",
            "h1", "h2", "h3",
        ]
        
        for selector in title_selectors:
            title_elem = element.select_one(selector)
            if title_elem:
                info["title"] = self.extract_text(title_elem)
                break
        
        # Extract date and time
        date_selectors = [
            ".date",
            ".hearing-date",
            "*[class*='date']",
        ]
        
        for selector in date_selectors:
            date_elem = element.select_one(selector)
            if date_elem:
                date_text = self.extract_text(date_elem)
                info["date_text"] = date_text
                # Try to parse date
                try:
                    parsed_date = self.parse_date(date_text)
                    if parsed_date:
                        info["scheduled_date"] = parsed_date.isoformat()
                except:
                    pass
                break
        
        # Extract location
        location_selectors = [
            ".location",
            ".hearing-location",
            ".room",
        ]
        
        for selector in location_selectors:
            location_elem = element.select_one(selector)
            if location_elem:
                info["location"] = self.extract_text(location_elem)
                break
        
        # Extract description
        description_selectors = [
            ".description",
            ".hearing-description",
            "p",
        ]
        
        for selector in description_selectors:
            desc_elem = element.select_one(selector)
            if desc_elem:
                desc_text = self.extract_text(desc_elem)
                if len(desc_text) > 20:  # Only use substantial descriptions
                    info["description"] = desc_text
                    break
        
        # Add metadata
        info["chamber"] = "House"
        info["source"] = "house.gov"
        
        return info
    
    def parse_date(self, date_text: str) -> Optional[datetime]:
        """
        Parse date string into datetime object.
        
        Args:
            date_text: Date string to parse
            
        Returns:
            Parsed datetime or None
        """
        # Common date formats found on House.gov
        date_formats = [
            "%B %d, %Y",
            "%b %d, %Y",
            "%m/%d/%Y",
            "%Y-%m-%d",
            "%d %B %Y",
            "%d %b %Y",
        ]
        
        for fmt in date_formats:
            try:
                return datetime.strptime(date_text.strip(), fmt)
            except ValueError:
                continue
        
        return None