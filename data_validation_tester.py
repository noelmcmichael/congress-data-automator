"""
Phase 2 Step 2.5: Data Validation & Testing
Validate reconciliation results and test update logic.
"""

import json
from typing import Dict, List, Optional, Any
from datetime import datetime
import requests

class DataValidationTester:
    """Validate reconciliation results and test update logic."""
    
    def __init__(self):
        self.base_url = "https://congressional-data-api-v2-1066017671167.us-central1.run.app/api/v1"
        self.headers = {
            "User-Agent": "Congressional Data Automator - Data Validation",
            "Accept": "application/json"
        }
        
        # Load all reconciliation results
        with open("wikipedia_data.json", "r") as f:
            self.wikipedia_data = json.load(f)
        
        with open("member_name_matching_results.json", "r") as f:
            self.member_matches = json.load(f)
        
        with open("committee_matching_results.json", "r") as f:
            self.committee_matches = json.load(f)
        
        with open("leadership_reconciliation_results.json", "r") as f:
            self.leadership_results = json.load(f)
    
    def validate_member_matches(self) -> Dict[str, Any]:
        """Validate member name matching accuracy."""
        print("🔍 Validating Member Name Matches...")
        
        validation_results = {
            "total_matches": len(self.member_matches["matches"]),
            "high_confidence_matches": 0,
            "medium_confidence_matches": 0,
            "low_confidence_matches": 0,
            "validation_errors": []
        }
        
        for match in self.member_matches["matches"]:
            score = match["match_result"]["match_score"]
            
            if score >= 120:
                validation_results["high_confidence_matches"] += 1
            elif score >= 100:
                validation_results["medium_confidence_matches"] += 1
            else:
                validation_results["low_confidence_matches"] += 1
            
            # Validate party and state consistency
            wiki_party = match["parsed_name"]["party"]
            db_party = match["match_result"]["database_party"]
            wiki_state = match["parsed_name"]["state"]
            db_state = match["match_result"]["database_state"]
            
            if wiki_party != "Unknown" and wiki_party != db_party:
                validation_results["validation_errors"].append({
                    "type": "party_mismatch",
                    "wikipedia_name": match["wikipedia_name"],
                    "expected_party": wiki_party,
                    "database_party": db_party
                })
            
            if wiki_state != "Unknown" and wiki_state != db_state:
                validation_results["validation_errors"].append({
                    "type": "state_mismatch",
                    "wikipedia_name": match["wikipedia_name"],
                    "expected_state": wiki_state,
                    "database_state": db_state
                })
        
        print(f"   ✅ Total matches: {validation_results['total_matches']}")
        print(f"   ✅ High confidence (120+): {validation_results['high_confidence_matches']}")
        print(f"   ✅ Medium confidence (100-119): {validation_results['medium_confidence_matches']}")
        print(f"   ✅ Low confidence (<100): {validation_results['low_confidence_matches']}")
        print(f"   ⚠️  Validation errors: {len(validation_results['validation_errors'])}")
        
        return validation_results
    
    def validate_committee_matches(self) -> Dict[str, Any]:
        """Validate committee name matching accuracy."""
        print("\n🔍 Validating Committee Name Matches...")
        
        validation_results = {
            "total_matches": len(self.committee_matches["matches"]),
            "perfect_matches": 0,
            "good_matches": 0,
            "acceptable_matches": 0,
            "chamber_mismatches": []
        }
        
        for match in self.committee_matches["matches"]:
            score = match["match_result"]["match_score"]
            
            if score >= 130:
                validation_results["perfect_matches"] += 1
            elif score >= 100:
                validation_results["good_matches"] += 1
            else:
                validation_results["acceptable_matches"] += 1
            
            # Validate chamber consistency
            wiki_chamber = match["wikipedia_committee"]["chamber"]
            db_chamber = match["match_result"]["database_chamber"]
            
            if wiki_chamber != db_chamber:
                validation_results["chamber_mismatches"].append({
                    "wikipedia_committee": match["wikipedia_committee"]["name"],
                    "expected_chamber": wiki_chamber,
                    "database_chamber": db_chamber
                })
        
        print(f"   ✅ Total matches: {validation_results['total_matches']}")
        print(f"   ✅ Perfect matches (130+): {validation_results['perfect_matches']}")
        print(f"   ✅ Good matches (100-129): {validation_results['good_matches']}")
        print(f"   ✅ Acceptable matches (<100): {validation_results['acceptable_matches']}")
        print(f"   ⚠️  Chamber mismatches: {len(validation_results['chamber_mismatches'])}")
        
        return validation_results
    
    def validate_leadership_updates(self) -> Dict[str, Any]:
        """Validate leadership position updates."""
        print("\n🔍 Validating Leadership Position Updates...")
        
        validation_results = {
            "total_updates": len(self.leadership_results["leadership_updates"]),
            "high_confidence_updates": 0,
            "medium_confidence_updates": 0,
            "low_confidence_updates": 0,
            "critical_committees_updated": 0,
            "critical_committees": []
        }
        
        # Define critical committees to validate
        critical_committee_names = [
            "Judiciary", "Appropriations", "Armed Services", "Finance", 
            "Commerce", "Foreign Relations", "Energy and Commerce", "Ways and Means"
        ]
        
        for update in self.leadership_results["leadership_updates"]:
            confidence = update["confidence_score"]
            
            if confidence >= 90:
                validation_results["high_confidence_updates"] += 1
            elif confidence >= 70:
                validation_results["medium_confidence_updates"] += 1
            else:
                validation_results["low_confidence_updates"] += 1
            
            # Check if this is a critical committee
            committee_name = update["committee_name"]
            if any(critical in committee_name for critical in critical_committee_names):
                validation_results["critical_committees_updated"] += 1
                validation_results["critical_committees"].append({
                    "committee": committee_name,
                    "chamber": update["chamber"],
                    "chair_id": update["chair_member_id"],
                    "ranking_id": update["ranking_member_id"],
                    "confidence": confidence
                })
        
        print(f"   ✅ Total updates: {validation_results['total_updates']}")
        print(f"   ✅ High confidence (90+): {validation_results['high_confidence_updates']}")
        print(f"   ✅ Medium confidence (70-89): {validation_results['medium_confidence_updates']}")
        print(f"   ✅ Low confidence (<70): {validation_results['low_confidence_updates']}")
        print(f"   ✅ Critical committees updated: {validation_results['critical_committees_updated']}")
        
        return validation_results
    
    def test_sql_statement_syntax(self) -> Dict[str, Any]:
        """Test SQL statement syntax and structure."""
        print("\n🔍 Testing SQL Statement Syntax...")
        
        test_results = {
            "total_statements": len(self.leadership_results["sql_statements"]),
            "syntax_valid": 0,
            "syntax_errors": [],
            "sample_validations": []
        }
        
        for stmt in self.leadership_results["sql_statements"]:
            sql = stmt["sql"]
            
            # Basic syntax validation
            if (sql.startswith("UPDATE committees SET") and 
                sql.endswith(";") and 
                "WHERE id =" in sql):
                test_results["syntax_valid"] += 1
                
                # Sample validation for first few statements
                if len(test_results["sample_validations"]) < 5:
                    test_results["sample_validations"].append({
                        "committee": stmt["committee_name"],
                        "sql": sql,
                        "confidence": stmt["confidence_score"],
                        "status": "✅ Valid"
                    })
            else:
                test_results["syntax_errors"].append({
                    "committee": stmt["committee_name"],
                    "sql": sql,
                    "error": "Invalid SQL syntax"
                })
        
        print(f"   ✅ Total statements: {test_results['total_statements']}")
        print(f"   ✅ Syntax valid: {test_results['syntax_valid']}")
        print(f"   ❌ Syntax errors: {len(test_results['syntax_errors'])}")
        
        return test_results
    
    def dry_run_validation(self) -> Dict[str, Any]:
        """Perform dry run validation of the reconciliation process."""
        print("\n🔍 Performing Dry Run Validation...")
        
        dry_run_results = {
            "wikipedia_committees": len(self.wikipedia_data["committees"]),
            "member_matches": self.member_matches["successful_matches"],
            "committee_matches": self.committee_matches["successful_matches"],
            "leadership_updates": self.leadership_results["successful_reconciliations"],
            "sql_statements": len(self.leadership_results["sql_statements"]),
            "pipeline_integrity": True,
            "pipeline_errors": []
        }
        
        # Check pipeline integrity
        if dry_run_results["member_matches"] == 0:
            dry_run_results["pipeline_integrity"] = False
            dry_run_results["pipeline_errors"].append("No member matches found")
        
        if dry_run_results["committee_matches"] == 0:
            dry_run_results["pipeline_integrity"] = False
            dry_run_results["pipeline_errors"].append("No committee matches found")
        
        if dry_run_results["leadership_updates"] == 0:
            dry_run_results["pipeline_integrity"] = False
            dry_run_results["pipeline_errors"].append("No leadership updates generated")
        
        # Test key leadership positions
        key_positions = [
            {"name": "Chuck Grassley", "expected_role": "Senate Judiciary Chair"},
            {"name": "Ted Cruz", "expected_role": "Senate Commerce Chair"},
            {"name": "Susan Collins", "expected_role": "Senate Appropriations Chair"}
        ]
        
        verified_positions = []
        for position in key_positions:
            # Find if this position was successfully reconciled
            for update in self.leadership_results["leadership_updates"]:
                if (position["name"] in update.get("chair_update_status", "") and 
                    update["confidence_score"] >= 90):
                    verified_positions.append({
                        "name": position["name"],
                        "role": position["expected_role"],
                        "committee": update["committee_name"],
                        "confidence": update["confidence_score"]
                    })
                    break
        
        dry_run_results["verified_key_positions"] = verified_positions
        
        print(f"   ✅ Pipeline integrity: {dry_run_results['pipeline_integrity']}")
        print(f"   ✅ Wikipedia committees: {dry_run_results['wikipedia_committees']}")
        print(f"   ✅ Member matches: {dry_run_results['member_matches']}")
        print(f"   ✅ Committee matches: {dry_run_results['committee_matches']}")
        print(f"   ✅ Leadership updates: {dry_run_results['leadership_updates']}")
        print(f"   ✅ SQL statements: {dry_run_results['sql_statements']}")
        print(f"   ✅ Key positions verified: {len(verified_positions)}")
        
        return dry_run_results
    
    def run_comprehensive_validation(self) -> Dict[str, Any]:
        """Run comprehensive validation of all reconciliation data."""
        print("🔍 Phase 2 Step 2.5: Data Validation & Testing")
        print("=" * 70)
        
        validation_results = {
            "timestamp": datetime.now().isoformat(),
            "member_validation": self.validate_member_matches(),
            "committee_validation": self.validate_committee_matches(),
            "leadership_validation": self.validate_leadership_updates(),
            "sql_validation": self.test_sql_statement_syntax(),
            "dry_run_validation": self.dry_run_validation()
        }
        
        # Calculate overall success metrics
        overall_success = (
            validation_results["member_validation"]["total_matches"] > 0 and
            validation_results["committee_validation"]["total_matches"] > 0 and
            validation_results["leadership_validation"]["total_updates"] > 0 and
            validation_results["sql_validation"]["syntax_valid"] > 0 and
            validation_results["dry_run_validation"]["pipeline_integrity"]
        )
        
        validation_results["overall_success"] = overall_success
        
        print(f"\n📊 Overall Validation Results:")
        print(f"   ✅ Member matching: {validation_results['member_validation']['total_matches']} matches")
        print(f"   ✅ Committee matching: {validation_results['committee_validation']['total_matches']} matches")
        print(f"   ✅ Leadership updates: {validation_results['leadership_validation']['total_updates']} updates")
        print(f"   ✅ SQL statements: {validation_results['sql_validation']['syntax_valid']} valid")
        print(f"   ✅ Pipeline integrity: {validation_results['dry_run_validation']['pipeline_integrity']}")
        print(f"   ✅ Overall success: {overall_success}")
        
        # Save validation results
        with open("phase2_validation_results.json", "w") as f:
            json.dump(validation_results, f, indent=2)
        
        print(f"\n✅ Validation complete! Results saved to phase2_validation_results.json")
        
        return validation_results

if __name__ == "__main__":
    tester = DataValidationTester()
    tester.run_comprehensive_validation()