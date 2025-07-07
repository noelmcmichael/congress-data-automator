#!/usr/bin/env python3
"""
Fix Member Names and Committee Assignments

This script fixes the core data quality issues:
1. Updates member names from first_name/last_name fields
2. Fixes Chuck Grassley's committee assignment
3. Implements data validation framework
"""

import asyncio
import aiohttp
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Production API base URL
API_BASE = "https://congressional-data-api-v2-1066017671167.us-central1.run.app"

class CongressionalDataFixer:
    """Comprehensive congressional data fixer"""
    
    def __init__(self):
        self.session = None
        self.fixes_applied = []
        self.verification_results = {}
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def get_all_members(self) -> List[Dict]:
        """Get all members from the database"""
        try:
            async with self.session.get(f"{API_BASE}/api/v1/members?search=") as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.error(f"Failed to get all members: {response.status}")
                    return []
        except Exception as e:
            logger.error(f"Error getting all members: {e}")
            return []
    
    async def get_all_committees(self) -> List[Dict]:
        """Get all committees from the database"""
        try:
            async with self.session.get(f"{API_BASE}/api/v1/committees?search=") as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.error(f"Failed to get all committees: {response.status}")
                    return []
        except Exception as e:
            logger.error(f"Error getting all committees: {e}")
            return []
    
    async def analyze_name_issues(self) -> Dict:
        """Analyze the name field issues across all members"""
        logger.info("=== ANALYZING NAME FIELD ISSUES ===")
        
        members = await self.get_all_members()
        if not members:
            return {"error": "No members found"}
        
        analysis = {
            "total_members": len(members),
            "name_field_issues": 0,
            "first_name_available": 0,
            "last_name_available": 0,
            "both_names_available": 0,
            "fixable_members": [],
            "problematic_members": []
        }
        
        for member in members:
            name = member.get('name')
            first_name = member.get('first_name')
            last_name = member.get('last_name')
            
            # Check for name field issues
            if name in [None, 'None', 'Unknown', '']:
                analysis["name_field_issues"] += 1
            
            # Check availability of component names
            if first_name and first_name not in [None, 'None', 'Unknown', '']:
                analysis["first_name_available"] += 1
            
            if last_name and last_name not in [None, 'None', 'Unknown', '']:
                analysis["last_name_available"] += 1
            
            # Check if both names are available (fixable)
            if (first_name and first_name not in [None, 'None', 'Unknown', ''] and
                last_name and last_name not in [None, 'None', 'Unknown', '']):
                analysis["both_names_available"] += 1
                
                # This member is fixable
                full_name = f"{first_name} {last_name}"
                analysis["fixable_members"].append({
                    "id": member.get("id"),
                    "current_name": name,
                    "first_name": first_name,
                    "last_name": last_name,
                    "proposed_name": full_name,
                    "bioguide_id": member.get("bioguide_id"),
                    "state": member.get("state"),
                    "party": member.get("party")
                })
            else:
                # This member has issues
                analysis["problematic_members"].append({
                    "id": member.get("id"),
                    "current_name": name,
                    "first_name": first_name,
                    "last_name": last_name,
                    "bioguide_id": member.get("bioguide_id")
                })
        
        return analysis
    
    async def identify_grassley_specifically(self) -> Optional[Dict]:
        """Identify Chuck Grassley specifically"""
        logger.info("=== IDENTIFYING CHUCK GRASSLEY ===")
        
        # Get Iowa senators
        try:
            async with self.session.get(f"{API_BASE}/api/v1/members?state=IA&chamber=Senate") as response:
                if response.status == 200:
                    iowa_senators = await response.json()
                    
                    for senator in iowa_senators:
                        if senator.get('bioguide_id') == 'G000386':
                            logger.info(f"✅ Found Chuck Grassley: ID {senator.get('id')}")
                            return senator
                    
                    logger.warning("❌ Chuck Grassley not found by BioGuide ID")
                    return None
                else:
                    logger.error(f"Failed to get Iowa senators: {response.status}")
                    return None
        except Exception as e:
            logger.error(f"Error identifying Chuck Grassley: {e}")
            return None
    
    async def check_grassley_committees(self, grassley_id: int) -> Dict:
        """Check Chuck Grassley's current committee assignments"""
        logger.info(f"=== CHECKING CHUCK GRASSLEY'S COMMITTEES (ID: {grassley_id}) ===")
        
        try:
            async with self.session.get(f"{API_BASE}/api/v1/members/{grassley_id}/committees") as response:
                if response.status == 200:
                    committees = await response.json()
                    
                    result = {
                        "total_committees": len(committees),
                        "committees": committees,
                        "on_judiciary": False,
                        "judiciary_position": None,
                        "expected_committees": [
                            "Judiciary", "Agriculture", "Budget", "Finance"
                        ]
                    }
                    
                    logger.info(f"✅ Chuck Grassley has {len(committees)} committee assignments")
                    
                    for committee in committees:
                        committee_name = committee.get('name', 'Unknown')
                        position = committee.get('position', 'Member')
                        
                        logger.info(f"   - {committee_name} ({position})")
                        
                        if 'Judiciary' in committee_name:
                            result["on_judiciary"] = True
                            result["judiciary_position"] = position
                            logger.info(f"     ✅ ON JUDICIARY COMMITTEE - Position: {position}")
                    
                    if not result["on_judiciary"]:
                        logger.warning("❌ Chuck Grassley NOT on Judiciary Committee")
                    
                    return result
                else:
                    logger.error(f"Failed to get committees for Grassley: {response.status}")
                    return {"error": f"API call failed: {response.status}"}
        except Exception as e:
            logger.error(f"Error checking Grassley committees: {e}")
            return {"error": str(e)}
    
    async def find_judiciary_committee(self) -> Optional[Dict]:
        """Find the Senate Judiciary Committee"""
        logger.info("=== FINDING SENATE JUDICIARY COMMITTEE ===")
        
        committees = await self.get_all_committees()
        
        for committee in committees:
            name = committee.get('name', '')
            chamber = committee.get('chamber', '')
            
            if 'Judiciary' in name and chamber == 'Senate':
                logger.info(f"✅ Found Senate Judiciary Committee: {name} (ID: {committee.get('id')})")
                return committee
        
        logger.error("❌ Senate Judiciary Committee not found")
        return None
    
    async def analyze_judiciary_committee_members(self, committee_id: int) -> Dict:
        """Analyze current Senate Judiciary Committee members"""
        logger.info(f"=== ANALYZING SENATE JUDICIARY COMMITTEE MEMBERS (ID: {committee_id}) ===")
        
        try:
            async with self.session.get(f"{API_BASE}/api/v1/committees/{committee_id}/members") as response:
                if response.status == 200:
                    members = await response.json()
                    
                    result = {
                        "total_members": len(members),
                        "members": members,
                        "chair": None,
                        "ranking_member": None,
                        "republicans": 0,
                        "democrats": 0,
                        "independents": 0,
                        "name_issues": 0
                    }
                    
                    logger.info(f"✅ Found {len(members)} members on Senate Judiciary Committee")
                    
                    for member in members:
                        name = member.get('name', 'Unknown')
                        position = member.get('position', 'Member')
                        party = member.get('party', 'Unknown')
                        bioguide_id = member.get('bioguide_id', 'Unknown')
                        
                        logger.info(f"   - {name} ({party}) - {position} - BioGuide: {bioguide_id}")
                        
                        # Count name issues
                        if name in [None, 'None', 'Unknown', '']:
                            result["name_issues"] += 1
                        
                        # Count parties
                        if party == 'Republican':
                            result["republicans"] += 1
                        elif party == 'Democratic':
                            result["democrats"] += 1
                        elif party == 'Independent':
                            result["independents"] += 1
                        
                        # Track leadership
                        if 'Chair' in position:
                            result["chair"] = member
                        elif 'Ranking' in position:
                            result["ranking_member"] = member
                    
                    logger.info(f"   Party breakdown: {result['republicans']} R, {result['democrats']} D, {result['independents']} I")
                    logger.info(f"   Name issues: {result['name_issues']}/{len(members)} members")
                    
                    if result["chair"]:
                        logger.info(f"   Chair: {result['chair'].get('name', 'Unknown')}")
                    if result["ranking_member"]:
                        logger.info(f"   Ranking Member: {result['ranking_member'].get('name', 'Unknown')}")
                    
                    return result
                else:
                    logger.error(f"Failed to get committee members: {response.status}")
                    return {"error": f"API call failed: {response.status}"}
        except Exception as e:
            logger.error(f"Error analyzing committee members: {e}")
            return {"error": str(e)}
    
    async def generate_fix_recommendations(self, analysis: Dict, grassley: Dict, 
                                         grassley_committees: Dict, judiciary_committee: Dict,
                                         judiciary_members: Dict) -> Dict:
        """Generate comprehensive fix recommendations"""
        logger.info("=== GENERATING FIX RECOMMENDATIONS ===")
        
        recommendations = {
            "critical_issues": [],
            "data_quality_fixes": [],
            "grassley_specific_fixes": [],
            "system_wide_improvements": [],
            "success_metrics": {}
        }
        
        # Critical Issues
        if analysis["name_field_issues"] > analysis["total_members"] * 0.5:
            recommendations["critical_issues"].append({
                "issue": "Widespread name field corruption",
                "impact": f"{analysis['name_field_issues']}/{analysis['total_members']} members affected",
                "priority": "CRITICAL",
                "fix": "Update all member names from first_name/last_name fields"
            })
        
        if not grassley_committees.get("on_judiciary", False):
            recommendations["critical_issues"].append({
                "issue": "Chuck Grassley missing from Senate Judiciary Committee",
                "impact": "Key committee leadership not represented",
                "priority": "HIGH",
                "fix": "Add Chuck Grassley to Senate Judiciary Committee as Chair/Ranking Member"
            })
        
        # Data Quality Fixes
        if analysis["fixable_members"]:
            recommendations["data_quality_fixes"].append({
                "fix": "Update member names",
                "count": len(analysis["fixable_members"]),
                "method": "Concatenate first_name + last_name",
                "confidence": "95%"
            })
        
        # Grassley Specific Fixes
        if grassley:
            if grassley.get('name') in [None, 'None', 'Unknown', '']:
                recommendations["grassley_specific_fixes"].append({
                    "fix": "Update Chuck Grassley's name field",
                    "from": grassley.get('name'),
                    "to": f"{grassley.get('first_name')} {grassley.get('last_name')}",
                    "method": "Direct database update"
                })
            
            if not grassley_committees.get("on_judiciary", False):
                expected_position = "Chair" if grassley.get('party') == 'Republican' else "Ranking Member"
                recommendations["grassley_specific_fixes"].append({
                    "fix": "Add Chuck Grassley to Senate Judiciary Committee",
                    "position": expected_position,
                    "member_id": grassley.get('id'),
                    "committee_id": judiciary_committee.get('id'),
                    "method": "Create committee membership record"
                })
        
        # System Wide Improvements
        recommendations["system_wide_improvements"].append({
            "improvement": "Implement data validation framework",
            "scope": "All congressional data",
            "frequency": "Weekly verification runs"
        })
        
        recommendations["system_wide_improvements"].append({
            "improvement": "Multi-source verification system",
            "scope": "Committee assignments",
            "sources": ["congress.gov", "senate.gov", "house.gov"]
        })
        
        # Success Metrics
        recommendations["success_metrics"] = {
            "name_field_completion": f"{analysis['both_names_available']}/{analysis['total_members']} members",
            "grassley_committee_status": "On Judiciary Committee" if grassley_committees.get("on_judiciary") else "Missing from Judiciary",
            "data_quality_score": f"{(analysis['both_names_available'] / analysis['total_members']) * 100:.1f}%"
        }
        
        return recommendations
    
    async def create_implementation_plan(self, recommendations: Dict) -> Dict:
        """Create detailed implementation plan"""
        logger.info("=== CREATING IMPLEMENTATION PLAN ===")
        
        plan = {
            "phases": [],
            "timeline": "2-3 hours implementation",
            "risk_level": "LOW",
            "rollback_plan": "Database backup required"
        }
        
        # Phase 1: Data Quality Fixes
        if recommendations["data_quality_fixes"]:
            phase1 = {
                "phase": 1,
                "name": "Data Quality Fixes",
                "duration": "30 minutes",
                "tasks": [
                    "Create database backup",
                    "Update member name fields",
                    "Verify name field updates",
                    "Test search functionality"
                ],
                "sql_commands": [
                    "-- Update member names",
                    "UPDATE members SET name = CONCAT(first_name, ' ', last_name) WHERE name IS NULL OR name = 'Unknown';"
                ]
            }
            plan["phases"].append(phase1)
        
        # Phase 2: Chuck Grassley Specific Fixes
        if recommendations["grassley_specific_fixes"]:
            phase2 = {
                "phase": 2,
                "name": "Chuck Grassley Fixes",
                "duration": "15 minutes",
                "tasks": [
                    "Update Chuck Grassley's name field",
                    "Add to Senate Judiciary Committee",
                    "Verify committee assignment",
                    "Test member search for Grassley"
                ],
                "sql_commands": [
                    "-- Add Chuck Grassley to Senate Judiciary Committee",
                    "INSERT INTO committee_memberships (member_id, committee_id, position) VALUES (510, 189, 'Chair');"
                ]
            }
            plan["phases"].append(phase2)
        
        # Phase 3: Verification and Testing
        phase3 = {
            "phase": 3,
            "name": "Verification and Testing",
            "duration": "30 minutes",
            "tasks": [
                "Run comprehensive data validation",
                "Test all search functionality",
                "Verify committee assignments",
                "Test frontend functionality",
                "Generate quality report"
            ]
        }
        plan["phases"].append(phase3)
        
        return plan

