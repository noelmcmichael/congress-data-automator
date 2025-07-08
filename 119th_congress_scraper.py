#!/usr/bin/env python3
"""
119th Congress Data Scraper
Collects current committee assignments, chairs, and ranking members for the 119th Congress.

This module provides:
- Current committee structure collection
- Member-committee relationship extraction
- Leadership position identification (chairs, ranking members)
- Committee hierarchy mapping
"""

import re
import json
import requests
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from bs4 import BeautifulSoup
import time

@dataclass
class CommitteeMember:
    """Committee member with role information"""
    bioguide_id: Optional[str]
    name: str
    party: str
    state: str
    position: str  # Chair, Ranking, Member
    chamber: str   # House or Senate
    
@dataclass
class Committee:
    """Committee structure for 119th Congress"""
    name: str
    chamber: str
    committee_type: str  # Standing, Select, Joint
    chair: Optional[str] = None
    ranking_member: Optional[str] = None
    members: List[CommitteeMember] = None
    subcommittees: List['Committee'] = None
    
    def __post_init__(self):
        if self.members is None:
            self.members = []
        if self.subcommittees is None:
            self.subcommittees = []

class Congress119Scraper:
    """Scraper for 119th Congress committee data"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        self.base_urls = {
            'senate_assignments': 'https://www.senate.gov/general/committee_assignments/assignments.htm',
            'house_assignments': 'https://clerk.house.gov/committees',
            'senate_committees': 'https://www.senate.gov/committees/committee_list.htm'
        }
        
    def get_senate_committee_assignments(self) -> Dict[str, List[Dict]]:
        """
        Extract all Senate committee assignments from official Senate page.
        
        Returns:
            Dictionary mapping committee names to member lists
        """
        print("🏛️ Collecting Senate committee assignments for 119th Congress...")
        
        try:
            response = self.session.get(self.base_urls['senate_assignments'])
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            committees = {}
            current_senator = None
            
            # Find all senator sections
            senator_sections = soup.find_all(['h4', 'h3'], string=re.compile(r'\([DR]-\w{2}\)'))
            
            for section in senator_sections:
                # Extract senator info
                senator_text = section.get_text().strip()
                name_match = re.match(r'(.+?)\s+\(([DR])-(\w{2})\)', senator_text)
                
                if name_match:
                    senator_name = name_match.group(1).strip()
                    party = 'Democratic' if name_match.group(2) == 'D' else 'Republican'
                    state = name_match.group(3)
                    
                    current_senator = {
                        'name': senator_name,
                        'party': party,
                        'state': state,
                        'chamber': 'Senate'
                    }
                    
                    # Find committee list for this senator
                    ul_element = section.find_next_sibling('ul')
                    if ul_element:
                        committee_items = ul_element.find_all('li')
                        
                        for item in committee_items:
                            committee_text = item.get_text().strip()
                            
                            # Extract committee name and position
                            committee_info = self._parse_committee_assignment(committee_text)
                            if committee_info:
                                committee_name = committee_info['committee']
                                position = committee_info['position']
                                
                                if committee_name not in committees:
                                    committees[committee_name] = []
                                
                                member_info = current_senator.copy()
                                member_info['position'] = position
                                committees[committee_name].append(member_info)
            
            print(f"✅ Collected {len(committees)} Senate committees with member assignments")
            return committees
            
        except Exception as e:
            print(f"❌ Error collecting Senate assignments: {e}")
            return {}
    
    def _parse_committee_assignment(self, text: str) -> Optional[Dict]:
        """Parse committee assignment text to extract committee name and position"""
        # Remove "Committee on " prefix and clean up
        clean_text = re.sub(r'^Committee on ', '', text)
        clean_text = re.sub(r'^Select Committee on ', '', clean_text)
        clean_text = re.sub(r'^Special Committee on ', '', clean_text)
        clean_text = re.sub(r'^Joint ', '', clean_text)
        
        # Check for leadership positions
        position = 'Member'
        if '(Chairman)' in text or '(Chair)' in text:
            position = 'Chair'
            clean_text = re.sub(r'\s*\(Chair(?:man)?\)', '', clean_text)
        elif '(Ranking)' in text or '(Ranking Member)' in text:
            position = 'Ranking Member'
            clean_text = re.sub(r'\s*\(Ranking(?: Member)?\)', '', clean_text)
        
        # Extract committee name (before any subcommittee info)
        committee_match = re.match(r'^([^-\n]+)', clean_text)
        if committee_match:
            committee_name = committee_match.group(1).strip()
            return {
                'committee': committee_name,
                'position': position
            }
        
        return None
    
    def get_committee_leadership(self, committees: Dict) -> Dict:
        """
        Extract committee chairs and ranking members from assignments.
        
        Args:
            committees: Committee assignments dictionary
            
        Returns:
            Dictionary with leadership information
        """
        leadership = {}
        
        for committee_name, members in committees.items():
            chairs = [m for m in members if m['position'] == 'Chair']
            ranking = [m for m in members if m['position'] == 'Ranking Member']
            
            leadership[committee_name] = {
                'chair': chairs[0] if chairs else None,
                'ranking_member': ranking[0] if ranking else None,
                'total_members': len(members),
                'republicans': len([m for m in members if m['party'] == 'Republican']),
                'democrats': len([m for m in members if m['party'] == 'Democratic'])
            }
        
        return leadership
    
    def search_house_committees(self) -> Dict:
        """
        Collect House committee information from clerk.house.gov
        
        Returns:
            Dictionary of House committee data
        """
        print("🏛️ Collecting House committee data for 119th Congress...")
        
        # For now, return known major House committees structure
        # This would be enhanced with actual scraping from House.gov
        house_committees = {
            'Agriculture': {'chair': None, 'ranking_member': None, 'chamber': 'House'},
            'Appropriations': {'chair': None, 'ranking_member': None, 'chamber': 'House'},
            'Armed Services': {'chair': None, 'ranking_member': None, 'chamber': 'House'},
            'Education and the Workforce': {'chair': None, 'ranking_member': None, 'chamber': 'House'},
            'Energy and Commerce': {'chair': None, 'ranking_member': None, 'chamber': 'House'},
            'Financial Services': {'chair': None, 'ranking_member': None, 'chamber': 'House'},
            'Foreign Affairs': {'chair': None, 'ranking_member': None, 'chamber': 'House'},
            'Homeland Security': {'chair': None, 'ranking_member': None, 'chamber': 'House'},
            'House Administration': {'chair': None, 'ranking_member': None, 'chamber': 'House'},
            'Judiciary': {'chair': None, 'ranking_member': None, 'chamber': 'House'},
            'Natural Resources': {'chair': None, 'ranking_member': None, 'chamber': 'House'},
            'Oversight and Accountability': {'chair': None, 'ranking_member': None, 'chamber': 'House'},
            'Rules': {'chair': None, 'ranking_member': None, 'chamber': 'House'},
            'Science, Space, and Technology': {'chair': None, 'ranking_member': None, 'chamber': 'House'},
            'Small Business': {'chair': None, 'ranking_member': None, 'chamber': 'House'},
            'Transportation and Infrastructure': {'chair': None, 'ranking_member': None, 'chamber': 'House'},
            'Veterans\' Affairs': {'chair': None, 'ranking_member': None, 'chamber': 'House'},
            'Ways and Means': {'chair': None, 'ranking_member': None, 'chamber': 'House'}
        }
        
        print(f"✅ Identified {len(house_committees)} major House committees")
        return house_committees
    
    def validate_119th_congress_data(self, data: Dict) -> Dict:
        """
        Validate collected data against known 119th Congress facts.
        
        Args:
            data: Collected committee data
            
        Returns:
            Validation report
        """
        validation = {
            'timestamp': datetime.now().isoformat(),
            'congress_session': '119th Congress (2025-2027)',
            'validation_checks': [],
            'warnings': [],
            'data_quality': 'UNKNOWN'
        }
        
        # Check for known 119th Congress leadership
        known_leadership = {
            'Judiciary': {'chair': 'Chuck Grassley (R-IA)', 'expected': True},
            'Commerce, Science, and Transportation': {'chair': 'Ted Cruz (R-TX)', 'expected': True},
            'Finance': {'chair': 'Mike Crapo (R-ID)', 'expected': True},
            'Armed Services': {'chair': 'Roger Wicker (R-MS)', 'expected': True}
        }
        
        correct_leadership = 0
        total_checks = 0
        
        for committee, expected in known_leadership.items():
            if committee in data:
                committee_data = data[committee]
                if committee_data.get('chair'):
                    chair_name = committee_data['chair']['name']
                    if 'Grassley' in chair_name and committee == 'Judiciary':
                        correct_leadership += 1
                        validation['validation_checks'].append(f"✅ {committee}: Chuck Grassley correctly identified as Chair")
                    elif 'Cruz' in chair_name and 'Commerce' in committee:
                        correct_leadership += 1
                        validation['validation_checks'].append(f"✅ {committee}: Ted Cruz correctly identified as Chair")
                    elif 'Crapo' in chair_name and committee == 'Finance':
                        correct_leadership += 1
                        validation['validation_checks'].append(f"✅ {committee}: Mike Crapo correctly identified as Chair")
                    elif 'Wicker' in chair_name and 'Armed Services' in committee:
                        correct_leadership += 1
                        validation['validation_checks'].append(f"✅ {committee}: Roger Wicker correctly identified as Chair")
                    else:
                        validation['warnings'].append(f"⚠️ {committee}: Chair may be incorrect - found {chair_name}")
                else:
                    validation['warnings'].append(f"⚠️ {committee}: No chair identified")
                total_checks += 1
            else:
                validation['warnings'].append(f"⚠️ {committee}: Committee not found in data")
        
        # Calculate data quality score
        if total_checks > 0:
            quality_score = (correct_leadership / total_checks) * 100
            if quality_score >= 75:
                validation['data_quality'] = 'HIGH'
            elif quality_score >= 50:
                validation['data_quality'] = 'MEDIUM'
            else:
                validation['data_quality'] = 'LOW'
            
            validation['quality_score'] = quality_score
            validation['correct_leadership'] = f"{correct_leadership}/{total_checks}"
        
        return validation
    
    def export_119th_congress_data(self, output_file: str = None) -> str:
        """
        Export complete 119th Congress committee data.
        
        Args:
            output_file: Optional output filename
            
        Returns:
            Output file path
        """
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"119th_congress_data_{timestamp}.json"
        
        print(f"🏛️ Starting 119th Congress data collection...")
        
        # Collect Senate data
        senate_assignments = self.get_senate_committee_assignments()
        senate_leadership = self.get_committee_leadership(senate_assignments)
        
        # Collect House data (basic structure for now)
        house_committees = self.search_house_committees()
        
        # Combine data
        all_committees = {}
        
        # Add Senate committees
        for committee_name, members in senate_assignments.items():
            leadership = senate_leadership.get(committee_name, {})
            all_committees[f"Senate {committee_name}"] = {
                'name': committee_name,
                'chamber': 'Senate',
                'type': 'Standing',
                'chair': leadership.get('chair'),
                'ranking_member': leadership.get('ranking_member'),
                'members': members,
                'total_members': len(members),
                'republicans': len([m for m in members if m['party'] == 'Republican']),
                'democrats': len([m for m in members if m['party'] == 'Democratic'])
            }
        
        # Add House committees
        for committee_name, info in house_committees.items():
            all_committees[f"House {committee_name}"] = {
                'name': committee_name,
                'chamber': 'House',
                'type': 'Standing',
                'chair': None,  # Would be populated with actual House scraping
                'ranking_member': None,
                'members': [],
                'total_members': 0,
                'republicans': 0,
                'democrats': 0
            }
        
        # Generate validation report
        validation = self.validate_119th_congress_data(senate_leadership)
        
        # Create comprehensive export
        export_data = {
            'metadata': {
                'congress_session': '119th Congress',
                'session_period': '2025-2027',
                'collection_timestamp': datetime.now().isoformat(),
                'data_source': 'Official Congressional websites',
                'scraper_version': '1.0.0'
            },
            'summary': {
                'total_committees': len(all_committees),
                'senate_committees': len(senate_assignments),
                'house_committees': len(house_committees),
                'committees_with_chairs': sum(1 for c in all_committees.values() if c.get('chair')),
                'total_member_assignments': sum(c.get('total_members', 0) for c in all_committees.values())
            },
            'committees': all_committees,
            'validation': validation,
            'data_quality_assessment': {
                'senate_data': 'COMPLETE' if senate_assignments else 'INCOMPLETE',
                'house_data': 'STRUCTURE_ONLY',
                'leadership_accuracy': validation.get('data_quality', 'UNKNOWN'),
                'currency': '119TH_CONGRESS_CURRENT'
            }
        }
        
        # Export to file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"✅ 119th Congress data exported to: {output_file}")
        print(f"📊 Summary: {len(all_committees)} committees, {validation.get('quality_score', 0):.1f}% leadership accuracy")
        
        return output_file

def main():
    """Main function for testing and data collection"""
    print("🇺🇸 119th Congress Data Scraper")
    print("=" * 50)
    
    scraper = Congress119Scraper()
    
    # Export complete 119th Congress data
    output_file = scraper.export_119th_congress_data()
    
    print(f"\n✅ Data collection complete!")
    print(f"📁 Output file: {output_file}")
    print(f"🔍 Review the validation section for data quality assessment")

if __name__ == "__main__":
    main()