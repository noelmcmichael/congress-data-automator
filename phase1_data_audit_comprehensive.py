#!/usr/bin/env python3
"""
Phase 1: Comprehensive Data Audit & Gap Analysis
Congressional Data System - 119th Congress

This script performs a systematic audit of our current data against official sources
to identify missing committees, incorrect relationships, and data quality issues.
"""

import json
import requests
from datetime import datetime
from typing import Dict, List, Set, Tuple
import time

class CongressionalDataAuditor:
    def __init__(self, api_base_url: str):
        self.api_base_url = api_base_url
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.audit_results = {
            "timestamp": self.timestamp,
            "phase": "Phase 1 - Data Audit & Gap Analysis",
            "current_data": {},
            "expected_data": {},
            "gaps": {},
            "issues": [],
            "recommendations": []
        }
    
    def fetch_current_data(self) -> Dict:
        """Fetch current system data for audit"""
        print("🔍 Fetching current system data...")
        
        # Get all committees
        committees_response = requests.get(f"{self.api_base_url}/committees")
        committees = committees_response.json()
        
        # Get all members
        members_response = requests.get(f"{self.api_base_url}/members")
        members = members_response.json()
        
        # Organize committees by type and chamber
        committees_by_type = {}
        for committee in committees:
            chamber = committee.get('chamber', 'Unknown')
            committee_type = committee.get('committee_type', 'Unknown')
            
            if chamber not in committees_by_type:
                committees_by_type[chamber] = {}
            if committee_type not in committees_by_type[chamber]:
                committees_by_type[chamber][committee_type] = []
            
            committees_by_type[chamber][committee_type].append({
                'name': committee['name'],
                'id': committee.get('id'),
                'committee_type': committee_type,
                'chamber': chamber
            })
        
        current_data = {
            "total_committees": len(committees),
            "total_members": len(members),
            "committees_by_type": committees_by_type,
            "committee_names": [c['name'] for c in committees],
            "member_count_by_chamber": self._count_members_by_chamber(members)
        }
        
        self.audit_results["current_data"] = current_data
        return current_data
    
    def _count_members_by_chamber(self, members: List[Dict]) -> Dict:
        """Count members by chamber"""
        counts = {"House": 0, "Senate": 0}
        for member in members:
            chamber = member.get('chamber', 'Unknown')
            if chamber in counts:
                counts[chamber] += 1
        return counts
    
    def define_expected_data(self) -> Dict:
        """Define expected data based on official Congressional structure"""
        print("📋 Defining expected data structure...")
        
        # Official Standing Committees for 119th Congress
        expected_house_standing = [
            "Committee on Agriculture",
            "Committee on Appropriations", 
            "Committee on Armed Services",
            "Committee on the Budget",
            "Committee on Education and the Workforce",
            "Committee on Energy and Commerce",
            "Committee on Ethics",
            "Committee on Financial Services",
            "Committee on Foreign Affairs",
            "Committee on Homeland Security",
            "Committee on House Administration",
            "Committee on the Judiciary",
            "Committee on Natural Resources",
            "Committee on Oversight and Accountability",
            "Committee on Rules",
            "Committee on Science, Space, and Technology",
            "Committee on Small Business",
            "Committee on Transportation and Infrastructure",
            "Committee on Veterans' Affairs",
            "Committee on Ways and Means"
        ]
        
        expected_senate_standing = [
            "Committee on Agriculture, Nutrition, and Forestry",
            "Committee on Appropriations",
            "Committee on Armed Services",
            "Committee on Banking, Housing, and Urban Affairs",
            "Committee on the Budget",
            "Committee on Commerce, Science, and Transportation",
            "Committee on Energy and Natural Resources",
            "Committee on Environment and Public Works",
            "Committee on Finance",
            "Committee on Foreign Relations",
            "Committee on Health, Education, Labor, and Pensions",
            "Committee on Homeland Security and Governmental Affairs",
            "Committee on the Judiciary",
            "Committee on Rules and Administration",
            "Committee on Small Business and Entrepreneurship",
            "Committee on Veterans' Affairs"
        ]
        
        expected_joint_committees = [
            "Joint Committee on Printing",
            "Joint Committee on Taxation", 
            "Joint Committee on the Library",
            "Joint Economic Committee"
        ]
        
        expected_special_committees = [
            "Select Committee on Intelligence",
            "Select Committee on Ethics",
            "Special Committee on Aging"
        ]
        
        expected_data = {
            "house_standing_committees": expected_house_standing,
            "senate_standing_committees": expected_senate_standing,
            "joint_committees": expected_joint_committees,
            "special_committees": expected_special_committees,
            "total_expected_standing": len(expected_house_standing) + len(expected_senate_standing),
            "expected_member_counts": {
                "House": 435,  # Official House size
                "Senate": 100  # Official Senate size
            }
        }
        
        self.audit_results["expected_data"] = expected_data
        return expected_data
    
    def identify_gaps(self, current_data: Dict, expected_data: Dict) -> Dict:
        """Identify gaps between current and expected data"""
        print("🔍 Identifying data gaps...")
        
        gaps = {
            "missing_committees": [],
            "incorrect_committee_names": [],
            "member_count_discrepancies": {},
            "committee_type_issues": [],
            "chamber_assignment_issues": []
        }
        
        # Check for missing House standing committees
        current_house_standing = []
        if "House" in current_data["committees_by_type"]:
            if "Standing" in current_data["committees_by_type"]["House"]:
                current_house_standing = [c['name'] for c in current_data["committees_by_type"]["House"]["Standing"]]
        
        missing_house_standing = []
        for expected_committee in expected_data["house_standing_committees"]:
            if expected_committee not in current_house_standing:
                missing_house_standing.append(expected_committee)
        
        # Check for missing Senate standing committees
        current_senate_standing = []
        if "Senate" in current_data["committees_by_type"]:
            if "Standing" in current_data["committees_by_type"]["Senate"]:
                current_senate_standing = [c['name'] for c in current_data["committees_by_type"]["Senate"]["Standing"]]
        
        missing_senate_standing = []
        for expected_committee in expected_data["senate_standing_committees"]:
            if expected_committee not in current_senate_standing:
                missing_senate_standing.append(expected_committee)
        
        # Check joint committees
        current_joint = []
        if "Joint" in current_data["committees_by_type"]:
            if "Standing" in current_data["committees_by_type"]["Joint"]:
                current_joint = [c['name'] for c in current_data["committees_by_type"]["Joint"]["Standing"]]
        
        missing_joint = []
        for expected_committee in expected_data["joint_committees"]:
            if expected_committee not in current_joint:
                missing_joint.append(expected_committee)
        
        gaps["missing_committees"] = {
            "house_standing": missing_house_standing,
            "senate_standing": missing_senate_standing,
            "joint": missing_joint
        }
        
        # Check member counts
        current_counts = current_data["member_count_by_chamber"]
        expected_counts = expected_data["expected_member_counts"]
        
        for chamber in expected_counts:
            if chamber in current_counts:
                if current_counts[chamber] != expected_counts[chamber]:
                    gaps["member_count_discrepancies"][chamber] = {
                        "current": current_counts[chamber],
                        "expected": expected_counts[chamber],
                        "difference": current_counts[chamber] - expected_counts[chamber]
                    }
        
        self.audit_results["gaps"] = gaps
        return gaps
    
    def analyze_data_quality(self, current_data: Dict, gaps: Dict) -> List[str]:
        """Analyze data quality issues and generate recommendations"""
        print("📊 Analyzing data quality issues...")
        
        issues = []
        recommendations = []
        
        # Check for missing committees
        total_missing = (len(gaps["missing_committees"]["house_standing"]) + 
                        len(gaps["missing_committees"]["senate_standing"]) + 
                        len(gaps["missing_committees"]["joint"]))
        
        if total_missing > 0:
            issues.append(f"Missing {total_missing} official committees")
            recommendations.append("Implement authoritative data collection from official sources")
        
        # Check member count discrepancies
        if gaps["member_count_discrepancies"]:
            for chamber, discrepancy in gaps["member_count_discrepancies"].items():
                issues.append(f"{chamber} member count: {discrepancy['current']} vs expected {discrepancy['expected']}")
                if discrepancy['difference'] > 0:
                    recommendations.append(f"Remove {discrepancy['difference']} duplicate {chamber} members")
                else:
                    recommendations.append(f"Add {abs(discrepancy['difference'])} missing {chamber} members")
        
        # Check committee structure
        if current_data["total_committees"] < 100:
            issues.append("Committee count suspiciously low - likely missing subcommittees")
            recommendations.append("Implement comprehensive committee structure including subcommittees")
        
        # Check for committee-member relationships
        issues.append("Committee-member relationships not verified against official sources")
        recommendations.append("Rebuild committee-member relationships from authoritative data")
        
        self.audit_results["issues"] = issues
        self.audit_results["recommendations"] = recommendations
        
        return issues, recommendations
    
    def generate_audit_report(self) -> Dict:
        """Generate comprehensive audit report"""
        print("📄 Generating audit report...")
        
        current_data = self.fetch_current_data()
        expected_data = self.define_expected_data()
        gaps = self.identify_gaps(current_data, expected_data)
        issues, recommendations = self.analyze_data_quality(current_data, gaps)
        
        # Calculate data quality score
        total_expected_committees = expected_data["total_expected_standing"] + len(expected_data["joint_committees"])
        missing_committees = sum(len(v) for v in gaps["missing_committees"].values())
        committee_completeness = ((total_expected_committees - missing_committees) / total_expected_committees) * 100
        
        # Member completeness
        member_completeness = 0
        for chamber, expected_count in expected_data["expected_member_counts"].items():
            if chamber in current_data["member_count_by_chamber"]:
                current_count = current_data["member_count_by_chamber"][chamber]
                completeness = min(current_count / expected_count, 1.0) * 100
                member_completeness += completeness
        member_completeness = member_completeness / len(expected_data["expected_member_counts"])
        
        overall_score = (committee_completeness + member_completeness) / 2
        
        self.audit_results["quality_metrics"] = {
            "committee_completeness": round(committee_completeness, 1),
            "member_completeness": round(member_completeness, 1),
            "overall_data_quality": round(overall_score, 1),
            "critical_issues": len([i for i in issues if "missing" in i.lower() or "duplicate" in i.lower()]),
            "total_issues": len(issues)
        }
        
        # Summary
        self.audit_results["summary"] = {
            "status": "CRITICAL" if overall_score < 80 else "WARNING" if overall_score < 95 else "GOOD",
            "primary_concern": "Committee-member relationships not verified",
            "immediate_action_required": overall_score < 80,
            "next_phase": "Phase 2 - Authoritative Data Collection"
        }
        
        return self.audit_results
    
    def save_audit_report(self, filename: str = None):
        """Save audit report to file"""
        if filename is None:
            filename = f"data_audit_report_{self.timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.audit_results, f, indent=2)
        
        print(f"📄 Audit report saved to {filename}")
        return filename

