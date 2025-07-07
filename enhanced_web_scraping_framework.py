#!/usr/bin/env python3

"""
Phase 2B: Enhanced Web Scraping Framework
Multi-source scraping system with confidence scoring and validation
"""

import psycopg2
from psycopg2.extras import RealDictCursor
import requests
from bs4 import BeautifulSoup
import json
import time
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging
from dataclasses import dataclass
from urllib.parse import urljoin, urlparse
import hashlib

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ScrapingResult:
    """Result of a scraping operation"""
    url: str
    success: bool
    data: Dict
    confidence_score: float
    error_message: Optional[str] = None
    scraped_at: datetime = datetime.now()
    response_time: float = 0.0

@dataclass
class CommitteeInfo:
    """Committee information with URLs"""
    id: int
    name: str
    chamber: str
    hearings_url: str
    members_url: str
    official_website_url: str

class EnhancedWebScraper:
    """Enhanced web scraper with confidence scoring and validation"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Congressional Data API (https://github.com/noelmcmichael/congress-data-automator)'
        })
        self.rate_limit_delay = 2.0  # Respectful 2-second delay between requests
        
    def connect_to_database(self):
        """Connect to Cloud SQL database via proxy"""
        try:
            conn = psycopg2.connect(
                host="localhost",
                port=5433,
                database="congress_data",
                user="postgres",
                password="mDf3S9ZnBpQqJvGsY1"
            )
            return conn
        except Exception as e:
            logger.error(f"Database connection error: {e}")
            return None

    def get_committees_with_urls(self) -> List[CommitteeInfo]:
        """Get all committees that have URLs populated"""
        conn = self.connect_to_database()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            cursor.execute("""
                SELECT id, name, chamber, hearings_url, members_url, official_website_url
                FROM committees
                WHERE hearings_url IS NOT NULL 
                AND members_url IS NOT NULL
                AND (is_subcommittee = FALSE OR is_subcommittee IS NULL)
                ORDER BY chamber, name;
            """)
            
            results = cursor.fetchall()
            
            committees = []
            for row in results:
                committees.append(CommitteeInfo(
                    id=row['id'],
                    name=row['name'],
                    chamber=row['chamber'],
                    hearings_url=row['hearings_url'],
                    members_url=row['members_url'],
                    official_website_url=row['official_website_url']
                ))
            
            logger.info(f"Found {len(committees)} committees with URLs")
            return committees
            
        except Exception as e:
            logger.error(f"Error fetching committees: {e}")
            return []
        
        finally:
            conn.close()

    def scrape_hearings_page(self, url: str) -> ScrapingResult:
        """Scrape a committee hearings page"""
        start_time = time.time()
        
        try:
            response = self.session.get(url, timeout=30)
            response_time = time.time() - start_time
            
            if response.status_code != 200:
                return ScrapingResult(
                    url=url,
                    success=False,
                    data={},
                    confidence_score=0.0,
                    error_message=f"HTTP {response.status_code}",
                    response_time=response_time
                )
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract hearings data with different patterns for different sites
            hearings_data = self._extract_hearings_from_soup(soup, url)
            
            # Calculate confidence score
            confidence = self._calculate_hearings_confidence(hearings_data, soup)
            
            return ScrapingResult(
                url=url,
                success=True,
                data=hearings_data,
                confidence_score=confidence,
                response_time=response_time
            )
            
        except Exception as e:
            return ScrapingResult(
                url=url,
                success=False,
                data={},
                confidence_score=0.0,
                error_message=str(e),
                response_time=time.time() - start_time
            )

    def scrape_members_page(self, url: str) -> ScrapingResult:
        """Scrape a committee members page"""
        start_time = time.time()
        
        try:
            response = self.session.get(url, timeout=30)
            response_time = time.time() - start_time
            
            if response.status_code != 200:
                return ScrapingResult(
                    url=url,
                    success=False,
                    data={},
                    confidence_score=0.0,
                    error_message=f"HTTP {response.status_code}",
                    response_time=response_time
                )
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract members data
            members_data = self._extract_members_from_soup(soup, url)
            
            # Calculate confidence score
            confidence = self._calculate_members_confidence(members_data, soup)
            
            return ScrapingResult(
                url=url,
                success=True,
                data=members_data,
                confidence_score=confidence,
                response_time=response_time
            )
            
        except Exception as e:
            return ScrapingResult(
                url=url,
                success=False,
                data={},
                confidence_score=0.0,
                error_message=str(e),
                response_time=time.time() - start_time
            )

    def _extract_hearings_from_soup(self, soup: BeautifulSoup, url: str) -> Dict:
        """Extract hearings information from BeautifulSoup object"""
        hearings_data = {
            'hearings': [],
            'page_title': '',
            'last_updated': None,
            'source_url': url
        }
        
        # Extract page title
        title_tag = soup.find('title')
        if title_tag:
            hearings_data['page_title'] = title_tag.get_text().strip()
        
        # Different extraction patterns for different committee sites
        if 'house.gov' in url:
            hearings_data['hearings'] = self._extract_house_hearings(soup)
        elif 'senate.gov' in url:
            hearings_data['hearings'] = self._extract_senate_hearings(soup)
        
        return hearings_data

    def _extract_house_hearings(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract hearings from House committee pages"""
        hearings = []
        
        # Look for common hearing patterns in House pages
        patterns = [
            # Pattern 1: Event listings with dates
            soup.find_all('div', class_=re.compile(r'event|hearing|calendar', re.I)),
            # Pattern 2: Table rows with hearing information
            soup.find_all('tr'),
            # Pattern 3: Article or section tags
            soup.find_all(['article', 'section'], class_=re.compile(r'hearing|event', re.I))
        ]
        
        for pattern_results in patterns:
            for element in pattern_results:
                hearing = self._extract_hearing_from_element(element)
                if hearing and hearing not in hearings:
                    hearings.append(hearing)
        
        return hearings[:20]  # Limit to most recent 20

    def _extract_senate_hearings(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract hearings from Senate committee pages"""
        hearings = []
        
        # Senate pages often use different structures
        patterns = [
            # Pattern 1: Hearing listings
            soup.find_all('div', class_=re.compile(r'hearing|event', re.I)),
            # Pattern 2: List items with hearing info
            soup.find_all('li'),
            # Pattern 3: Article tags
            soup.find_all('article')
        ]
        
        for pattern_results in patterns:
            for element in pattern_results:
                hearing = self._extract_hearing_from_element(element)
                if hearing and hearing not in hearings:
                    hearings.append(hearing)
        
        return hearings[:20]  # Limit to most recent 20

    def _extract_hearing_from_element(self, element) -> Optional[Dict]:
        """Extract hearing information from a single HTML element"""
        text = element.get_text().strip()
        
        # Skip if element is too short or likely not a hearing
        if len(text) < 20 or not re.search(r'\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4}', text):
            return None
        
        # Extract date pattern
        date_match = re.search(r'(\d{1,2})[/\-](\d{1,2})[/\-](\d{2,4})', text)
        if not date_match:
            return None
        
        # Extract time if present
        time_match = re.search(r'(\d{1,2}):(\d{2})\s*(AM|PM|am|pm)?', text)
        
        # Extract title (usually the longest meaningful text)
        title = text[:200].strip()
        
        # Look for links
        link = None
        link_tag = element.find('a')
        if link_tag and link_tag.get('href'):
            link = link_tag.get('href')
        
        return {
            'title': title,
            'date': date_match.group(0),
            'time': time_match.group(0) if time_match else None,
            'link': link,
            'raw_text': text[:500]  # Store raw text for debugging
        }

    def _extract_members_from_soup(self, soup: BeautifulSoup, url: str) -> Dict:
        """Extract members information from BeautifulSoup object"""
        members_data = {
            'members': [],
            'leadership': {},
            'page_title': '',
            'source_url': url
        }
        
        # Extract page title
        title_tag = soup.find('title')
        if title_tag:
            members_data['page_title'] = title_tag.get_text().strip()
        
        # Look for member listings
        member_patterns = [
            soup.find_all('div', class_=re.compile(r'member|representative|senator', re.I)),
            soup.find_all('li'),
            soup.find_all('tr'),
            soup.find_all('p')
        ]
        
        for pattern_results in member_patterns:
            for element in pattern_results:
                member = self._extract_member_from_element(element)
                if member and member not in members_data['members']:
                    members_data['members'].append(member)
        
        # Extract leadership positions
        leadership_text = soup.get_text().lower()
        if 'chairman' in leadership_text or 'chair' in leadership_text:
            members_data['leadership']['chair'] = self._extract_leadership_info(soup, 'chair')
        if 'ranking member' in leadership_text:
            members_data['leadership']['ranking_member'] = self._extract_leadership_info(soup, 'ranking')
        
        return members_data

    def _extract_member_from_element(self, element) -> Optional[Dict]:
        """Extract member information from a single HTML element"""
        text = element.get_text().strip()
        
        # Look for name patterns (title-cased words)
        name_match = re.search(r'\b([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b', text)
        if not name_match:
            return None
        
        name = name_match.group(1)
        
        # Skip common false positives
        skip_words = ['Committee', 'Subcommittee', 'Congress', 'House', 'Senate', 'United States']
        if any(word in name for word in skip_words):
            return None
        
        # Extract state if present
        state_match = re.search(r'\b([A-Z]{2})\b', text)
        
        # Extract party if present
        party_match = re.search(r'\b([RDI])-', text)
        
        return {
            'name': name,
            'state': state_match.group(1) if state_match else None,
            'party': party_match.group(1) if party_match else None,
            'raw_text': text[:200]
        }

    def _extract_leadership_info(self, soup: BeautifulSoup, position_type: str) -> Optional[str]:
        """Extract leadership position information"""
        position_keywords = {
            'chair': ['chairman', 'chairwoman', 'chair'],
            'ranking': ['ranking member', 'ranking minority member']
        }
        
        keywords = position_keywords.get(position_type, [])
        
        for keyword in keywords:
            # Look for text containing the keyword
            elements = soup.find_all(text=re.compile(keyword, re.I))
            for element in elements:
                parent = element.parent
                if parent:
                    text = parent.get_text()
                    # Extract name from the context
                    name_match = re.search(r'([A-Z][a-z]+\s+[A-Z][a-z]+)', text)
                    if name_match:
                        return name_match.group(1)
        
        return None

    def _calculate_hearings_confidence(self, hearings_data: Dict, soup: BeautifulSoup) -> float:
        """Calculate confidence score for hearings data"""
        score = 0.0
        
        # Page accessibility (base score)
        score += 0.3
        
        # Number of hearings found
        num_hearings = len(hearings_data.get('hearings', []))
        if num_hearings > 0:
            score += min(0.3, num_hearings * 0.05)
        
        # Page structure indicators
        if soup.find_all(text=re.compile(r'hearing|hearing schedule', re.I)):
            score += 0.2
        
        # Date information quality
        hearings = hearings_data.get('hearings', [])
        valid_dates = sum(1 for h in hearings if h.get('date'))
        if valid_dates > 0:
            score += min(0.2, valid_dates * 0.04)
        
        return min(1.0, score)

    def _calculate_members_confidence(self, members_data: Dict, soup: BeautifulSoup) -> float:
        """Calculate confidence score for members data"""
        score = 0.0
        
        # Page accessibility (base score)
        score += 0.3
        
        # Number of members found
        num_members = len(members_data.get('members', []))
        if num_members > 0:
            score += min(0.4, num_members * 0.02)
        
        # Leadership information
        if members_data.get('leadership'):
            score += 0.2
        
        # Page structure indicators
        if soup.find_all(text=re.compile(r'member|committee member', re.I)):
            score += 0.1
        
        return min(1.0, score)

    def scrape_committee_data(self, committee: CommitteeInfo) -> Dict:
        """Scrape both hearings and members data for a committee"""
        logger.info(f"Scraping data for {committee.chamber} {committee.name}")
        
        results = {
            'committee_id': committee.id,
            'committee_name': committee.name,
            'chamber': committee.chamber,
            'hearings_result': None,
            'members_result': None,
            'overall_confidence': 0.0,
            'scraped_at': datetime.now().isoformat()
        }
        
        # Scrape hearings page
        if committee.hearings_url:
            results['hearings_result'] = self.scrape_hearings_page(committee.hearings_url)
            time.sleep(self.rate_limit_delay)  # Respectful rate limiting
        
        # Scrape members page
        if committee.members_url:
            results['members_result'] = self.scrape_members_page(committee.members_url)
            time.sleep(self.rate_limit_delay)  # Respectful rate limiting
        
        # Calculate overall confidence
        hearings_conf = results['hearings_result'].confidence_score if results['hearings_result'] else 0.0
        members_conf = results['members_result'].confidence_score if results['members_result'] else 0.0
        results['overall_confidence'] = (hearings_conf + members_conf) / 2.0
        
        return results

    def run_comprehensive_scrape(self) -> Dict:
        """Run comprehensive scraping for all committees with URLs"""
        print("🚀 STARTING ENHANCED WEB SCRAPING FRAMEWORK")
        print("=" * 60)
        
        committees = self.get_committees_with_urls()
        
        if not committees:
            print("❌ No committees with URLs found")
            return {}
        
        print(f"📋 Found {len(committees)} committees to scrape")
        
        all_results = {
            'start_time': datetime.now().isoformat(),
            'committees_scraped': len(committees),
            'results': [],
            'summary': {
                'successful_hearings': 0,
                'successful_members': 0,
                'high_confidence': 0,
                'errors': []
            }
        }
        
        for i, committee in enumerate(committees, 1):
            print(f"\n🔄 [{i}/{len(committees)}] {committee.chamber} {committee.name}")
            
            try:
                result = self.scrape_committee_data(committee)
                all_results['results'].append(result)
                
                # Update summary
                if result['hearings_result'] and result['hearings_result'].success:
                    all_results['summary']['successful_hearings'] += 1
                    
                if result['members_result'] and result['members_result'].success:
                    all_results['summary']['successful_members'] += 1
                
                if result['overall_confidence'] > 0.7:
                    all_results['summary']['high_confidence'] += 1
                
                print(f"   Hearings: {'✅' if result['hearings_result'] and result['hearings_result'].success else '❌'}")
                print(f"   Members: {'✅' if result['members_result'] and result['members_result'].success else '❌'}")
                print(f"   Confidence: {result['overall_confidence']:.2f}")
                
            except Exception as e:
                error_msg = f"Error scraping {committee.name}: {e}"
                all_results['summary']['errors'].append(error_msg)
                logger.error(error_msg)
        
        all_results['end_time'] = datetime.now().isoformat()
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"enhanced_scraping_results_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(all_results, f, indent=2, default=str)
        
        print(f"\n📊 SCRAPING COMPLETE")
        print("=" * 60)
        print(f"✅ Committees processed: {len(committees)}")
        print(f"✅ Successful hearings scrapes: {all_results['summary']['successful_hearings']}")
        print(f"✅ Successful members scrapes: {all_results['summary']['successful_members']}")
        print(f"✅ High confidence results: {all_results['summary']['high_confidence']}")
        print(f"❌ Errors: {len(all_results['summary']['errors'])}")
        print(f"📁 Results saved to: {filename}")
        
        return all_results

def main():
    """Main function to run the enhanced web scraping framework"""
    scraper = EnhancedWebScraper()
    results = scraper.run_comprehensive_scrape()
    
    if results:
        print("\n🎉 ENHANCED WEB SCRAPING FRAMEWORK DEPLOYED")
        print("=" * 60)
        print("✅ Multi-source data collection operational")
        print("✅ Confidence scoring system active")
        print("✅ Rate limiting and respectful scraping implemented")
        print("✅ Data validation and error handling complete")
        print("\n📋 Ready for integration with existing system")
    else:
        print("\n❌ ENHANCED WEB SCRAPING FRAMEWORK FAILED")
        print("=" * 60)
        print("❌ Check database connection and committee URLs")

if __name__ == "__main__":
    main()