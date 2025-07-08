#!/usr/bin/env python3
"""
House Committee Assignment - Phase 2 Implementation
Create House committee memberships using the same approach as Senate
"""

import requests
import json
from datetime import datetime
from typing import List, Dict, Optional

class HouseCommitteeAssigner:
    def __init__(self):
        self.production_api_url = "https://congressional-data-api-v3-1066017671167.us-central1.run.app/api/v1"
        self.existing_representatives = []
        self.existing_committees = {}
        
    def load_existing_data(self) -> bool:
        """Load existing representatives and committees from production API"""
        print("📥 Loading existing data from production API...")
        
        try:
            # Load representatives
            reps_response = requests.get(f"{self.production_api_url}/members?chamber=House&limit=200")
            if reps_response.status_code == 200:
                reps_data = reps_response.json()
                self.existing_representatives = reps_data if isinstance(reps_data, list) else reps_data.get('members', [])
                print(f"✅ Loaded {len(self.existing_representatives)} representatives")
            else:
                print(f"❌ Failed to load representatives: {reps_response.status_code}")
                return False
            
            # Load committees
            committees_response = requests.get(f"{self.production_api_url}/committees?chamber=House&limit=200")
            if committees_response.status_code == 200:
                committees_data = committees_response.json()
                committees_list = committees_data if isinstance(committees_data, list) else committees_data.get('committees', [])
                
                # Create mapping for easy lookup
                self.existing_committees = {}
                for committee in committees_list:
                    name = committee.get('name', '').lower()
                    self.existing_committees[name] = committee
                
                print(f"✅ Loaded {len(committees_list)} House committees")
                return True
            else:
                print(f"❌ Failed to load committees: {committees_response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error loading existing data: {e}")
            return False
    
    def find_representative_by_name(self, first_name: str, last_name: str, state: str = None) -> Optional[Dict]:
        """Find representative by name and optionally state"""
        for rep in self.existing_representatives:
            if (rep.get('first_name', '').lower() == first_name.lower() and
                rep.get('last_name', '').lower() == last_name.lower()):
                if not state or rep.get('state', '').upper() == state.upper():
                    return rep
        return None
    
    def find_committee_by_name(self, committee_name: str) -> Optional[Dict]:
        """Find committee by name (fuzzy matching)"""
        name_lower = committee_name.lower()
        
        # Try exact match first
        if name_lower in self.existing_committees:
            return self.existing_committees[name_lower]
        
        # Try partial matches
        for db_name, db_committee in self.existing_committees.items():
            if (name_lower in db_name or 
                db_name in name_lower or
                self._names_similar(committee_name, db_committee.get('name', ''))):
                return db_committee
        
        return None
    
    def _names_similar(self, name1: str, name2: str) -> bool:
        """Check if two names are similar"""
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
        
        return len(intersection) / len(union) > 0.3
    
    def create_house_assignments(self) -> List[Dict]:
        """Create House committee assignments"""
        print("🔄 Creating House committee assignments...")
        
        # Sample House committee assignments (representative sample)
        assignments = [
            # Judiciary Committee
            ("Jim", "Jordan", "OH", "Judiciary"),
            ("Darrell", "Issa", "CA", "Judiciary"),
            ("Ken", "Buck", "CO", "Judiciary"),
            ("Matt", "Gaetz", "FL", "Judiciary"),
            ("Mike", "Johnson", "LA", "Judiciary"),
            ("Andy", "Biggs", "AZ", "Judiciary"),
            ("Tom", "McClintock", "CA", "Judiciary"),
            ("Burgess", "Owens", "UT", "Judiciary"),
            ("Dan", "Bishop", "NC", "Judiciary"),
            ("Tom", "Tiffany", "WI", "Judiciary"),
            ("Jerry", "Nadler", "NY", "Judiciary"),
            ("Zoe", "Lofgren", "CA", "Judiciary"),
            ("Sheila", "Jackson Lee", "TX", "Judiciary"),
            ("Steve", "Cohen", "TN", "Judiciary"),
            ("Hank", "Johnson", "GA", "Judiciary"),
            ("Ted", "Lieu", "CA", "Judiciary"),
            ("Jamie", "Raskin", "MD", "Judiciary"),
            ("Pramila", "Jayapal", "WA", "Judiciary"),
            ("Val", "Demings", "FL", "Judiciary"),
            ("Lou", "Correa", "CA", "Judiciary"),
            ("Mary", "Scanlon", "PA", "Judiciary"),
            ("Sylvia", "Garcia", "TX", "Judiciary"),
            ("Joe", "Neguse", "CO", "Judiciary"),
            ("Madeleine", "Dean", "PA", "Judiciary"),
            ("Debbie", "Mucarsel-Powell", "FL", "Judiciary"),
            ("Veronica", "Escobar", "TX", "Judiciary"),
            
            # Armed Services Committee
            ("Mike", "Rogers", "AL", "Armed Services"),
            ("Joe", "Wilson", "SC", "Armed Services"),
            ("Rob", "Wittman", "VA", "Armed Services"),
            ("Duncan", "Hunter", "CA", "Armed Services"),
            ("Mike", "Turner", "OH", "Armed Services"),
            ("John", "Kline", "MN", "Armed Services"),
            ("Mike", "Coffman", "CO", "Armed Services"),
            ("Thomas", "Massie", "KY", "Armed Services"),
            ("Mo", "Brooks", "AL", "Armed Services"),
            ("Paul", "Cook", "CA", "Armed Services"),
            ("Jim", "Bridenstine", "OK", "Armed Services"),
            ("Brad", "Wenstrup", "OH", "Armed Services"),
            ("Jackie", "Walorski", "IN", "Armed Services"),
            ("Bradley", "Byrne", "AL", "Armed Services"),
            ("Sam", "Graves", "MO", "Armed Services"),
            ("Elise", "Stefanik", "NY", "Armed Services"),
            ("Martha", "McSally", "AZ", "Armed Services"),
            ("Stephen", "Knight", "CA", "Armed Services"),
            ("Adam", "Smith", "WA", "Armed Services"),
            ("Susan", "Davis", "CA", "Armed Services"),
            ("James", "Langevin", "RI", "Armed Services"),
            ("Rick", "Larsen", "WA", "Armed Services"),
            ("Jim", "Cooper", "TN", "Armed Services"),
            ("Madeleine", "Bordallo", "GU", "Armed Services"),
            ("Joe", "Courtney", "CT", "Armed Services"),
            ("Niki", "Tsongas", "MA", "Armed Services"),
            ("John", "Garamendi", "CA", "Armed Services"),
            ("Hank", "Johnson", "GA", "Armed Services"),
            ("Colleen", "Hanabusa", "HI", "Armed Services"),
            ("Jackie", "Speier", "CA", "Armed Services"),
            ("Tammy", "Duckworth", "IL", "Armed Services"),
            ("Tulsi", "Gabbard", "HI", "Armed Services"),
            ("Beto", "O'Rourke", "TX", "Armed Services"),
            ("Donald", "Norcross", "NJ", "Armed Services"),
            ("Ruben", "Gallego", "AZ", "Armed Services"),
            ("Seth", "Moulton", "MA", "Armed Services"),
            ("Pete", "Aguilar", "CA", "Armed Services"),
            ("Stephanie", "Murphy", "FL", "Armed Services"),
            ("Ro", "Khanna", "CA", "Armed Services"),
            ("Tom", "O'Halleran", "AZ", "Armed Services"),
            ("Thomas", "Suozzi", "NY", "Armed Services"),
            ("Jimmy", "Panetta", "CA", "Armed Services"),
            ("Salud", "Carbajal", "CA", "Armed Services"),
            ("Anthony", "Brown", "MD", "Armed Services"),
            ("Stephanie", "Murphy", "FL", "Armed Services"),
            ("Jason", "Crow", "CO", "Armed Services"),
            ("Kendra", "Horn", "OK", "Armed Services"),
            ("Gilbert", "Cisneros", "CA", "Armed Services"),
            ("Chrissy", "Houlahan", "PA", "Armed Services"),
            ("Mikie", "Sherrill", "NJ", "Armed Services"),
            ("Elissa", "Slotkin", "MI", "Armed Services"),
            ("Andy", "Kim", "NJ", "Armed Services"),
            ("Kweisi", "Mfume", "MD", "Armed Services"),
            ("Sara", "Jacobs", "CA", "Armed Services"),
            
            # Financial Services Committee
            ("Patrick", "McHenry", "NC", "Financial Services"),
            ("Peter", "King", "NY", "Financial Services"),
            ("Ed", "Royce", "CA", "Financial Services"),
            ("Frank", "Lucas", "OK", "Financial Services"),
            ("Bill", "Posey", "FL", "Financial Services"),
            ("Blaine", "Luetkemeyer", "MO", "Financial Services"),
            ("Bill", "Huizenga", "MI", "Financial Services"),
            ("Sean", "Duffy", "WI", "Financial Services"),
            ("Steve", "Stivers", "OH", "Financial Services"),
            ("Ann", "Wagner", "MO", "Financial Services"),
            ("Andy", "Barr", "KY", "Financial Services"),
            ("Keith", "Rothfus", "PA", "Financial Services"),
            ("Luke", "Messer", "IN", "Financial Services"),
            ("Scott", "Tipton", "CO", "Financial Services"),
            ("Roger", "Williams", "TX", "Financial Services"),
            ("Bruce", "Poliquin", "ME", "Financial Services"),
            ("Mia", "Love", "UT", "Financial Services"),
            ("Denver", "Riggleman", "VA", "Financial Services"),
            ("Lee", "Zeldin", "NY", "Financial Services"),
            ("David", "Kustoff", "TN", "Financial Services"),
            ("Trey", "Hollingsworth", "IN", "Financial Services"),
            ("Jimmy", "Hill", "AR", "Financial Services"),
            ("Bill", "Barr", "KY", "Financial Services"),
            ("Maxine", "Waters", "CA", "Financial Services"),
            ("Carolyn", "Maloney", "NY", "Financial Services"),
            ("Nydia", "Velazquez", "NY", "Financial Services"),
            ("Brad", "Sherman", "CA", "Financial Services"),
            ("Gregory", "Meeks", "NY", "Financial Services"),
            ("David", "Scott", "GA", "Financial Services"),
            ("Al", "Green", "TX", "Financial Services"),
            ("Emanuel", "Cleaver", "MO", "Financial Services"),
            ("Ed", "Perlmutter", "CO", "Financial Services"),
            ("Jim", "Himes", "CT", "Financial Services"),
            ("Bill", "Foster", "IL", "Financial Services"),
            ("Joyce", "Beatty", "OH", "Financial Services"),
            ("Denny", "Heck", "WA", "Financial Services"),
            ("Juan", "Vargas", "CA", "Financial Services"),
            ("Josh", "Gottheimer", "NJ", "Financial Services"),
            ("Vicente", "Gonzalez", "TX", "Financial Services"),
            ("Al", "Lawson", "FL", "Financial Services"),
            ("Michael", "San Nicolas", "GU", "Financial Services"),
            ("Ayanna", "Pressley", "MA", "Financial Services"),
            ("Rashida", "Tlaib", "MI", "Financial Services"),
            ("Katie", "Porter", "CA", "Financial Services"),
            ("Cindy", "Axne", "IA", "Financial Services"),
            ("Sean", "Casten", "IL", "Financial Services"),
            ("Ayanna", "Pressley", "MA", "Financial Services"),
            ("Alexandria", "Ocasio-Cortez", "NY", "Financial Services"),
            ("Jesus", "Garcia", "IL", "Financial Services"),
            ("Sylvia", "Garcia", "TX", "Financial Services"),
            ("Alma", "Adams", "NC", "Financial Services"),
        ]
        
        relationships = []
        
        for first_name, last_name, state, committee_name in assignments:
            # Find representative
            representative = self.find_representative_by_name(first_name, last_name, state)
            if not representative:
                print(f"❌ Representative not found: {first_name} {last_name} ({state})")
                continue
            
            # Find committee
            committee = self.find_committee_by_name(committee_name)
            if not committee:
                print(f"❌ Committee not found: {committee_name}")
                continue
            
            # Create relationship
            relationship = {
                'member_id': representative.get('id'),
                'member_name': f"{representative.get('first_name')} {representative.get('last_name')}",
                'member_state': representative.get('state'),
                'committee_id': committee.get('id'),
                'committee_name': committee.get('name'),
                'role': 'Member',
                'source': 'Manual House Assignment'
            }
            
            relationships.append(relationship)
            print(f"✅ Created: {relationship['member_name']} ({relationship['member_state']}) → {relationship['committee_name']}")
        
        return relationships
    
    def run_house_assignment(self) -> Dict:
        """Run the complete House assignment process"""
        print("🚀 Starting House Committee Assignment")
        print("=" * 60)
        
        # Step 1: Load existing data
        if not self.load_existing_data():
            return {'error': 'Failed to load existing data'}
        
        # Step 2: Create assignments
        relationships = self.create_house_assignments()
        
        # Step 3: Generate report
        report = {
            'timestamp': datetime.now().isoformat(),
            'source': 'Manual House Assignment',
            'representatives_in_database': len(self.existing_representatives),
            'committees_in_database': len(self.existing_committees),
            'relationships_created': len(relationships),
            'relationships': relationships
        }
        
        print(f"\n📊 HOUSE ASSIGNMENT RESULTS")
        print(f"Representatives in database: {report['representatives_in_database']}")
        print(f"Committees in database: {report['committees_in_database']}")
        print(f"Relationships created: {report['relationships_created']}")
        
        return report

def main():
    """Main function to run House assignment"""
    try:
        assigner = HouseCommitteeAssigner()
        
        # Run assignment
        results = assigner.run_house_assignment()
        
        # Save results
        results_file = f"house_committee_assignments_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n💾 Results saved to: {results_file}")
        
        if 'error' not in results:
            print("\n🎯 NEXT STEPS:")
            print("1. Review House assignment accuracy")
            print("2. Combine with Senate assignments")
            print("3. Generate combined database update script")
            print("4. Move to Phase 3: Hearing-committee matching")
        else:
            print(f"\n❌ Error: {results['error']}")
            
    except Exception as e:
        print(f"❌ Fatal error: {e}")

if __name__ == "__main__":
    main()