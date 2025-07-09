#!/usr/bin/env python3
"""
Phase 1, Step 1.3: Migration Strategy Planning
Plan migration strategy based on current state and API capacity
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any

def load_audit_results() -> Dict[str, Any]:
    """Load the latest audit results"""
    # Find the most recent audit file
    audit_files = [f for f in os.listdir('.') if f.startswith('phase1_audit_results_')]
    if not audit_files:
        return {}
    
    latest_audit = sorted(audit_files)[-1]
    
    try:
        with open(latest_audit, 'r') as f:
            return json.load(f)
    except:
        return {}

def load_capacity_results() -> Dict[str, Any]:
    """Load the latest capacity test results"""
    # Find the most recent capacity file
    capacity_files = [f for f in os.listdir('.') if f.startswith('phase1_capacity_results_')]
    if not capacity_files:
        return {}
    
    latest_capacity = sorted(capacity_files)[-1]
    
    try:
        with open(latest_capacity, 'r') as f:
            return json.load(f)
    except:
        return {}

def plan_migration_strategy() -> Dict[str, Any]:
    """Plan the migration strategy based on audit and capacity results"""
    print("🔍 Planning Migration Strategy...")
    
    # Load previous results
    audit_results = load_audit_results()
    capacity_results = load_capacity_results()
    
    strategy = {
        "timestamp": datetime.now().isoformat(),
        "current_state": audit_results,
        "api_capacity": capacity_results,
        "migration_approach": {},
        "phase_breakdown": {},
        "risk_mitigation": {},
        "success_criteria": {}
    }
    
    # Analyze current state
    current_members = audit_results.get("members", {}).get("total_count", 0)
    current_committees = audit_results.get("committees", {}).get("total_count", 0)
    
    target_members = 535
    target_committees = 200  # Estimated
    
    members_gap = target_members - current_members
    committees_gap = target_committees - current_committees
    
    print(f"   📊 Current state: {current_members} members, {current_committees} committees")
    print(f"   📊 Target state: {target_members} members, {target_committees} committees")
    print(f"   📊 Gap: {members_gap} members, {committees_gap} committees")
    
    # Migration approach decision
    print("   🎯 Determining migration approach...")
    
    # Based on current 50-member sample, recommend incremental expansion
    if current_members > 0 and current_members < 100:
        approach = "incremental_expansion"
        print("   ✅ Recommended: Incremental expansion (build on existing data)")
    else:
        approach = "full_replacement"
        print("   ✅ Recommended: Full replacement (complete data refresh)")
    
    strategy["migration_approach"] = {
        "type": approach,
        "reason": f"Current dataset of {current_members} members is suitable for expansion",
        "backup_required": True,
        "rollback_plan": "Restore from backup if data quality degrades"
    }
    
    # Phase breakdown
    print("   📋 Planning phase breakdown...")
    
    # Based on API capacity and our 8-12 hour timeline
    api_recommendations = capacity_results.get("recommendations", {})
    batch_size = api_recommendations.get("batch_size", 15)
    request_delay = api_recommendations.get("request_delay", 0.7)
    
    # Calculate realistic timelines
    member_collection_batches = (members_gap + batch_size - 1) // batch_size
    committee_collection_batches = (committees_gap + batch_size - 1) // batch_size
    
    member_collection_time = member_collection_batches * (0.5 + request_delay)  # API time + delay
    committee_collection_time = committee_collection_batches * (0.5 + request_delay)
    
    strategy["phase_breakdown"] = {
        "phase_2_member_collection": {
            "target": f"{members_gap} additional members",
            "batches": member_collection_batches,
            "estimated_time_minutes": member_collection_time / 60,
            "estimated_time_hours": member_collection_time / 3600,
            "approach": "Progressive collection from Congress.gov API"
        },
        "phase_3_committee_expansion": {
            "target": f"{committees_gap} additional committees",
            "batches": committee_collection_batches,
            "estimated_time_minutes": committee_collection_time / 60,
            "estimated_time_hours": committee_collection_time / 3600,
            "approach": "Complete committee structure mapping"
        },
        "phase_4_data_integration": {
            "target": "Relationship mapping and validation",
            "estimated_time_hours": 2.0,
            "approach": "Cross-reference and validate relationships"
        },
        "phase_5_deployment": {
            "target": "Production deployment",
            "estimated_time_hours": 1.0,
            "approach": "Rolling deployment with backup"
        }
    }
    
    # Risk mitigation
    print("   🛡️ Planning risk mitigation...")
    
    strategy["risk_mitigation"] = {
        "api_rate_limiting": {
            "risk": "Congress.gov API rate limiting during bulk collection",
            "mitigation": f"Use batch size {batch_size} with {request_delay}s delays",
            "fallback": "Reduce batch size and increase delays if needed"
        },
        "data_quality_degradation": {
            "risk": "New data quality issues during expansion",
            "mitigation": "Incremental validation at each phase",
            "fallback": "Rollback to previous stable state"
        },
        "performance_impact": {
            "risk": "System performance degradation with larger dataset",
            "mitigation": "Database indexing and query optimization",
            "fallback": "Scale infrastructure resources"
        },
        "deployment_failure": {
            "risk": "Production deployment issues",
            "mitigation": "Blue-green deployment with health checks",
            "fallback": "Immediate rollback to previous version"
        }
    }
    
    # Success criteria
    print("   🎯 Defining success criteria...")
    
    strategy["success_criteria"] = {
        "quantitative": {
            "member_count": 535,
            "committee_count": 200,
            "data_accuracy": ">99%",
            "api_response_time": "<500ms",
            "system_uptime": ">99.9%"
        },
        "qualitative": {
            "complete_congressional_coverage": "All 119th Congress members",
            "enhanced_search_capabilities": "Improved filtering and search",
            "wikipedia_validation": "Leadership accuracy maintained",
            "user_experience": "No degradation in frontend performance"
        }
    }
    
    # Recommended next steps
    strategy["next_steps"] = [
        {
            "phase": "Phase 2: Complete Member Collection",
            "priority": "HIGH",
            "estimated_time": "3 hours",
            "dependencies": ["Congress.gov API access", "Database backup"]
        },
        {
            "phase": "Phase 3: Complete Committee Structure",
            "priority": "HIGH", 
            "estimated_time": "3 hours",
            "dependencies": ["Phase 2 completion", "Committee mapping"]
        },
        {
            "phase": "Phase 4: Enhanced Data Integration",
            "priority": "MEDIUM",
            "estimated_time": "2 hours",
            "dependencies": ["Phases 2-3 completion"]
        },
        {
            "phase": "Phase 5: Production Deployment",
            "priority": "MEDIUM",
            "estimated_time": "1 hour",
            "dependencies": ["All previous phases", "Deployment approval"]
        }
    ]
    
    print("✅ Migration Strategy Planning Complete")
    return strategy

def save_migration_strategy(strategy: Dict[str, Any]) -> str:
    """Save migration strategy to file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"phase1_migration_strategy_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(strategy, f, indent=2)
    
    print(f"📄 Migration strategy saved to: {filename}")
    return filename

