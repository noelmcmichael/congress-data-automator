"""
Web scraper for Senate.gov websites.
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


class SenateScraper(BaseScraper):
    """
    Scraper for Senate.gov websites.
    """
    
    def __init__(self):
        super().__init__("https://www.senate.gov", "SenateScraper")
        
        # Common Senate.gov URL patterns
        self.committee_list_url = "https://www.senate.gov/committees/committees_home.htm"
        self.hearing_calendar_url = "https://www.senate.gov/committees/hearings_meetings.htm"
    
    async def scrape_committees(self) -> List[Dict[str, Any]]:
        """
        Scrape Senate committees from the committees page.
        
        Returns:
            List of committee information dictionaries
        """
        try:
            soup = await self.fetch_page(self.committee_list_url)
            committees = []
            
            # Find committee links - Senate uses different structure
            committee_links = soup.select("a[href*='committee']")
            
            for link in committee_links:
                committee_url = self.make_absolute_url(link.get("href"))
                committee_name = self.extract_text(link)
                
                if committee_name and committee_url and len(committee_name) > 3:
                    committee_info = {
                        "name": committee_name,
                        "url": committee_url,
                        "chamber": "Senate",
                        "source": "senate.gov",
                    }
                    
                    # Try to get detailed information
                    try:
                        committee_details = await self.scrape_committee_details(committee_url)
                        committee_info.update(committee_details)
                    except Exception as e:
                        logger.warning(
                            "Could not scrape Senate committee details",
                            committee=committee_name,
                            url=committee_url,
                            error=str(e)
                        )
                    
                    committees.append(committee_info)
            
            logger.info(f"Scraped {len(committees)} Senate committees")
            return committees
            
        except Exception as e:
            logger.error("Error scraping Senate committees", error=str(e))
            return []
    
    async def scrape_committee_details(self, committee_url: str) -> Dict[str, Any]:
        """
        Scrape detailed information for a specific Senate committee.
        
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
        subcommittee_selectors = [
            "a[href*='subcommittee']",
            "*:contains('Subcommittee')",
        ]
        
        for selector in subcommittee_selectors:
            subcommittee_elements = soup.select(selector)
            
            for elem in subcommittee_elements:
                if elem.name == "a":
                    subcommittee_url = self.make_absolute_url(elem.get("href"))
                    subcommittee_name = self.extract_text(elem)
                else:
                    subcommittee_name = self.extract_text(elem)
                    subcommittee_url = None
                
                if subcommittee_name and "subcommittee" in subcommittee_name.lower():
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
            ".about",
            ".description",
            "p",
        ]
        
        for selector in description_selectors:
            description_elem = soup.select_one(selector)
            if description_elem:
                desc_text = self.extract_text(description_elem)
                if len(desc_text) > 50:  # Only use substantial descriptions
                    info["description"] = desc_text
                    break
        
        # Try to find jurisdiction information
        jurisdiction_text = soup.get_text()
        if "jurisdiction" in jurisdiction_text.lower():
            # Extract text around "jurisdiction"
            jurisdiction_match = re.search(
                r'jurisdiction[:\s]*(.*?)(?:\n|\.|\|)', 
                jurisdiction_text, 
                re.IGNORECASE | re.DOTALL
            )
            if jurisdiction_match:
                info["jurisdiction"] = jurisdiction_match.group(1).strip()
        
        # Try to find leadership information
        leadership = self.extract_leadership(soup)
        if leadership:
            info.update(leadership)
        
        return info
    
    def extract_leadership(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """
        Extract Senate committee leadership information.
        
        Args:
            soup: BeautifulSoup object
            
        Returns:
            Leadership information dictionary
        """
        leadership = {}
        
        # Look for chair information
        chair_patterns = [
            r'(?:chair|chairman|chairwoman)[:\s]*(.*?)(?:\n|,|\|)',
            r'(.*?)\s+\(chair\)',
        ]
        
        page_text = soup.get_text()
        for pattern in chair_patterns:
            match = re.search(pattern, page_text, re.IGNORECASE)
            if match:
                leadership["chair_info"] = match.group(1).strip()
                break
        
        # Look for ranking member information
        ranking_patterns = [
            r'ranking member[:\s]*(.*?)(?:\n|,|\|)',
            r'(.*?)\s+\(ranking member\)',
        ]
        
        for pattern in ranking_patterns:
            match = re.search(pattern, page_text, re.IGNORECASE)
            if match:
                leadership["ranking_member_info"] = match.group(1).strip()
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
        office_patterns = [
            r'(?:room|office|suite)\s+([A-Z]?\d+[A-Z]?)',
            r'(\d+\s+[A-Z][a-z]+\s+building)',
        ]
        
        page_text = soup.get_text()
        for pattern in office_patterns:
            match = re.search(pattern, page_text, re.IGNORECASE)
            if match:
                contact["office_location"] = match.group(1).strip()
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
            "a[href*='meeting']",
        ]
        
        for selector in hearing_selectors:
            hearing_link = soup.select_one(selector)
            if hearing_link:
                return self.make_absolute_url(hearing_link.get("href"))
        
        return None
    
    async def scrape_hearings(self, committee_url: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Scrape hearing information from Senate calendar or committee page.
        
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
            
            # Senate uses table structure for hearings
            hearing_tables = soup.select("table")
            
            for table in hearing_tables:
                rows = table.select("tr")
                
                for row in rows:
                    cells = row.select("td")
                    if len(cells) >= 2:  # At least date and description
                        hearing_info = self.extract_hearing_from_row(cells)
                        if hearing_info:
                            # Find video URLs
                            video_urls = self.find_video_urls(row)
                            if video_urls:
                                hearing_info["video_urls"] = video_urls
                            
                            hearings.append(hearing_info)
            
            # Also look for individual hearing entries
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
            
            logger.info(f"Scraped {len(hearings)} Senate hearings")
            return hearings
            
        except Exception as e:
            logger.error("Error scraping Senate hearings", error=str(e))
            return []
    
    def extract_hearing_from_row(self, cells: List) -> Dict[str, Any]:
        """
        Extract hearing information from table row cells.
        
        Args:
            cells: List of table cells
            
        Returns:
            Hearing information dictionary
        """
        info = {}
        
        if len(cells) >= 2:
            # First cell usually contains date
            date_text = self.extract_text(cells[0])
            if date_text:
                info["date_text"] = date_text
                # Try to parse date
                try:
                    parsed_date = self.parse_date(date_text)
                    if parsed_date:
                        info["scheduled_date"] = parsed_date.isoformat()
                except:
                    pass
            
            # Second cell usually contains title/description
            title_text = self.extract_text(cells[1])
            if title_text and len(title_text) > 10:
                info["title"] = title_text
            
            # Third cell might contain location
            if len(cells) >= 3:
                location_text = self.extract_text(cells[2])
                if location_text:
                    info["location"] = location_text
        
        # Add metadata
        info["chamber"] = "Senate"
        info["source"] = "senate.gov"
        
        return info if info.get("title") else {}
    
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
            "h1", "h2", "h3", "h4",
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
        info["chamber"] = "Senate"
        info["source"] = "senate.gov"
        
        return info
    
    def parse_date(self, date_text: str) -> Optional[datetime]:
        """
        Parse date string into datetime object.
        
        Args:
            date_text: Date string to parse
            
        Returns:
            Parsed datetime or None
        """
        # Common date formats found on Senate.gov
        date_formats = [
            "%B %d, %Y",
            "%b %d, %Y",
            "%m/%d/%Y",
            "%Y-%m-%d",
            "%d %B %Y",
            "%d %b %Y",
            "%A, %B %d, %Y",
            "%a, %b %d, %Y",
        ]
        
        for fmt in date_formats:
            try:
                return datetime.strptime(date_text.strip(), fmt)
            except ValueError:
                continue
        
        return None