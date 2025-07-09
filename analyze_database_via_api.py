"""
Phase 2 Step 2.1: Database Analysis via API
Analyze current database structure and leadership positions via production API.
"""

import requests
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

class DatabaseAnalyzer:
    """Analyze database through production API."""
    
    def __init__(self):
        self.base_url = "https://congressional-data-api-v2-1066017671167.us-central1.run.app/api/v1"
        self.headers = {
            "User-Agent": "Congressional Data Automator - Database Analysis",
            "Accept": "application/json"
        }
    
    def get_api_data(self, endpoint: str) -> Dict[str, Any]:
        """Get data from API endpoint."""
        try:
            response = requests.get(f"{self.base_url}/{endpoint}", headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching {endpoint}: {e}")
            return {}
    
    def analyze_database(self):
        """Analyze database structure and current state."""
        print("🔍 Phase 2 Step 2.1: Database Analysis via API")
        print("=" * 70)
        
        # 1. Test API connectivity
        print("\n1. Testing API Connectivity...")
        health_response = requests.get("https://congressional-data-api-v2-1066017671167.us-central1.run.app/health", headers=self.headers)
        health = health_response.json() if health_response.status_code == 200 else {}
        if health.get("status") == "healthy":
            print("   ✅ API connection successful")
        else:
            print("   ❌ API connection failed")
            return None
        
        # 2. Get database statistics
        print("\n2. Analyzing Database Statistics...")
        
        # Get all committees
        committees = self.get_api_data("committees?limit=500")
        if isinstance(committees, list):
            committees_count = len(committees)
            print(f"   📊 Total committees: {committees_count}")
            
            # Analyze committee types
            chambers = {}
            standing_committees = []
            subcommittees = []
            
            for committee in committees:
                chamber = committee.get("chamber", "Unknown")
                chambers[chamber] = chambers.get(chamber, 0) + 1
                
                if committee.get("is_subcommittee", False):
                    subcommittees.append(committee)
                else:
                    standing_committees.append(committee)
            
            print(f"   📋 Standing committees: {len(standing_committees)}")
            print(f"   📋 Subcommittees: {len(subcommittees)}")
            print(f"   📋 By chamber: {chambers}")
        
        # Get all members
        members = self.get_api_data("members?limit=600")
        if isinstance(members, list):
            members_count = len(members)
            print(f"   📊 Total members: {members_count}")
            
            # Analyze member distribution
            member_chambers = {}
            member_parties = {}
            
            for member in members:
                chamber = member.get("chamber", "Unknown")
                party = member.get("party", "Unknown")
                
                member_chambers[chamber] = member_chambers.get(chamber, 0) + 1
                member_parties[party] = member_parties.get(party, 0) + 1
            
            print(f"   📋 By chamber: {member_chambers}")
            print(f"   📋 By party: {member_parties}")
        
        # 3. Check for key Wikipedia committee leaders
        print("\n3. Checking Key Wikipedia Leaders...")
        
        # Key leaders from Wikipedia to check
        key_leaders = [
            {"name": "Grassley", "expected_role": "Senate Judiciary Chair"},
            {"name": "Cruz", "expected_role": "Senate Commerce Chair"},
            {"name": "Collins", "expected_role": "Senate Appropriations Chair"},
            {"name": "Durbin", "expected_role": "Senate Judiciary Ranking Member"},
            {"name": "Jordan", "expected_role": "House Judiciary Chair"},
            {"name": "Cole", "expected_role": "House Appropriations Chair"}
        ]
        
        found_leaders = []
        for leader in key_leaders:
            member_data = self.get_api_data(f"members?search={leader['name']}")
            if isinstance(member_data, list) and len(member_data) > 0:
                member = member_data[0]
                found_leaders.append({
                    "name": f"{member['first_name']} {member['last_name']}",
                    "party": member.get("party", "Unknown"),
                    "chamber": member.get("chamber", "Unknown"),
                    "state": member.get("state", "Unknown"),
                    "expected_role": leader["expected_role"],
                    "member_id": member.get("id")
                })
                print(f"   ✅ Found {member['first_name']} {member['last_name']} ({member['party']}-{member['state']})")
            else:
                print(f"   ❌ {leader['name']} not found in database")
        
        # 4. Check committee leadership structure
        print("\n4. Analyzing Committee Leadership Structure...")
        
        # Check specific committees from Wikipedia
        key_committees = [
            {"name": "Judiciary", "chamber": "Senate"},
            {"name": "Judiciary", "chamber": "House"},
            {"name": "Appropriations", "chamber": "Senate"},
            {"name": "Appropriations", "chamber": "House"},
            {"name": "Commerce", "chamber": "Senate"},
            {"name": "Armed Services", "chamber": "Senate"}
        ]
        
        committee_leadership = []
        for committee_info in key_committees:
            committee_data = self.get_api_data(f"committees?search={committee_info['name']}")
            if isinstance(committee_data, list):
                # Find the committee matching the chamber
                for committee in committee_data:
                    if committee.get("chamber") == committee_info["chamber"] and not committee.get("is_subcommittee", False):
                        committee_leadership.append({
                            "committee_id": committee.get("id"),
                            "name": committee.get("name"),
                            "chamber": committee.get("chamber"),
                            "has_leadership_api": False  # Current API doesn't expose leadership
                        })
                        print(f"   📋 {committee['name']} ({committee['chamber']}) - ID: {committee['id']}")
                        break
        
        # 5. Save analysis results
        analysis_results = {
            "timestamp": datetime.now().isoformat(),
            "database_stats": {
                "committees_count": committees_count if 'committees_count' in locals() else 0,
                "standing_committees": len(standing_committees) if 'standing_committees' in locals() else 0,
                "subcommittees": len(subcommittees) if 'subcommittees' in locals() else 0,
                "members_count": members_count if 'members_count' in locals() else 0,
                "chamber_distribution": member_chambers if 'member_chambers' in locals() else {},
                "party_distribution": member_parties if 'member_parties' in locals() else {}
            },
            "key_leaders_found": found_leaders,
            "committee_leadership": committee_leadership,
            "api_structure": {
                "committees_endpoint": f"{self.base_url}/committees",
                "members_endpoint": f"{self.base_url}/members",
                "leadership_exposed": False,
                "reconciliation_approach": "API-based member and committee matching"
            }
        }
        
        with open("database_analysis_via_api.json", "w") as f:
            json.dump(analysis_results, f, indent=2)
        
        print(f"\n✅ Analysis complete! Results saved to database_analysis_via_api.json")
        print(f"   📊 Summary: {len(found_leaders)} key leaders found, {len(committee_leadership)} committees identified")
        
        return analysis_results

if __name__ == "__main__":
    analyzer = DatabaseAnalyzer()
    analyzer.analyze_database()