#!/usr/bin/env python3
"""
Senate Committee Scraper - Phase 1 Implementation
Scrapes Senate committee memberships from senate.gov and matches to existing database records
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime
import time
from typing import List, Dict, Optional, Tuple

# Production API URL for member matching
API_BASE_URL = "https://congressional-data-api-v3-1066017671167.us-central1.run.app/api/v1"

class SenateCommitteeScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.all_senators = []
        self.committees_scraped = []
        self.member_committee_relationships = []
        
    def load_existing_senators(self) -> bool:
        """Load all senators from production API"""
        print("📥 Loading existing senators from production API...")
        
        try:
            response = self.session.get(f"{API_BASE_URL}/members?chamber=Senate&limit=200")
            if response.status_code == 200:
                senators_data = response.json()
                self.all_senators = senators_data if isinstance(senators_data, list) else senators_data.get('members', [])
                print(f"✅ Loaded {len(self.all_senators)} senators from database")
                
                # Show sample senators for verification
                print("📋 Sample senators loaded:")
                for senator in self.all_senators[:5]:
                    print(f"  - {senator.get('first_name')} {senator.get('last_name')} ({senator.get('state')})")
                
                return True
            else:
                print(f"❌ Failed to load senators: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error loading senators: {e}")
            return False
    
    def load_existing_committees(self) -> Dict[str, Dict]:
        """Load all committees from production API"""
        print("📥 Loading existing committees from production API...")
        
        try:
            response = self.session.get(f"{API_BASE_URL}/committees?chamber=Senate&limit=200")
            if response.status_code == 200:
                committees_data = response.json()
                committees_list = committees_data if isinstance(committees_data, list) else committees_data.get('committees', [])
                
                # Create mapping by committee name for easy lookup
                committees_map = {}
                for committee in committees_list:
                    name = committee.get('name', '').lower()
                    committees_map[name] = committee
                
                print(f"✅ Loaded {len(committees_list)} committees from database")
                return committees_map
                
            else:
                print(f"❌ Failed to load committees: HTTP {response.status_code}")
                return {}
                
        except Exception as e:
            print(f"❌ Error loading committees: {e}")
            return {}
    
    def match_senator_by_name(self, full_name: str, state: str = None) -> Optional[Dict]:
        """Match scraped senator name to existing database record"""
        if not full_name or not self.all_senators:
            return None
            
        # Clean the name
        full_name = full_name.strip()
        
        # Try exact match first
        for senator in self.all_senators:
            senator_full_name = f"{senator.get('first_name', '')} {senator.get('last_name', '')}".strip()
            if full_name.lower() == senator_full_name.lower():
                if not state or senator.get('state', '').upper() == state.upper():
                    return senator
        
        # Try last name match with state
        if state:
            last_name = full_name.split()[-1].lower()
            for senator in self.all_senators:
                if (senator.get('last_name', '').lower() == last_name and 
                    senator.get('state', '').upper() == state.upper()):
                    return senator
        
        # Try partial matches
        name_parts = full_name.lower().split()
        for senator in self.all_senators:
            senator_first = senator.get('first_name', '').lower()
            senator_last = senator.get('last_name', '').lower()
            
            if (len(name_parts) >= 2 and 
                senator_first in name_parts and 
                senator_last in name_parts):
                if not state or senator.get('state', '').upper() == state.upper():
                    return senator
        
        return None
    
    def scrape_judiciary_committee(self) -> List[Dict]:
        """Test scraping with Senate Judiciary Committee"""
        print("🔍 Testing with Senate Judiciary Committee...")
        
        url = "https://www.senate.gov/committees/judiciary.htm"
        
        try:
            response = self.session.get(url)
            if response.status_code != 200:
                print(f"❌ Failed to fetch Judiciary Committee page: {response.status_code}")
                return []
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for committee member lists
            members = []
            
            # Multiple strategies to find member names
            strategies = [
                # Strategy 1: Look for specific member list containers
                lambda: soup.find_all('div', class_='member-listing'),
                # Strategy 2: Look for list items with senator names
                lambda: soup.find_all('li', string=re.compile(r'Sen\.|Senator')),
                # Strategy 3: Look for paragraph tags with senator names  
                lambda: soup.find_all('p', string=re.compile(r'Sen\.|Senator')),
                # Strategy 4: Look for all text containing "Sen."
                lambda: soup.find_all(string=re.compile(r'Sen\.|Senator')),
            ]
            
            for i, strategy in enumerate(strategies, 1):
                print(f"  Trying strategy {i}...")
                try:
                    elements = strategy()
                    if elements:
                        print(f"    Found {len(elements)} elements")
                        for element in elements[:5]:  # Show first 5
                            text = element.get_text() if hasattr(element, 'get_text') else str(element)
                            print(f"    Sample: {text[:100]}...")
                        break
                except Exception as e:
                    print(f"    Strategy {i} failed: {e}")
                    continue
            
            # For now, let's extract all text and look for patterns
            page_text = soup.get_text()
            
            # Find lines with "Sen." or "Senator"
            lines = page_text.split('\n')
            senator_lines = [line.strip() for line in lines if 'Sen.' in line or 'Senator' in line]
            
            print(f"📋 Found {len(senator_lines)} lines with 'Sen.' or 'Senator':")
            for line in senator_lines[:10]:  # Show first 10
                print(f"  - {line}")
            
            # Extract senator names using regex
            senator_pattern = r'(?:Sen\.|Senator)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)'
            
            for line in senator_lines:
                matches = re.findall(senator_pattern, line)
                for match in matches:
                    members.append({
                        'name': match.strip(),
                        'raw_text': line.strip(),
                        'committee': 'Judiciary'
                    })
            
            print(f"✅ Extracted {len(members)} potential senator names")
            
            return members
            
        except Exception as e:
            print(f"❌ Error scraping Judiciary Committee: {e}")
            return []
    
    def test_member_matching(self, scraped_members: List[Dict]) -> List[Dict]:
        """Test matching scraped members to database records"""
        print("🔗 Testing member matching...")
        
        matched_relationships = []
        
        for scraped_member in scraped_members:
            name = scraped_member['name']
            matched_senator = self.match_senator_by_name(name)
            
            if matched_senator:
                print(f"✅ Matched: {name} → {matched_senator.get('first_name')} {matched_senator.get('last_name')} ({matched_senator.get('state')})")
                matched_relationships.append({
                    'member_id': matched_senator.get('id'),
                    'member_name': f"{matched_senator.get('first_name')} {matched_senator.get('last_name')}",
                    'committee_name': scraped_member['committee'],
                    'scraped_name': name,
                    'raw_text': scraped_member['raw_text']
                })
            else:
                print(f"❌ No match found for: {name}")
        
        print(f"📊 Matching Results: {len(matched_relationships)}/{len(scraped_members)} successful matches")
        
        return matched_relationships
    
    def run_test_scraping(self) -> Dict:
        """Run complete test of scraping process"""
        print("🚀 Starting Senate Committee Scraping Test")
        print("=" * 50)
        
        # Step 1: Load existing data
        if not self.load_existing_senators():
            return {'error': 'Failed to load senators'}
        
        committees_map = self.load_existing_committees()
        if not committees_map:
            return {'error': 'Failed to load committees'}
        
        # Step 2: Test scraping with Judiciary Committee
        scraped_members = self.scrape_judiciary_committee()
        if not scraped_members:
            return {'error': 'Failed to scrape committee members'}
        
        # Step 3: Test member matching
        matched_relationships = self.test_member_matching(scraped_members)
        
        # Step 4: Generate report
        report = {
            'timestamp': datetime.now().isoformat(),
            'senators_loaded': len(self.all_senators),
            'committees_loaded': len(committees_map),
            'scraped_members': len(scraped_members),
            'matched_relationships': len(matched_relationships),
            'success_rate': len(matched_relationships) / len(scraped_members) * 100 if scraped_members else 0,
            'scraped_data': scraped_members,
            'matched_data': matched_relationships
        }
        
        print(f"\n📊 TEST RESULTS SUMMARY")
        print(f"Senators loaded: {report['senators_loaded']}")
        print(f"Committees loaded: {report['committees_loaded']}")
        print(f"Members scraped: {report['scraped_members']}")
        print(f"Successful matches: {report['matched_relationships']}")
        print(f"Success rate: {report['success_rate']:.1f}%")
        
        return report

def main():
    """Run Senate committee scraping test"""
    scraper = SenateCommitteeScraper()
    
    # Run test
    results = scraper.run_test_scraping()
    
    # Save results
    results_file = f"senate_scraping_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Results saved to: {results_file}")
    
    if 'error' not in results:
        print("\n🎯 NEXT STEPS:")
        print("1. Review scraped data accuracy")
        print("2. Improve scraping patterns if needed")
        print("3. Scale to all Senate committees")
        print("4. Implement database updates")
    else:
        print(f"\n❌ Error: {results['error']}")

if __name__ == "__main__":
    main()