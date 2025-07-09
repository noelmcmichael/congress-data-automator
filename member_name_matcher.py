"""
Phase 2 Step 2.2: Member Name Matching Implementation
Match Wikipedia leader names with database member IDs.
"""

import json
import re
import requests
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
from fuzzywuzzy import fuzz

class MemberNameMatcher:
    """Match Wikipedia names to database member IDs."""
    
    def __init__(self):
        self.base_url = "https://congressional-data-api-v2-1066017671167.us-central1.run.app/api/v1"
        self.headers = {
            "User-Agent": "Congressional Data Automator - Member Name Matcher",
            "Accept": "application/json"
        }
        
        # Load Wikipedia data
        with open("wikipedia_data.json", "r") as f:
            self.wikipedia_data = json.load(f)
        
        # Load database analysis
        with open("database_analysis_via_api.json", "r") as f:
            self.database_analysis = json.load(f)
    
    def parse_wikipedia_name(self, name_string: str) -> Dict[str, str]:
        """
        Parse Wikipedia name format like 'Chuck Grassley (R-IA)' into components.
        """
        # Pattern for Name (Party-State) format
        pattern = r'^(.+?)\s*\(([DRI])-([A-Z]{2})\)$'
        match = re.match(pattern, name_string.strip())
        
        if match:
            full_name = match.group(1).strip()
            party_code = match.group(2)
            state = match.group(3)
            
            # Convert party code to full name
            party_mapping = {'D': 'Democratic', 'R': 'Republican', 'I': 'Independent'}
            party = party_mapping.get(party_code, party_code)
            
            # Split full name into first and last
            name_parts = full_name.split()
            first_name = name_parts[0] if name_parts else ""
            last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""
            
            return {
                "full_name": full_name,
                "first_name": first_name,
                "last_name": last_name,
                "party": party,
                "state": state,
                "original": name_string
            }
        else:
            # Handle cases without party/state info
            return {
                "full_name": name_string,
                "first_name": name_string.split()[0] if name_string.split() else "",
                "last_name": " ".join(name_string.split()[1:]) if len(name_string.split()) > 1 else "",
                "party": "Unknown",
                "state": "Unknown",
                "original": name_string
            }
    
    def search_member_by_name(self, name: str) -> List[Dict]:
        """Search for member by name using API."""
        try:
            response = requests.get(
                f"{self.base_url}/members?search={name}",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Error searching for {name}: {e}")
            return []
    
    def calculate_name_similarity(self, name1: str, name2: str) -> float:
        """Calculate similarity score between two names."""
        # Use token sort ratio to handle different name orders
        return fuzz.token_sort_ratio(name1.lower(), name2.lower())
    
    def match_member_to_database(self, parsed_name: Dict[str, str]) -> Optional[Dict]:
        """
        Match a parsed Wikipedia name to a database member.
        """
        # Search by last name first (most reliable)
        candidates = self.search_member_by_name(parsed_name["last_name"])
        
        if not candidates:
            # Fallback to first name search
            candidates = self.search_member_by_name(parsed_name["first_name"])
        
        if not candidates:
            return None
        
        best_match = None
        best_score = 0
        
        for candidate in candidates:
            # Calculate name similarity
            candidate_full = f"{candidate['first_name']} {candidate['last_name']}"
            name_score = self.calculate_name_similarity(parsed_name["full_name"], candidate_full)
            
            # Boost score for matching party and state
            party_match = candidate.get("party", "").lower() == parsed_name["party"].lower()
            state_match = candidate.get("state", "").upper() == parsed_name["state"].upper()
            
            total_score = name_score
            if party_match:
                total_score += 10  # Party match bonus
            if state_match:
                total_score += 10  # State match bonus
            
            # Penalty for wrong party/state
            if parsed_name["party"] != "Unknown" and not party_match:
                total_score -= 20
            if parsed_name["state"] != "Unknown" and not state_match:
                total_score -= 20
            
            if total_score > best_score:
                best_score = total_score
                best_match = {
                    "member_id": candidate["id"],
                    "database_name": candidate_full,
                    "database_party": candidate.get("party", ""),
                    "database_state": candidate.get("state", ""),
                    "database_chamber": candidate.get("chamber", ""),
                    "match_score": total_score,
                    "name_similarity": name_score,
                    "party_match": party_match,
                    "state_match": state_match,
                    "candidate_data": candidate
                }
        
        return best_match if best_score > 70 else None  # Threshold for acceptable match
    
    def process_all_wikipedia_names(self) -> Dict[str, Any]:
        """Process all Wikipedia committee leadership names."""
        print("🔍 Phase 2 Step 2.2: Member Name Matching Implementation")
        print("=" * 70)
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "total_names_processed": 0,
            "successful_matches": 0,
            "failed_matches": 0,
            "matches": [],
            "failures": []
        }
        
        print("\n1. Processing Wikipedia Committee Leadership Names...")
        
        for committee in self.wikipedia_data["committees"]:
            committee_name = committee["name"]
            chamber = committee["chamber"]
            
            print(f"\n📋 Processing {committee_name} ({chamber})")
            
            # Process chair
            if "chair" in committee:
                chair_parsed = self.parse_wikipedia_name(committee["chair"])
                chair_match = self.match_member_to_database(chair_parsed)
                
                results["total_names_processed"] += 1
                
                if chair_match:
                    results["successful_matches"] += 1
                    results["matches"].append({
                        "committee": committee_name,
                        "chamber": chamber,
                        "position": "Chair",
                        "wikipedia_name": committee["chair"],
                        "parsed_name": chair_parsed,
                        "match_result": chair_match
                    })
                    print(f"   ✅ Chair: {committee['chair']} → {chair_match['database_name']} (ID: {chair_match['member_id']}, Score: {chair_match['match_score']})")
                else:
                    results["failed_matches"] += 1
                    results["failures"].append({
                        "committee": committee_name,
                        "chamber": chamber,
                        "position": "Chair",
                        "wikipedia_name": committee["chair"],
                        "parsed_name": chair_parsed,
                        "reason": "No suitable match found"
                    })
                    print(f"   ❌ Chair: {committee['chair']} → No match found")
            
            # Process ranking member
            if "ranking_member" in committee:
                ranking_parsed = self.parse_wikipedia_name(committee["ranking_member"])
                ranking_match = self.match_member_to_database(ranking_parsed)
                
                results["total_names_processed"] += 1
                
                if ranking_match:
                    results["successful_matches"] += 1
                    results["matches"].append({
                        "committee": committee_name,
                        "chamber": chamber,
                        "position": "Ranking Member",
                        "wikipedia_name": committee["ranking_member"],
                        "parsed_name": ranking_parsed,
                        "match_result": ranking_match
                    })
                    print(f"   ✅ Ranking: {committee['ranking_member']} → {ranking_match['database_name']} (ID: {ranking_match['member_id']}, Score: {ranking_match['match_score']})")
                else:
                    results["failed_matches"] += 1
                    results["failures"].append({
                        "committee": committee_name,
                        "chamber": chamber,
                        "position": "Ranking Member",
                        "wikipedia_name": committee["ranking_member"],
                        "parsed_name": ranking_parsed,
                        "reason": "No suitable match found"
                    })
                    print(f"   ❌ Ranking: {committee['ranking_member']} → No match found")
        
        # Calculate success rate
        success_rate = (results["successful_matches"] / results["total_names_processed"]) * 100 if results["total_names_processed"] > 0 else 0
        
        print(f"\n📊 Name Matching Results:")
        print(f"   Total names processed: {results['total_names_processed']}")
        print(f"   Successful matches: {results['successful_matches']}")
        print(f"   Failed matches: {results['failed_matches']}")
        print(f"   Success rate: {success_rate:.1f}%")
        
        # Save results
        with open("member_name_matching_results.json", "w") as f:
            json.dump(results, f, indent=2)
        
        print(f"\n✅ Name matching complete! Results saved to member_name_matching_results.json")
        
        return results

if __name__ == "__main__":
    matcher = MemberNameMatcher()
    matcher.process_all_wikipedia_names()