def print_migration_summary(strategy: Dict[str, Any]):
    """Print migration strategy summary"""
    print("\n" + "="*60)
    print("📋 MIGRATION STRATEGY SUMMARY")
    print("="*60)
    
    print(f"🕐 Strategy Time: {strategy.get('timestamp', 'Unknown')}")
    
    # Migration approach
    approach = strategy.get("migration_approach", {})
    print(f"\n🎯 MIGRATION APPROACH:")
    print(f"   • Type: {approach.get('type', 'Unknown')}")
    print(f"   • Reason: {approach.get('reason', 'Unknown')}")
    print(f"   • Backup Required: {approach.get('backup_required', False)}")
    
    # Phase breakdown
    phases = strategy.get("phase_breakdown", {})
    print(f"\n📋 PHASE BREAKDOWN:")
    total_hours = 0
    for phase_name, phase_info in phases.items():
        hours = phase_info.get("estimated_time_hours", 0)
        total_hours += hours
        print(f"   • {phase_name}: {hours:.1f}h - {phase_info.get('target', 'Unknown')}")
    
    print(f"   • Total Estimated Time: {total_hours:.1f} hours")
    
    # Success criteria
    criteria = strategy.get("success_criteria", {})
    print(f"\n🎯 SUCCESS CRITERIA:")
    quantitative = criteria.get("quantitative", {})
    for criterion, target in quantitative.items():
        print(f"   • {criterion}: {target}")
    
    # Next steps
    next_steps = strategy.get("next_steps", [])
    print(f"\n🚀 NEXT STEPS:")
    for i, step in enumerate(next_steps, 1):
        print(f"   {i}. {step.get('phase', 'Unknown')} ({step.get('estimated_time', 'Unknown')})")
        print(f"      Priority: {step.get('priority', 'Unknown')}")
    
    print(f"\n📊 EXPANSION SUMMARY:")
    current_state = strategy.get("current_state", {})
    current_members = current_state.get("members", {}).get("total_count", 0)
    current_committees = current_state.get("committees", {}).get("total_count", 0)
    
    print(f"   • Current: {current_members} members, {current_committees} committees")
    print(f"   • Target: 535 members, 200 committees")
    print(f"   • Growth: {535 - current_members} members, {200 - current_committees} committees")
    print(f"   • Completion: From {current_members/535*100:.1f}% to 100% coverage")

if __name__ == "__main__":
    print("🚀 Phase 1, Step 1.3: Migration Strategy Planning")
    print("="*50)
    
    # Plan migration strategy
    migration_strategy = plan_migration_strategy()
    
    # Save strategy
    filename = save_migration_strategy(migration_strategy)
    
    # Print summary
    print_migration_summary(migration_strategy)
    
    print(f"\n📋 Phase 1 Complete - Ready for Phase 2:")
    print("   ✅ Current data audited")
    print("   ✅ API capacity assessed")
    print("   ✅ Migration strategy planned")
    print("   🚀 Ready to begin Phase 2: Complete Member Collection")