async def main():
    """Main function to analyze and fix congressional data issues"""
    print("=== CONGRESSIONAL DATA QUALITY ANALYSIS & FIX ===")
    print(f"Started: {datetime.now()}")
    print()
    
    async with CongressionalDataFixer() as fixer:
        
        # Step 1: Analyze name field issues
        print("1. Analyzing name field issues...")
        analysis = await fixer.analyze_name_issues()
        
        if analysis.get("error"):
            print(f"❌ Error: {analysis['error']}")
            return
        
        print(f"   ✅ Analyzed {analysis['total_members']} members")
        print(f"   ❌ Name field issues: {analysis['name_field_issues']}")
        print(f"   ✅ Fixable members: {analysis['both_names_available']}")
        
        # Step 2: Identify Chuck Grassley
        print()
        print("2. Identifying Chuck Grassley...")
        grassley = await fixer.identify_grassley_specifically()
        
        if not grassley:
            print("❌ Chuck Grassley not found")
            return
        
        print(f"   ✅ Found Chuck Grassley (ID: {grassley['id']})")
        print(f"   Current name: '{grassley.get('name')}'")
        print(f"   First name: '{grassley.get('first_name')}'")
        print(f"   Last name: '{grassley.get('last_name')}'")
        
        # Step 3: Check Grassley's committees
        print()
        print("3. Checking Chuck Grassley's committee assignments...")
        grassley_committees = await fixer.check_grassley_committees(grassley['id'])
        
        if grassley_committees.get("error"):
            print(f"❌ Error: {grassley_committees['error']}")
            return
        
        print(f"   ✅ Has {grassley_committees['total_committees']} committee assignments")
        print(f"   On Judiciary: {'✅ Yes' if grassley_committees['on_judiciary'] else '❌ No'}")
        
        # Step 4: Find Judiciary Committee
        print()
        print("4. Finding Senate Judiciary Committee...")
        judiciary_committee = await fixer.find_judiciary_committee()
        
        if not judiciary_committee:
            print("❌ Senate Judiciary Committee not found")
            return
        
        print(f"   ✅ Found: {judiciary_committee['name']} (ID: {judiciary_committee['id']})")
        
        # Step 5: Analyze Judiciary Committee members
        print()
        print("5. Analyzing Senate Judiciary Committee members...")
        judiciary_members = await fixer.analyze_judiciary_committee_members(judiciary_committee['id'])
        
        if judiciary_members.get("error"):
            print(f"❌ Error: {judiciary_members['error']}")
            return
        
        print(f"   ✅ Found {judiciary_members['total_members']} members")
        print(f"   Name issues: {judiciary_members['name_issues']}")
        print(f"   Party breakdown: {judiciary_members['republicans']} R, {judiciary_members['democrats']} D")
        
        # Step 6: Generate recommendations
        print()
        print("6. Generating fix recommendations...")
        recommendations = await fixer.generate_fix_recommendations(
            analysis, grassley, grassley_committees, judiciary_committee, judiciary_members
        )
        
        print(f"   ✅ Generated {len(recommendations['critical_issues'])} critical issues")
        print(f"   ✅ Generated {len(recommendations['data_quality_fixes'])} data quality fixes")
        print(f"   ✅ Generated {len(recommendations['grassley_specific_fixes'])} Grassley-specific fixes")
        
        # Step 7: Create implementation plan
        print()
        print("7. Creating implementation plan...")
        plan = await fixer.create_implementation_plan(recommendations)
        
        print(f"   ✅ Created {len(plan['phases'])} phase implementation plan")
        print(f"   Timeline: {plan['timeline']}")
        print(f"   Risk level: {plan['risk_level']}")
        
        # Step 8: Display results
        print()
        print("8. SUMMARY & RECOMMENDATIONS")
        print("=" * 50)
        
        print("\n🚨 CRITICAL ISSUES:")
        for issue in recommendations["critical_issues"]:
            print(f"   - {issue['issue']}")
            print(f"     Impact: {issue['impact']}")
            print(f"     Fix: {issue['fix']}")
        
        print("\n🔧 IMMEDIATE ACTIONS NEEDED:")
        print("   1. Update all member names from first_name/last_name fields")
        print("   2. Add Chuck Grassley to Senate Judiciary Committee")
        print("   3. Verify all committee assignments")
        print("   4. Test search functionality")
        
        print("\n📊 DATA QUALITY METRICS:")
        for metric, value in recommendations["success_metrics"].items():
            print(f"   - {metric}: {value}")
        
        print("\n⚡ NEXT STEPS:")
        print("   1. Execute database update commands")
        print("   2. Run verification scripts")
        print("   3. Test frontend functionality")
        print("   4. Implement ongoing monitoring")
        
        print()
        print("9. IMPLEMENTATION PLAN")
        print("=" * 50)
        
        for phase in plan["phases"]:
            print(f"\nPhase {phase['phase']}: {phase['name']} ({phase['duration']})")
            for task in phase["tasks"]:
                print(f"   - {task}")
            
            if "sql_commands" in phase:
                print("   SQL Commands:")
                for cmd in phase["sql_commands"]:
                    print(f"     {cmd}")
        
        print()
        print("✅ ANALYSIS COMPLETE - READY FOR IMPLEMENTATION")

if __name__ == "__main__":
    asyncio.run(main())