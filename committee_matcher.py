"""
Phase 2 Step 2.3: Committee Matching Implementation
Match Wikipedia committee names with database committee IDs.
"""

import json
import re
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime
from fuzzywuzzy import fuzz

class CommitteeMatcher:
    """Match Wikipedia committee names to database committee IDs."""
    
    def __init__(self):
        self.base_url = "https://congressional-data-api-v2-1066017671167.us-central1.run.app/api/v1"
        self.headers = {
            "User-Agent": "Congressional Data Automator - Committee Matcher",
            "Accept": "application/json"
        }
        
        # Load Wikipedia data
        with open("wikipedia_data.json", "r") as f:
            self.wikipedia_data = json.load(f)
        
        # Load member matching results
        with open("member_name_matching_results.json", "r") as f:
            self.member_matches = json.load(f)
    
    def normalize_committee_name(self, name: str) -> str:
        """
        Normalize committee name for matching.
        """
        # Convert to lowercase
        normalized = name.lower()
        
        # Remove common prefixes
        prefixes_to_remove = [
            "committee on the ",
            "committee on ",
            "select committee on ",
            "permanent select committee on ",
            "special committee on ",
            "joint committee on ",
            "standing committee on "
        ]
        
        for prefix in prefixes_to_remove:
            if normalized.startswith(prefix):
                normalized = normalized[len(prefix):]
                break
        
        # Remove common suffixes
        suffixes_to_remove = [
            " committee",
            " subcommittee",
            " (select)",
            " (special)",
            " (permanent select)",
            " (permanent caucus)"
        ]
        
        for suffix in suffixes_to_remove:
            if normalized.endswith(suffix):
                normalized = normalized[:-len(suffix)]
                break
        
        # Handle special cases
        special_mappings = {
            "aging": "aging (special)",
            "homeland security and governmental affairs": "homeland security and government affairs",
            "small business and entrepreneurship": "small business and entrepreneurship",
            "international narcotics control": "international narcotics control caucus",
            "veterans' affairs": "veterans affairs",
            "science, space and technology": "science, space, and technology",
            "house administration": "administration",
            "oversight and government reform": "oversight and accountability",
            "strategic competition between the united statesand the chinese communist party": "strategic competition between the united states and the chinese communist party"
        }
        
        return special_mappings.get(normalized, normalized)
    
    def search_committee_by_name(self, name: str) -> List[Dict]:
        """Search for committee by name using API."""
        try:
            response = requests.get(
                f"{self.base_url}/committees?search={name}",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Error searching for committee {name}: {e}")
            return []
    
    def calculate_committee_similarity(self, name1: str, name2: str) -> float:
        """Calculate similarity score between two committee names."""
        # Normalize both names
        norm1 = self.normalize_committee_name(name1)
        norm2 = self.normalize_committee_name(name2)
        
        # Use token sort ratio for better matching
        return fuzz.token_sort_ratio(norm1, norm2)
    
    def match_committee_to_database(self, wikipedia_committee: Dict[str, str]) -> Optional[Dict]:
        """
        Match a Wikipedia committee to a database committee.
        """
        wiki_name = wikipedia_committee["name"]
        wiki_chamber = wikipedia_committee["chamber"]
        
        # Search by normalized name
        normalized_name = self.normalize_committee_name(wiki_name)
        candidates = self.search_committee_by_name(normalized_name)
        
        if not candidates:
            # Fallback to search by individual words
            words = wiki_name.split()
            for word in words:
                if len(word) > 3:  # Skip short words
                    candidates = self.search_committee_by_name(word)
                    if candidates:
                        break
        
        if not candidates:
            return None
        
        best_match = None
        best_score = 0
        
        for candidate in candidates:
            # Calculate name similarity
            name_score = self.calculate_committee_similarity(wiki_name, candidate["name"])
            
            # Check chamber match
            chamber_match = candidate.get("chamber", "").lower() == wiki_chamber.lower()
            
            # Check that it's not a subcommittee (we want standing committees)
            is_standing = not candidate.get("is_subcommittee", False)
            
            # Calculate total score
            total_score = name_score
            if chamber_match:
                total_score += 20  # Chamber match bonus
            if is_standing:
                total_score += 10  # Standing committee bonus
            else:
                total_score -= 20  # Subcommittee penalty
            
            # Special handling for Joint committees
            if wiki_chamber == "Joint":
                total_score += 10  # Joint committee bonus
            
            if total_score > best_score:
                best_score = total_score
                best_match = {
                    "committee_id": candidate["id"],
                    "database_name": candidate["name"],
                    "database_chamber": candidate.get("chamber", ""),
                    "is_subcommittee": candidate.get("is_subcommittee", False),
                    "match_score": total_score,
                    "name_similarity": name_score,
                    "chamber_match": chamber_match,
                    "is_standing": is_standing,
                    "candidate_data": candidate
                }
        
        return best_match if best_score > 60 else None  # Threshold for acceptable match
    
    def process_all_wikipedia_committees(self) -> Dict[str, Any]:
        """Process all Wikipedia committees for matching."""
        print("🔍 Phase 2 Step 2.3: Committee Matching Implementation")
        print("=" * 70)
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "total_committees_processed": 0,
            "successful_matches": 0,
            "failed_matches": 0,
            "matches": [],
            "failures": []
        }
        
        print("\n1. Processing Wikipedia Committees...")
        
        for committee in self.wikipedia_data["committees"]:
            committee_name = committee["name"]
            chamber = committee["chamber"]
            
            print(f"\n📋 Processing {committee_name} ({chamber})")
            
            results["total_committees_processed"] += 1
            
            match = self.match_committee_to_database(committee)
            
            if match:
                results["successful_matches"] += 1
                results["matches"].append({
                    "wikipedia_committee": committee,
                    "match_result": match
                })
                print(f"   ✅ {committee_name} → {match['database_name']} (ID: {match['committee_id']}, Score: {match['match_score']})")
            else:
                results["failed_matches"] += 1
                results["failures"].append({
                    "wikipedia_committee": committee,
                    "reason": "No suitable match found"
                })
                print(f"   ❌ {committee_name} → No match found")
        
        # Calculate success rate
        success_rate = (results["successful_matches"] / results["total_committees_processed"]) * 100 if results["total_committees_processed"] > 0 else 0
        
        print(f"\n📊 Committee Matching Results:")
        print(f"   Total committees processed: {results['total_committees_processed']}")
        print(f"   Successful matches: {results['successful_matches']}")
        print(f"   Failed matches: {results['failed_matches']}")
        print(f"   Success rate: {success_rate:.1f}%")
        
        # Show some key matches
        print(f"\n🔍 Key Committee Matches:")
        key_committees = ["Judiciary", "Appropriations", "Armed Services", "Finance", "Commerce"]
        for match in results["matches"]:
            wiki_name = match["wikipedia_committee"]["name"]
            if any(key in wiki_name for key in key_committees):
                chamber = match["wikipedia_committee"]["chamber"]
                db_name = match["match_result"]["database_name"]
                committee_id = match["match_result"]["committee_id"]
                score = match["match_result"]["match_score"]
                print(f"   📋 {wiki_name} ({chamber}) → {db_name} (ID: {committee_id}, Score: {score})")
        
        # Save results
        with open("committee_matching_results.json", "w") as f:
            json.dump(results, f, indent=2)
        
        print(f"\n✅ Committee matching complete! Results saved to committee_matching_results.json")
        
        return results

if __name__ == "__main__":
    matcher = CommitteeMatcher()
    matcher.process_all_wikipedia_committees()