def main():
    """Execute Phase 1 data audit"""
    print("🚀 Starting Phase 1: Data Audit & Gap Analysis")
    print("=" * 60)
    
    # Initialize auditor
    api_base_url = "https://congressional-data-api-v3-1066017671167.us-central1.run.app/api/v1"
    auditor = CongressionalDataAuditor(api_base_url)
    
    # Run comprehensive audit
    try:
        audit_report = auditor.generate_audit_report()
        filename = auditor.save_audit_report()
        
        # Print summary
        print("\n📋 AUDIT SUMMARY")
        print("=" * 40)
        print(f"Overall Data Quality: {audit_report['quality_metrics']['overall_data_quality']}%")
        print(f"Status: {audit_report['summary']['status']}")
        print(f"Critical Issues: {audit_report['quality_metrics']['critical_issues']}")
        print(f"Total Issues: {audit_report['quality_metrics']['total_issues']}")
        
        print("\n🔍 KEY FINDINGS")
        print("-" * 20)
        for issue in audit_report['issues'][:5]:  # Show top 5 issues
            print(f"• {issue}")
        
        print("\n💡 RECOMMENDATIONS")
        print("-" * 20)
        for rec in audit_report['recommendations'][:3]:  # Show top 3 recommendations
            print(f"• {rec}")
        
        print(f"\n📄 Full report saved to: {filename}")
        print(f"Next Step: {audit_report['summary']['next_phase']}")
        
        if audit_report['summary']['immediate_action_required']:
            print("\n⚠️  IMMEDIATE ACTION REQUIRED")
            print("Data quality below acceptable threshold. Proceeding to Phase 2...")
            return True
        else:
            print("\n✅ Data quality acceptable. Manual review recommended.")
            return False
            
    except Exception as e:
        print(f"❌ Audit failed: {str(e)}")
        return False

if __name__ == "__main__":
    needs_remediation = main()
    if needs_remediation:
        print("\n🔄 Ready for Phase 2: Authoritative Data Collection")
    else:
        print("\n✅ Phase 1 Complete. Review audit report before proceeding.")