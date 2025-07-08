#!/usr/bin/env python3
"""
Manual committee assignment approach
Create realistic committee memberships based on known senators and committees
This validates our database update approach before implementing full automation
"""

import requests
import json
from datetime import datetime
from typing import List, Dict, Optional

class ManualCommitteeAssigner:
    def __init__(self):
        self.production_api_url = "https://congressional-data-api-v3-1066017671167.us-central1.run.app/api/v1"
        self.existing_senators = []
        self.existing_committees = {}
        self.manual_assignments = []
        
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
    
    def find_senator_by_name(self, first_name: str, last_name: str, state: str = None) -> Optional[Dict]:
        """Find senator by name and optionally state"""
        for senator in self.existing_senators:
            if (senator.get('first_name', '').lower() == first_name.lower() and
                senator.get('last_name', '').lower() == last_name.lower()):
                if not state or senator.get('state', '').upper() == state.upper():
                    return senator
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
    
    def create_realistic_assignments(self) -> List[Dict]:
        """Create realistic committee assignments based on known senators"""
        print("🔄 Creating realistic committee assignments...")
        
        # Known committee assignments (based on public information)
        # This is a representative sample to validate our approach
        assignments = [
            # Judiciary Committee
            ("Chuck", "Grassley", "IA", "Judiciary"),
            ("Lindsey", "Graham", "SC", "Judiciary"),
            ("John", "Cornyn", "TX", "Judiciary"),
            ("Mike", "Lee", "UT", "Judiciary"),
            ("Ted", "Cruz", "TX", "Judiciary"),
            ("Josh", "Hawley", "MO", "Judiciary"),
            ("Tom", "Cotton", "AR", "Judiciary"),
            ("John", "Kennedy", "LA", "Judiciary"),
            ("Dick", "Durbin", "IL", "Judiciary"),
            ("Sheldon", "Whitehouse", "RI", "Judiciary"),
            ("Amy", "Klobuchar", "MN", "Judiciary"),
            ("Chris", "Coons", "DE", "Judiciary"),
            ("Richard", "Blumenthal", "CT", "Judiciary"),
            ("Mazie", "Hirono", "HI", "Judiciary"),
            ("Cory", "Booker", "NJ", "Judiciary"),
            ("Alex", "Padilla", "CA", "Judiciary"),
            ("Jon", "Ossoff", "GA", "Judiciary"),
            ("Peter", "Welch", "VT", "Judiciary"),
            
            # Armed Services Committee
            ("Roger", "Wicker", "MS", "Armed Services"),
            ("Deb", "Fischer", "NE", "Armed Services"),
            ("Tom", "Cotton", "AR", "Armed Services"),
            ("Mike", "Rounds", "SD", "Armed Services"),
            ("Joni", "Ernst", "IA", "Armed Services"),
            ("Dan", "Sullivan", "AK", "Armed Services"),
            ("Kevin", "Cramer", "ND", "Armed Services"),
            ("Rick", "Scott", "FL", "Armed Services"),
            ("Jack", "Reed", "RI", "Armed Services"),
            ("Jeanne", "Shaheen", "NH", "Armed Services"),
            ("Kirsten", "Gillibrand", "NY", "Armed Services"),
            ("Richard", "Blumenthal", "CT", "Armed Services"),
            ("Mazie", "Hirono", "HI", "Armed Services"),
            ("Tim", "Kaine", "VA", "Armed Services"),
            ("Angus", "King", "ME", "Armed Services"),
            ("Martin", "Heinrich", "NM", "Armed Services"),
            ("Elizabeth", "Warren", "MA", "Armed Services"),
            ("Gary", "Peters", "MI", "Armed Services"),
            ("Joe", "Manchin", "WV", "Armed Services"),
            ("Jacky", "Rosen", "NV", "Armed Services"),
            ("Mark", "Kelly", "AZ", "Armed Services"),
            ("Elissa", "Slotkin", "MI", "Armed Services"),
            
            # Finance Committee
            ("Mike", "Crapo", "ID", "Finance"),
            ("Chuck", "Grassley", "IA", "Finance"),
            ("John", "Cornyn", "TX", "Finance"),
            ("John", "Thune", "SD", "Finance"),
            ("Richard", "Burr", "NC", "Finance"),
            ("Rob", "Portman", "OH", "Finance"),
            ("Pat", "Toomey", "PA", "Finance"),
            ("Tim", "Scott", "SC", "Finance"),
            ("Bill", "Cassidy", "LA", "Finance"),
            ("James", "Lankford", "OK", "Finance"),
            ("Steve", "Daines", "MT", "Finance"),
            ("Todd", "Young", "IN", "Finance"),
            ("Ben", "Sasse", "NE", "Finance"),
            ("Ron", "Wyden", "OR", "Finance"),
            ("Debbie", "Stabenow", "MI", "Finance"),
            ("Maria", "Cantwell", "WA", "Finance"),
            ("Bob", "Menendez", "NJ", "Finance"),
            ("Tom", "Carper", "DE", "Finance"),
            ("Ben", "Cardin", "MD", "Finance"),
            ("Sherrod", "Brown", "OH", "Finance"),
            ("Michael", "Bennet", "CO", "Finance"),
            ("Bob", "Casey", "PA", "Finance"),
            ("Mark", "Warner", "VA", "Finance"),
            ("Sheldon", "Whitehouse", "RI", "Finance"),
            ("Maggie", "Hassan", "NH", "Finance"),
            ("Catherine", "Cortez Masto", "NV", "Finance"),
            ("Elizabeth", "Warren", "MA", "Finance"),
        ]
        
        relationships = []
        
        for first_name, last_name, state, committee_name in assignments:
            # Find senator
            senator = self.find_senator_by_name(first_name, last_name, state)
            if not senator:
                print(f"❌ Senator not found: {first_name} {last_name} ({state})")
                continue
            
            # Find committee
            committee = self.find_committee_by_name(committee_name)
            if not committee:
                print(f"❌ Committee not found: {committee_name}")
                continue
            
            # Create relationship
            relationship = {
                'member_id': senator.get('id'),
                'member_name': f"{senator.get('first_name')} {senator.get('last_name')}",
                'member_state': senator.get('state'),
                'committee_id': committee.get('id'),
                'committee_name': committee.get('name'),
                'role': 'Member',
                'source': 'Manual Assignment'
            }
            
            relationships.append(relationship)
            print(f"✅ Created: {relationship['member_name']} ({relationship['member_state']}) → {relationship['committee_name']}")
        
        return relationships
    
    def validate_assignments(self, relationships: List[Dict]) -> Dict:
        """Validate the created assignments"""
        print("🔍 Validating assignments...")
        
        # Count by committee
        committee_counts = {}
        for rel in relationships:
            committee_name = rel['committee_name']
            if committee_name not in committee_counts:
                committee_counts[committee_name] = 0
            committee_counts[committee_name] += 1
        
        # Count by state
        state_counts = {}
        for rel in relationships:
            state = rel['member_state']
            if state not in state_counts:
                state_counts[state] = 0
            state_counts[state] += 1
        
        validation_report = {
            'total_relationships': len(relationships),
            'unique_senators': len(set(rel['member_id'] for rel in relationships)),
            'unique_committees': len(set(rel['committee_id'] for rel in relationships)),
            'committee_counts': committee_counts,
            'state_counts': state_counts,
            'validation_passed': len(relationships) > 0
        }
        
        print(f"📊 Validation Results:")
        print(f"  Total relationships: {validation_report['total_relationships']}")
        print(f"  Unique senators: {validation_report['unique_senators']}")
        print(f"  Unique committees: {validation_report['unique_committees']}")
        print(f"  Committee distribution: {committee_counts}")
        
        return validation_report
    
    def run_manual_assignment(self) -> Dict:
        """Run the complete manual assignment process"""
        print("🚀 Starting Manual Committee Assignment")
        print("=" * 60)
        
        # Step 1: Load existing data
        if not self.load_existing_data():
            return {'error': 'Failed to load existing data'}
        
        # Step 2: Create assignments
        relationships = self.create_realistic_assignments()
        
        # Step 3: Validate assignments
        validation = self.validate_assignments(relationships)
        
        # Step 4: Generate report
        report = {
            'timestamp': datetime.now().isoformat(),
            'source': 'Manual Assignment',
            'senators_in_database': len(self.existing_senators),
            'committees_in_database': len(self.existing_committees),
            'relationships_created': len(relationships),
            'validation': validation,
            'relationships': relationships
        }
        
        print(f"\n📊 ASSIGNMENT RESULTS SUMMARY")
        print(f"Senators in database: {report['senators_in_database']}")
        print(f"Committees in database: {report['committees_in_database']}")
        print(f"Relationships created: {report['relationships_created']}")
        print(f"Success rate: {(report['relationships_created'] / 50) * 100:.1f}%")  # Rough estimate
        
        return report

def main():
    """Main function to run manual assignment"""
    try:
        assigner = ManualCommitteeAssigner()
        
        # Run assignment
        results = assigner.run_manual_assignment()
        
        # Save results
        results_file = f"manual_senate_assignments_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n💾 Results saved to: {results_file}")
        
        if 'error' not in results:
            print("\n🎯 NEXT STEPS:")
            print("1. Review assignment accuracy")
            print("2. Implement database update script")
            print("3. Test API with new relationship data")
            print("4. Create House committee assignments")
            print("5. Implement hearing-committee matching")
        else:
            print(f"\n❌ Error: {results['error']}")
            
    except Exception as e:
        print(f"❌ Fatal error: {e}")

if __name__ == "__main__":
    main()