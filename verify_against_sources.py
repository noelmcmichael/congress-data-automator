#!/usr/bin/env python3
"""
Congressional Data Verification System
Fetches authoritative data and compares against our database
"""

import requests
from bs4 import BeautifulSoup
import json
import psycopg2
import time
from datetime import datetime
import re
from typing import Dict, List, Optional, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CongressionalDataVerifier:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        
        # Database connection
        self.db_config = {
            'host': 'localhost',
            'port': 5433,
            'database': 'congress_data',
            'user': 'postgres',
            'password': 'mDf3S9ZnBpQqJvGsY1'
        }
        
        # Results storage
        self.verification_results = {
            'timestamp': datetime.now().isoformat(),
            'house_committees': {'authoritative': [], 'database': [], 'discrepancies': []},
            'senate_committees': {'authoritative': [], 'database': [], 'discrepancies': []},
            'member_assignments': {'errors': []},
            'leadership_errors': []
        }
    
    def fetch_house_committees(self) -> List[Dict]:
        """Fetch current House committees from house.gov"""
        try:
            logger.info("Fetching House committees from house.gov...")
            url = "https://www.house.gov/committees"
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            committees = []
            
            # Find committee listings (structure may vary)
            committee_links = soup.find_all('a', href=re.compile(r'/committees/'))
            
            for link in committee_links:
                committee_name = link.get_text(strip=True)
                if committee_name and 'Committee' in committee_name:
                    committees.append({
                        'name': committee_name,
                        'chamber': 'House',
                        'url': link.get('href', ''),
                        'type': 'Standing'
                    })
            
            logger.info(f"Found {len(committees)} House committees")
            return committees
            
        except Exception as e:
            logger.error(f"Error fetching House committees: {e}")
            return []
    
    def fetch_senate_committees(self) -> List[Dict]:
        """Fetch current Senate committees from senate.gov"""
        try:
            logger.info("Fetching Senate committees from senate.gov...")
            url = "https://www.senate.gov/committees/committee_membership.htm"
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            committees = []
            
            # Parse committee structure from Senate page
            committee_sections = soup.find_all('div', class_='committee-section')
            
            for section in committee_sections:
                committee_name = section.find('h3') or section.find('h2')
                if committee_name:
                    name = committee_name.get_text(strip=True)
                    committees.append({
                        'name': name,
                        'chamber': 'Senate',
                        'type': 'Standing',
                        'members': []
                    })
            
            logger.info(f"Found {len(committees)} Senate committees")
            return committees
            
        except Exception as e:
            logger.error(f"Error fetching Senate committees: {e}")
            return []
    
    def fetch_congress_gov_data(self) -> Dict:
        """Fetch data from congress.gov API"""
        try:
            logger.info("Fetching data from congress.gov...")
            # Note: congress.gov requires API key for full access
            # This is a simplified example - real implementation would use their API
            
            base_url = "https://api.congress.gov/v3"
            # Would need API key: headers = {'X-API-Key': 'your_key_here'}
            
            # For now, return placeholder structure
            return {
                'committees': [],
                'members': [],
                'note': 'Requires API key for full access'
            }
            
        except Exception as e:
            logger.error(f"Error fetching congress.gov data: {e}")
            return {}
    
    def fetch_database_committees(self) -> List[Dict]:
        """Fetch committees from our database"""
        try:
            with psycopg2.connect(**self.db_config) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT c.id, c.name, c.chamber, c.committee_type, 
                               c.parent_committee_id, pc.name as parent_name
                        FROM committees c
                        LEFT JOIN committees pc ON c.parent_committee_id = pc.id
                        WHERE c.is_current = true
                        ORDER BY c.chamber, c.name
                    """)
                    
                    committees = []
                    for row in cursor.fetchall():
                        committees.append({
                            'id': row[0],
                            'name': row[1],
                            'chamber': row[2],
                            'type': row[3],
                            'parent_id': row[4],
                            'parent_name': row[5]
                        })
                    
                    logger.info(f"Found {len(committees)} committees in database")
                    return committees
                    
        except Exception as e:
            logger.error(f"Error fetching database committees: {e}")
            return []
    
    def fetch_database_members(self) -> List[Dict]:
        """Fetch member assignments from our database"""
        try:
            with psycopg2.connect(**self.db_config) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT m.id, m.first_name, m.last_name, m.party, m.chamber, m.state,
                               c.name as committee_name, cm.position, cm.is_current
                        FROM members m
                        JOIN committee_memberships cm ON m.id = cm.member_id
                        JOIN committees c ON cm.committee_id = c.id
                        WHERE cm.is_current = true AND c.is_current = true
                        ORDER BY m.last_name, m.first_name, c.name
                    """)
                    
                    members = []
                    for row in cursor.fetchall():
                        members.append({
                            'id': row[0],
                            'name': f"{row[1]} {row[2]}",
                            'party': row[3],
                            'chamber': row[4],
                            'state': row[5],
                            'committee': row[6],
                            'position': row[7],
                            'is_current': row[8]
                        })
                    
                    logger.info(f"Found {len(members)} member assignments in database")
                    return members
                    
        except Exception as e:
            logger.error(f"Error fetching database members: {e}")
            return []
    
    def compare_committee_structures(self) -> Dict:
        """Compare our database committees against authoritative sources"""
        logger.info("Comparing committee structures...")
        
        # Fetch data from all sources
        house_committees = self.fetch_house_committees()
        senate_committees = self.fetch_senate_committees()
        db_committees = self.fetch_database_committees()
        
        # Store in results
        self.verification_results['house_committees']['authoritative'] = house_committees
        self.verification_results['senate_committees']['authoritative'] = senate_committees
        self.verification_results['house_committees']['database'] = [
            c for c in db_committees if c['chamber'] == 'House'
        ]
        self.verification_results['senate_committees']['database'] = [
            c for c in db_committees if c['chamber'] == 'Senate'
        ]
        
        # Find discrepancies
        discrepancies = []
        
        # Check House committees
        auth_house_names = {c['name'] for c in house_committees}
        db_house_names = {c['name'] for c in db_committees if c['chamber'] == 'House'}
        
        missing_from_db = auth_house_names - db_house_names
        extra_in_db = db_house_names - auth_house_names
        
        for name in missing_from_db:
            discrepancies.append({
                'type': 'missing_committee',
                'chamber': 'House',
                'committee': name,
                'issue': 'Committee exists in authoritative source but not in database'
            })
        
        for name in extra_in_db:
            discrepancies.append({
                'type': 'extra_committee',
                'chamber': 'House',
                'committee': name,
                'issue': 'Committee exists in database but not in authoritative source'
            })
        
        # Check Senate committees
        auth_senate_names = {c['name'] for c in senate_committees}
        db_senate_names = {c['name'] for c in db_committees if c['chamber'] == 'Senate'}
        
        missing_from_db = auth_senate_names - db_senate_names
        extra_in_db = db_senate_names - auth_senate_names
        
        for name in missing_from_db:
            discrepancies.append({
                'type': 'missing_committee',
                'chamber': 'Senate',
                'committee': name,
                'issue': 'Committee exists in authoritative source but not in database'
            })
        
        for name in extra_in_db:
            discrepancies.append({
                'type': 'extra_committee',
                'chamber': 'Senate',
                'committee': name,
                'issue': 'Committee exists in database but not in authoritative source'
            })
        
        self.verification_results['house_committees']['discrepancies'] = discrepancies
        
        logger.info(f"Found {len(discrepancies)} committee discrepancies")
        return discrepancies
    
    def verify_leadership_accuracy(self) -> List[Dict]:
        """Verify leadership positions against known structure"""
        logger.info("Verifying leadership accuracy...")
        
        try:
            with psycopg2.connect(**self.db_config) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT c.name, c.chamber, m.first_name, m.last_name, 
                               m.party, cm.position
                        FROM committees c
                        JOIN committee_memberships cm ON c.id = cm.committee_id
                        JOIN members m ON cm.member_id = m.id
                        WHERE cm.position IN ('Chair', 'Ranking Member')
                        AND c.is_current = true AND cm.is_current = true
                        ORDER BY c.name, cm.position
                    """)
                    
                    leadership_errors = []
                    for row in cursor.fetchall():
                        committee_name = row[0]
                        chamber = row[1]
                        member_name = f"{row[2]} {row[3]}"
                        party = row[4]
                        position = row[5]
                        
                        # Check if leadership positions match expected party control
                        # 119th Congress: Republicans control House, Democrats control Senate
                        expected_chair_party = 'Republican' if chamber == 'House' else 'Democratic'
                        expected_ranking_party = 'Democratic' if chamber == 'House' else 'Republican'
                        
                        if position == 'Chair' and party != expected_chair_party:
                            leadership_errors.append({
                                'committee': committee_name,
                                'chamber': chamber,
                                'member': member_name,
                                'position': position,
                                'party': party,
                                'expected_party': expected_chair_party,
                                'error': f"Chair should be {expected_chair_party}"
                            })
                        
                        elif position == 'Ranking Member' and party != expected_ranking_party:
                            leadership_errors.append({
                                'committee': committee_name,
                                'chamber': chamber,
                                'member': member_name,
                                'position': position,
                                'party': party,
                                'expected_party': expected_ranking_party,
                                'error': f"Ranking Member should be {expected_ranking_party}"
                            })
                    
                    self.verification_results['leadership_errors'] = leadership_errors
                    logger.info(f"Found {len(leadership_errors)} leadership errors")
                    return leadership_errors
                    
        except Exception as e:
            logger.error(f"Error verifying leadership: {e}")
            return []
    
    def generate_verification_report(self) -> str:
        """Generate comprehensive verification report"""
        logger.info("Generating verification report...")
        
        # Run all verifications
        self.compare_committee_structures()
        self.verify_leadership_accuracy()
        
        # Calculate accuracy scores
        house_discrepancies = len(self.verification_results['house_committees']['discrepancies'])
        senate_discrepancies = len(self.verification_results['senate_committees']['discrepancies'])
        leadership_errors = len(self.verification_results['leadership_errors'])
        
        total_issues = house_discrepancies + senate_discrepancies + leadership_errors
        
        # Generate report
        report = f"""
