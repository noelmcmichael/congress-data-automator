#!/usr/bin/env python3
"""
Create comprehensive plan to fix all congressional data issues.
Priority: Senate first, then House, with proper 119th Congress context.
"""

import os
import sys
from sqlalchemy import create_engine, text
import logging
import json
from datetime import datetime, date

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_comprehensive_fix_plan():
    """Create plan to fix all congressional data issues."""
    
    logger.info("📋 CREATING COMPREHENSIVE FIX PLAN")
    logger.info("="*60)
    
    plan = {
        "title": "119th Congress Data Comprehensive Fix",
        "created": datetime.now().isoformat(),
        "congress": {
            "number": 119,
            "years": "2025-2027",
            "status": "Current"
        },
        "priority": "Senate first, then House",
        "phases": []
    }
    
    # Phase 1: Fix Senate Data and Relationships
    phase1 = {
        "phase": 1,
        "title": "Complete Senate Data and Relationships",
        "priority": "HIGH",
        "estimated_time": "45 minutes",
        "tasks": [
            {
                "task": "1.1",
                "title": "Complete Senate Membership",
                "description": "Ensure all 100 senators are in database with proper term information",
                "actions": [
                    "Verify current 55 senators",
                    "Add missing 45 senators for complete 100",
                    "Update term_end dates for 2025 re-elections (Class I senators)",
                    "Validate all 50 states have 2 senators"
                ],
                "success_criteria": "100 senators total, all states represented"
            },
            {
                "task": "1.2", 
                "title": "Complete Senate Committee Assignments",
                "description": "Assign all senators to appropriate committees with leadership roles",
                "actions": [
                    "Create realistic Senate committee assignments",
                    "Assign committee chairs and ranking members",
                    "Ensure proper party ratio on committees",
                    "Add subcommittee assignments"
                ],
                "success_criteria": "95%+ senators have committee assignments"
            },
            {
                "task": "1.3",
                "title": "Senate Committee Hierarchy",
                "description": "Link all Senate subcommittees to parent committees",
                "actions": [
                    "Map subcommittees to standing committees",
                    "Update parent_committee_id for all subcommittees",
                    "Verify hierarchy is correct"
                ],
                "success_criteria": "All Senate subcommittees linked to parent committees"
            }
        ]
    }
    
    # Phase 2: Fix House Data and Relationships  
    phase2 = {
        "phase": 2,
        "title": "Complete House Data and Relationships",
        "priority": "HIGH", 
        "estimated_time": "60 minutes",
        "tasks": [
            {
                "task": "2.1",
                "title": "Complete House Membership",
                "description": "Ensure all 435 House members are in database",
                "actions": [
                    "Verify current 483 House members", 
                    "Handle any discrepancies (vacancies, special elections)",
                    "Validate district assignments",
                    "Update for 119th Congress composition"
                ],
                "success_criteria": "435 House members total with proper districts"
            },
            {
                "task": "2.2",
                "title": "Complete House Committee Assignments", 
                "description": "Assign all House members to appropriate committees",
                "actions": [
                    "Create realistic House committee assignments",
                    "Assign committee chairs and ranking members",
                    "Ensure proper party ratio on committees",
                    "Add subcommittee assignments"
                ],
                "success_criteria": "95%+ House members have committee assignments"
            },
            {
                "task": "2.3",
                "title": "House Committee Hierarchy",
                "description": "Link all House subcommittees to parent committees", 
                "actions": [
                    "Map subcommittees to standing committees",
                    "Update parent_committee_id for all subcommittees",
                    "Verify hierarchy is correct"
                ],
                "success_criteria": "All House subcommittees linked to parent committees"
            }
        ]
    }
    
    # Phase 3: 119th Congress Context and Future-Proofing
    phase3 = {
        "phase": 3,
        "title": "119th Congress Context and Future-Proofing",
        "priority": "MEDIUM",
        "estimated_time": "30 minutes", 
        "tasks": [
            {
                "task": "3.1",
                "title": "Add Congress Context",
                "description": "Add 119th Congress context to all data",
                "actions": [
                    "Add congress_number field to relevant tables",
                    "Set all current data to 119th Congress",
                    "Add effective_date ranges",
                    "Update documentation references"
                ],
                "success_criteria": "All data properly labeled as 119th Congress"
            },
            {
                "task": "3.2",
                "title": "Senator Term Tracking",
                "description": "Complete senator term information for re-election planning",
                "actions": [
                    "Set proper term_end dates for each senator class",
                    "Class I: Up for re-election 2025",
                    "Class II: Up for re-election 2027", 
                    "Class III: Up for re-election 2029",
                    "Add term_class field"
                ],
                "success_criteria": "All senators have proper term information"
            },
            {
                "task": "3.3",
                "title": "Future Congress Preparation",
                "description": "Prepare system for 120th Congress transition",
                "actions": [
                    "Design congress transition workflow",
                    "Add archival system for historical data",
                    "Create 120th Congress preparation templates",
                    "Document transition procedures"
                ],
                "success_criteria": "System ready for future congress transitions"
            }
        ]
    }
    
    # Phase 4: Validation and Enhancement
    phase4 = {
        "phase": 4,
        "title": "Validation and Dashboard Enhancement",
        "priority": "MEDIUM",
        "estimated_time": "30 minutes",
        "tasks": [
            {
                "task": "4.1",
                "title": "Complete Data Validation",
                "description": "Validate all fixes and ensure data quality",
                "actions": [
                    "Run comprehensive validation tests",
                    "Verify relationship completeness", 
                    "Check committee hierarchy accuracy",
                    "Validate 119th Congress context"
                ],
                "success_criteria": "All validation tests pass"
            },
            {
                "task": "4.2",
                "title": "Enhanced Dashboard Views",
                "description": "Create enhanced views leveraging complete relationships",
                "actions": [
                    "Committee hierarchy views",
                    "Senator term timeline views",
                    "Party leadership dashboards",
                    "Committee jurisdiction mappings"
                ],
                "success_criteria": "Rich dashboard views available"
            }
        ]
    }
    
    plan["phases"] = [phase1, phase2, phase3, phase4]
    
    # Summary
    plan["summary"] = {
        "total_phases": 4,
        "total_tasks": sum(len(phase["tasks"]) for phase in plan["phases"]),
        "estimated_total_time": "165 minutes (2h 45m)",
        "key_priorities": [
            "Complete Senate data first (100 senators)",
            "Fix committee hierarchy (164 subcommittees need parent links)",
            "Improve relationship coverage (currently <11%)",
            "Ensure 119th Congress accuracy",
            "Prepare for future congress transitions"
        ]
    }
    
    # Save plan
    with open('comprehensive_fix_plan_119th.json', 'w') as f:
        json.dump(plan, f, indent=2)
    
    logger.info("📋 COMPREHENSIVE FIX PLAN CREATED")
    logger.info(f"Total phases: {plan['summary']['total_phases']}")
    logger.info(f"Total tasks: {plan['summary']['total_tasks']}")
    logger.info(f"Estimated time: {plan['summary']['estimated_total_time']}")
    logger.info("Priority: Senate first, then House")
    logger.info("Congress: 119th (2025-2027)")
    logger.info("\nKey fixes needed:")
    for priority in plan['summary']['key_priorities']:
        logger.info(f"  • {priority}")
    
    logger.info(f"\nPlan saved to: comprehensive_fix_plan_119th.json")
    
    return plan

if __name__ == "__main__":
    create_comprehensive_fix_plan()