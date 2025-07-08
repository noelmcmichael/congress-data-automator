#!/usr/bin/env python3
"""
Use Congress.gov API to get committee membership information
This is more reliable than web scraping and provides authoritative data
"""

import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv
from typing import List, Dict, Optional

# Load environment variables
load_dotenv()

class CongressAPICommitteeScraper:
    def __init__(self):
        self.api_key = os.getenv('CONGRESS_API_KEY')
        if not self.api_key:
            raise ValueError("CONGRESS_API_KEY not found in environment variables")
        
        self.base_url = "https://api.congress.gov/v3"
        self.session = requests.Session()
        self.session.headers.update({
            'X-API-Key': self.api_key,
            'User-Agent': 'Congressional Data Automator'
        })
        
        # Production API for matching
        self.production_api_url = "https://congressional-data-api-v3-1066017671167.us-central1.run.app/api/v1"
        
        self.existing_senators = []
        self.existing_committees = {}
        self.relationships = []
    
    def load_existing_data(self) -> bool:
        """Load existing senators and committees from production API"""
        print("📥 Loading existing data from production API...")
        
        try:
            # Load senators
            senators_response = requests.get(f"{self.production_api_url}/members?chamber=Senate&limit=200")
            if senators_response.status_code == 200:
                senators_data = senators_response.json()
                self.existing_senators = senators_data if isinstance(senators_data, list) else senators_data.get('members', [])
                print(f"✅ Loaded {len(self.existing_senators)} senators")
            else:
                print(f"❌ Failed to load senators: {senators_response.status_code}")
                return False
            
            # Load committees
            committees_response = requests.get(f"{self.production_api_url}/committees?chamber=Senate&limit=200")
            if committees_response.status_code == 200:
                committees_data = committees_response.json()
                committees_list = committees_data if isinstance(committees_data, list) else committees_data.get('committees', [])
                
                # Create mapping for easy lookup
                self.existing_committees = {}
                for committee in committees_list:
                    name = committee.get('name', '').lower()
                    self.existing_committees[name] = committee
                
                print(f"✅ Loaded {len(committees_list)} committees")
                return True
            else:
                print(f"❌ Failed to load committees: {committees_response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error loading existing data: {e}")
            return False
    
    def get_senate_committees(self) -> List[Dict]:
        """Get all Senate committees from Congress.gov API"""
        print("🔍 Fetching Senate committees from Congress.gov API...")
        
        try:
            url = f"{self.base_url}/committee/senate"
            params = {
                'congress': '119',  # 119th Congress
                'format': 'json',
                'limit': 50
            }
            
            response = self.session.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                committees = data.get('committees', [])
                print(f"✅ Found {len(committees)} Senate committees")
                
                # Show some examples
                print("📋 Sample committees:")
                for committee in committees[:5]:
                    print(f"  - {committee.get('name')} ({committee.get('systemCode')})")
                
                return committees
            else:
                print(f"❌ Failed to get committees: {response.status_code} - {response.text}")
                return []
                
        except Exception as e:
            print(f"❌ Error fetching committees: {e}")
            return []
    
    def get_committee_members(self, committee_system_code: str, committee_name: str) -> List[Dict]:
        """Get members of a specific committee"""
        print(f"🔍 Fetching members for committee: {committee_name}")
        
        try:
            url = f"{self.base_url}/committee/senate/{committee_system_code}/membership"
            params = {
                'congress': '119',
                'format': 'json',
                'limit': 50
            }
            
            response = self.session.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                members = data.get('members', [])
                print(f"✅ Found {len(members)} members for {committee_name}")
                
                return members
            else:
                print(f"❌ Failed to get members for {committee_name}: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ Error fetching members for {committee_name}: {e}")
            return []
    
    def match_senator_to_database(self, congress_member: Dict) -> Optional[Dict]:
        """Match a Congress.gov member to our database senator"""
        if not congress_member or not self.existing_senators:
            return None
        
        # Get member details
        first_name = congress_member.get('firstName', '')
        last_name = congress_member.get('lastName', '')
        state = congress_member.get('state', '')
        
        # Try exact match first
        for senator in self.existing_senators:
            if (senator.get('first_name', '').lower() == first_name.lower() and
                senator.get('last_name', '').lower() == last_name.lower() and
                senator.get('state', '').upper() == state.upper()):
                return senator
        
        # Try last name + state match
        for senator in self.existing_senators:
            if (senator.get('last_name', '').lower() == last_name.lower() and
                senator.get('state', '').upper() == state.upper()):
                return senator
        
        return None
    
    def match_committee_to_database(self, committee_name: str) -> Optional[Dict]:
        """Match a committee name to our database committee"""
        if not committee_name or not self.existing_committees:
            return None
        
        # Try exact match first
        name_lower = committee_name.lower()
        if name_lower in self.existing_committees:
            return self.existing_committees[name_lower]
        
        # Try partial matches
        for db_name, db_committee in self.existing_committees.items():
            if (name_lower in db_name or 
                db_name in name_lower or
                self._committee_names_similar(committee_name, db_committee.get('name', ''))):
                return db_committee
        
        return None
    
    def _committee_names_similar(self, name1: str, name2: str) -> bool:
        """Check if two committee names are similar"""
        name1_words = set(name1.lower().split())
        name2_words = set(name2.lower().split())
        
        # Remove common words
        common_words = {'committee', 'on', 'the', 'and', 'of', 'for', 'to', 'in', 'subcommittee'}
        name1_words -= common_words
        name2_words -= common_words
        
        if not name1_words or not name2_words:
            return False
        
        # Check if majority of words match
        intersection = name1_words & name2_words
        union = name1_words | name2_words
        
        return len(intersection) / len(union) > 0.5
    
    def process_committee_memberships(self, committees: List[Dict]) -> List[Dict]:
        """Process all committee memberships"""
        print("🔄 Processing committee memberships...")
        
        all_relationships = []
        
        for committee in committees:
            committee_name = committee.get('name', '')
            system_code = committee.get('systemCode', '')
            
            if not system_code:
                print(f"⚠️  Skipping {committee_name} - no system code")
                continue
            
            # Get committee members
            members = self.get_committee_members(system_code, committee_name)
            
            if not members:
                print(f"⚠️  No members found for {committee_name}")
                continue
            
            # Match committee to database
            db_committee = self.match_committee_to_database(committee_name)
            if not db_committee:
                print(f"⚠️  No database match for committee: {committee_name}")
                continue
            
            # Process each member
            for member in members:
                # Match senator to database
                db_senator = self.match_senator_to_database(member)
                
                if db_senator:
                    relationship = {
                        'member_id': db_senator.get('id'),
                        'member_name': f"{db_senator.get('first_name')} {db_senator.get('last_name')}",
                        'member_state': db_senator.get('state'),
                        'committee_id': db_committee.get('id'),
                        'committee_name': db_committee.get('name'),
                        'role': member.get('role', 'Member'),
                        'congress_gov_data': {
                            'member_bioguide_id': member.get('bioguideId'),
                            'committee_system_code': system_code,
                            'original_committee_name': committee_name
                        }
                    }
                    
                    all_relationships.append(relationship)
                    print(f"✅ Matched: {relationship['member_name']} ({relationship['member_state']}) → {relationship['committee_name']}")
                else:
                    print(f"❌ No database match for senator: {member.get('firstName')} {member.get('lastName')} ({member.get('state')})")
        
        return all_relationships
    
    def run_committee_scraping(self) -> Dict:
        """Run the complete committee scraping process"""
        print("🚀 Starting Congress.gov API Committee Scraping")
        print("=" * 60)
        
        # Step 1: Load existing data
        if not self.load_existing_data():
            return {'error': 'Failed to load existing data'}
        
        # Step 2: Get Senate committees
        committees = self.get_senate_committees()
        if not committees:
            return {'error': 'Failed to get Senate committees'}
        
        # Step 3: Process memberships
        relationships = self.process_committee_memberships(committees)
        
        # Step 4: Generate report
        report = {
            'timestamp': datetime.now().isoformat(),
            'source': 'Congress.gov API',
            'congress': '119th',
            'senators_in_database': len(self.existing_senators),
            'committees_in_database': len(self.existing_committees),
            'congress_committees_found': len(committees),
            'relationships_created': len(relationships),
            'success_rate': len(relationships) / (len(committees) * 10) * 100 if committees else 0,  # Rough estimate
            'relationships': relationships,
            'committees_processed': [{'name': c.get('name'), 'system_code': c.get('systemCode')} for c in committees]
        }
        
        print(f"\n📊 SCRAPING RESULTS SUMMARY")
        print(f"Senators in database: {report['senators_in_database']}")
        print(f"Committees in database: {report['committees_in_database']}")
        print(f"Congress.gov committees: {report['congress_committees_found']}")
        print(f"Relationships created: {report['relationships_created']}")
        print(f"Estimated success rate: {report['success_rate']:.1f}%")
        
        return report

def main():
    """Main function to run committee scraping"""
    try:
        scraper = CongressAPICommitteeScraper()
        
        # Run scraping
        results = scraper.run_committee_scraping()
        
        # Save results
        results_file = f"senate_committee_relationships_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n💾 Results saved to: {results_file}")
        
        if 'error' not in results:
            print("\n🎯 NEXT STEPS:")
            print("1. Review relationship data for accuracy")
            print("2. Implement database updates")
            print("3. Test API with new relationship data")
            print("4. Scale to House committees")
        else:
            print(f"\n❌ Error: {results['error']}")
            
    except Exception as e:
        print(f"❌ Fatal error: {e}")

if __name__ == "__main__":
    main()