CONGRESSIONAL DATA VERIFICATION REPORT
Generated: {self.verification_results['timestamp']}

SUMMARY
=======
Total Issues Found: {total_issues}
- House Committee Issues: {house_discrepancies}
- Senate Committee Issues: {senate_discrepancies}
- Leadership Errors: {leadership_errors}

DETAILED FINDINGS
================

House Committees:
- Authoritative Sources: {len(self.verification_results['house_committees']['authoritative'])}
- Database: {len(self.verification_results['house_committees']['database'])}
- Discrepancies: {house_discrepancies}

Senate Committees:
- Authoritative Sources: {len(self.verification_results['senate_committees']['authoritative'])}
- Database: {len(self.verification_results['senate_committees']['database'])}
- Discrepancies: {senate_discrepancies}

Leadership Issues:
"""
        
        for error in self.verification_results['leadership_errors']:
            report += f"- {error['committee']} ({error['chamber']}): {error['member']} ({error['party']}) as {error['position']} - {error['error']}\n"
        
        report += f"""
COMMITTEE DISCREPANCIES
======================
"""
        
        for disc in self.verification_results['house_committees']['discrepancies']:
            report += f"- {disc['type']}: {disc['committee']} - {disc['issue']}\n"
        
        return report
    
    def save_results(self, filename: str = None):
        """Save verification results to file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"verification_results_{timestamp}.json"
        
        filepath = f"/Users/noelmcmichael/Workspace/congress_data_automator/docs/progress/{filename}"
        
        with open(filepath, 'w') as f:
            json.dump(self.verification_results, f, indent=2)
        
        logger.info(f"Verification results saved to {filepath}")
        return filepath

def main():
    """Run comprehensive verification"""
    verifier = CongressionalDataVerifier()
    
    print("Starting Congressional Data Verification...")
    print("=" * 50)
    
    # Generate report
    report = verifier.generate_verification_report()
    print(report)
    
    # Save results
    results_file = verifier.save_results()
    print(f"\nDetailed results saved to: {results_file}")
    
    # Save report
    report_file = "/Users/noelmcmichael/Workspace/congress_data_automator/docs/progress/verification_report.txt"
    with open(report_file, 'w') as f:
        f.write(report)
    
    print(f"Report saved to: {report_file}")

if __name__ == "__main__":
    main()