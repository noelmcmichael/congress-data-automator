"""
Phase 2 Step 2.4: Leadership Position Reconciliation
Combine member and committee matches to generate leadership updates.
"""

import json
from typing import Dict, List, Optional, Any
from datetime import datetime

class LeadershipReconciler:
    """Reconcile Wikipedia leadership data with database records."""
    
    def __init__(self):
        # Load Wikipedia data
        with open("wikipedia_data.json", "r") as f:
            self.wikipedia_data = json.load(f)
        
        # Load member matching results
        with open("member_name_matching_results.json", "r") as f:
            self.member_matches = json.load(f)
        
        # Load committee matching results
        with open("committee_matching_results.json", "r") as f:
            self.committee_matches = json.load(f)
    
    def find_member_match(self, committee_name: str, chamber: str, position: str) -> Optional[Dict]:
        """Find member match for a specific committee leadership position."""
        for match in self.member_matches["matches"]:
            if (match["committee"] == committee_name and 
                match["chamber"] == chamber and 
                match["position"] == position):
                return match
        return None
    
    def find_committee_match(self, committee_name: str, chamber: str) -> Optional[Dict]:
        """Find committee match for a specific committee."""
        for match in self.committee_matches["matches"]:
            wiki_committee = match["wikipedia_committee"]
            if (wiki_committee["name"] == committee_name and 
                wiki_committee["chamber"] == chamber):
                return match
        return None
    
    def generate_leadership_updates(self) -> Dict[str, Any]:
        """Generate leadership position updates from reconciliation data."""
        print("🔍 Phase 2 Step 2.4: Leadership Position Reconciliation")
        print("=" * 70)
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "total_committees_processed": 0,
            "successful_reconciliations": 0,
            "failed_reconciliations": 0,
            "leadership_updates": [],
            "reconciliation_failures": [],
            "sql_statements": []
        }
        
        print("\n1. Generating Leadership Position Updates...")
        
        for committee in self.wikipedia_data["committees"]:
            committee_name = committee["name"]
            chamber = committee["chamber"]
            
            print(f"\n📋 Processing {committee_name} ({chamber})")
            
            results["total_committees_processed"] += 1
            
            # Find committee match
            committee_match = self.find_committee_match(committee_name, chamber)
            
            if not committee_match:
                results["failed_reconciliations"] += 1
                results["reconciliation_failures"].append({
                    "committee": committee_name,
                    "chamber": chamber,
                    "reason": "Committee not found in database"
                })
                print(f"   ❌ Committee not found in database")
                continue
            
            committee_id = committee_match["match_result"]["committee_id"]
            database_committee_name = committee_match["match_result"]["database_name"]
            
            # Process chair position
            chair_member_id = None
            chair_update_status = "No chair specified"
            
            if "chair" in committee:
                chair_match = self.find_member_match(committee_name, chamber, "Chair")
                if chair_match:
                    chair_member_id = chair_match["match_result"]["member_id"]
                    chair_name = chair_match["match_result"]["database_name"]
                    chair_update_status = f"Chair: {chair_name} (ID: {chair_member_id})"
                else:
                    chair_update_status = f"Chair not found: {committee['chair']}"
            
            # Process ranking member position
            ranking_member_id = None
            ranking_update_status = "No ranking member specified"
            
            if "ranking_member" in committee:
                ranking_match = self.find_member_match(committee_name, chamber, "Ranking Member")
                if ranking_match:
                    ranking_member_id = ranking_match["match_result"]["member_id"]
                    ranking_name = ranking_match["match_result"]["database_name"]
                    ranking_update_status = f"Ranking: {ranking_name} (ID: {ranking_member_id})"
                else:
                    ranking_update_status = f"Ranking not found: {committee['ranking_member']}"
            
            # Check if we have at least one leadership position
            if chair_member_id or ranking_member_id:
                results["successful_reconciliations"] += 1
                
                # Generate update record
                update_record = {
                    "committee_id": committee_id,
                    "committee_name": committee_name,
                    "database_committee_name": database_committee_name,
                    "chamber": chamber,
                    "chair_member_id": chair_member_id,
                    "ranking_member_id": ranking_member_id,
                    "wikipedia_chair": committee.get("chair", ""),
                    "wikipedia_ranking": committee.get("ranking_member", ""),
                    "chair_update_status": chair_update_status,
                    "ranking_update_status": ranking_update_status,
                    "confidence_score": self._calculate_confidence_score(committee_match, chair_match, ranking_match)
                }
                
                results["leadership_updates"].append(update_record)
                
                # Generate SQL update statement
                sql_parts = []
                if chair_member_id:
                    sql_parts.append(f"chair_member_id = {chair_member_id}")
                if ranking_member_id:
                    sql_parts.append(f"ranking_member_id = {ranking_member_id}")
                
                if sql_parts:
                    sql_statement = f"UPDATE committees SET {', '.join(sql_parts)} WHERE id = {committee_id};"
                    results["sql_statements"].append({
                        "committee_id": committee_id,
                        "committee_name": database_committee_name,
                        "sql": sql_statement,
                        "confidence_score": update_record["confidence_score"]
                    })
                
                print(f"   ✅ {database_committee_name} (ID: {committee_id})")
                print(f"      {chair_update_status}")
                print(f"      {ranking_update_status}")
                print(f"      Confidence: {update_record['confidence_score']}/100")
            else:
                results["failed_reconciliations"] += 1
                results["reconciliation_failures"].append({
                    "committee": committee_name,
                    "chamber": chamber,
                    "reason": "No leadership positions matched"
                })
                print(f"   ❌ No leadership positions matched")
        
        # Calculate success rate
        success_rate = (results["successful_reconciliations"] / results["total_committees_processed"]) * 100 if results["total_committees_processed"] > 0 else 0
        
        print(f"\n📊 Leadership Reconciliation Results:")
        print(f"   Total committees processed: {results['total_committees_processed']}")
        print(f"   Successful reconciliations: {results['successful_reconciliations']}")
        print(f"   Failed reconciliations: {results['failed_reconciliations']}")
        print(f"   Success rate: {success_rate:.1f}%")
        print(f"   SQL statements generated: {len(results['sql_statements'])}")
        
        # Show high-confidence updates
        print(f"\n🔍 High-Confidence Leadership Updates:")
        high_confidence = [update for update in results["leadership_updates"] if update["confidence_score"] >= 90]
        for update in high_confidence[:10]:  # Show first 10
            print(f"   📋 {update['committee_name']} ({update['chamber']})")
            print(f"      {update['chair_update_status']}")
            print(f"      {update['ranking_update_status']}")
            print(f"      Confidence: {update['confidence_score']}/100")
        
        # Save results
        with open("leadership_reconciliation_results.json", "w") as f:
            json.dump(results, f, indent=2)
        
        # Save SQL statements to separate file
        with open("leadership_update_statements.sql", "w") as f:
            f.write("-- Leadership Position Updates Generated from Wikipedia Data\n")
            f.write(f"-- Generated at: {datetime.now().isoformat()}\n")
            f.write(f"-- Total updates: {len(results['sql_statements'])}\n\n")
            
            for stmt in results["sql_statements"]:
                f.write(f"-- {stmt['committee_name']} (Confidence: {stmt['confidence_score']}/100)\n")
                f.write(f"{stmt['sql']}\n\n")
        
        print(f"\n✅ Leadership reconciliation complete!")
        print(f"   📄 Results saved to leadership_reconciliation_results.json")
        print(f"   📄 SQL statements saved to leadership_update_statements.sql")
        
        return results
    
    def _calculate_confidence_score(self, committee_match: Optional[Dict], chair_match: Optional[Dict], ranking_match: Optional[Dict]) -> int:
        """Calculate confidence score for a leadership update."""
        score = 0
        
        # Base score for having a committee match
        if committee_match:
            score += 40
            # Bonus for high committee match score
            if committee_match["match_result"]["match_score"] >= 120:
                score += 10
        
        # Score for chair match
        if chair_match:
            score += 25
            # Bonus for high member match score
            if chair_match["match_result"]["match_score"] >= 120:
                score += 10
        
        # Score for ranking member match
        if ranking_match:
            score += 25
            # Bonus for high member match score
            if ranking_match["match_result"]["match_score"] >= 120:
                score += 10
        
        return min(score, 100)  # Cap at 100

if __name__ == "__main__":
    reconciler = LeadershipReconciler()
    reconciler.generate_leadership_updates()