#!/usr/bin/env python3
"""
Phase 1, Step 1.1: Current Data Audit
Audit current production data to establish baseline for expansion
"""

import requests
import json
from datetime import datetime
from typing import Dict, List, Any

# Production API base URL
API_BASE = "https://congressional-data-api-v2-1066017671167.us-central1.run.app/api/v1"

def audit_current_data() -> Dict[str, Any]:
    """Audit current production data"""
    print("🔍 Starting Current Data Audit...")
    
    audit_results = {
        "timestamp": datetime.now().isoformat(),
        "members": {},
        "committees": {},
        "data_quality": {},
        "api_performance": {}
    }
    
    try:
        # Test API health first
        print("   Testing API health...")
        health_response = requests.get("https://congressional-data-api-v2-1066017671167.us-central1.run.app/health", timeout=10)
        audit_results["api_performance"]["health_status"] = health_response.status_code
        audit_results["api_performance"]["health_response_time"] = health_response.elapsed.total_seconds()
        
        if health_response.status_code != 200:
            print(f"   ❌ API health check failed: {health_response.status_code}")
            return audit_results
        
        print("   ✅ API is healthy")
        
        # Audit members
        print("   Auditing members...")
        members_response = requests.get(f"{API_BASE}/members", timeout=30)
        if members_response.status_code == 200:
            members_data = members_response.json()
            audit_results["api_performance"]["members_response_time"] = members_response.elapsed.total_seconds()
            
            # API returns direct array, not wrapped in "members" key
            members = members_data if isinstance(members_data, list) else members_data.get("members", [])
            audit_results["members"]["total_count"] = len(members)
            
            chamber_counts = {}
            party_counts = {}
            state_counts = {}
            
            for member in members:
                # Chamber analysis
                chamber = member.get("chamber", "Unknown")
                chamber_counts[chamber] = chamber_counts.get(chamber, 0) + 1
                
                # Party analysis
                party = member.get("party", "Unknown")
                party_counts[party] = party_counts.get(party, 0) + 1
                
                # State analysis
                state = member.get("state", "Unknown")
                state_counts[state] = state_counts.get(state, 0) + 1
            
            audit_results["members"]["by_chamber"] = chamber_counts
            audit_results["members"]["by_party"] = party_counts
            audit_results["members"]["states_represented"] = len(state_counts)
            audit_results["members"]["sample_states"] = list(state_counts.keys())[:10]
            
            print(f"   📊 Members: {len(members)} total")
            print(f"   📊 Chambers: {chamber_counts}")
            print(f"   📊 Parties: {party_counts}")
            print(f"   📊 States: {len(state_counts)} represented")
        
        # Audit committees
        print("   Auditing committees...")
        committees_response = requests.get(f"{API_BASE}/committees", timeout=30)
        if committees_response.status_code == 200:
            committees_data = committees_response.json()
            audit_results["api_performance"]["committees_response_time"] = committees_response.elapsed.total_seconds()
            
            # API returns direct array, not wrapped in "committees" key
            committees = committees_data if isinstance(committees_data, list) else committees_data.get("committees", [])
            audit_results["committees"]["total_count"] = len(committees)
            
            chamber_counts = {}
            type_counts = {}
            
            for committee in committees:
                # Chamber analysis
                chamber = committee.get("chamber", "Unknown")
                chamber_counts[chamber] = chamber_counts.get(chamber, 0) + 1
                
                # Type analysis
                committee_type = committee.get("type", "Unknown")
                type_counts[committee_type] = type_counts.get(committee_type, 0) + 1
            
            audit_results["committees"]["by_chamber"] = chamber_counts
            audit_results["committees"]["by_type"] = type_counts
            
            print(f"   📊 Committees: {len(committees)} total")
            print(f"   📊 Chambers: {chamber_counts}")
            print(f"   📊 Types: {type_counts}")
        
        # Data quality assessment
        print("   Assessing data quality...")
        
        # Expected totals for 119th Congress
        expected_members = 535  # 435 House + 100 Senate
        expected_house_committees = 20  # Approximate standing committees
        expected_senate_committees = 16  # Approximate standing committees
        
        current_members = audit_results["members"]["total_count"]
        current_committees = audit_results["committees"]["total_count"]
        
        audit_results["data_quality"]["completeness"] = {
            "members_percentage": round((current_members / expected_members) * 100, 2),
            "members_gap": expected_members - current_members,
            "committees_current": current_committees
        }
        
        print(f"   📈 Member completeness: {audit_results['data_quality']['completeness']['members_percentage']}%")
        print(f"   📈 Members gap: {audit_results['data_quality']['completeness']['members_gap']} needed")
        
        print("✅ Current Data Audit Complete")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ API request failed: {e}")
        audit_results["error"] = str(e)
    except Exception as e:
        print(f"❌ Audit failed: {e}")
        audit_results["error"] = str(e)
    
    return audit_results

def save_audit_results(results: Dict[str, Any]) -> str:
    """Save audit results to file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"phase1_audit_results_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"📄 Audit results saved to: {filename}")
    return filename

def print_audit_summary(results: Dict[str, Any]):
    """Print audit summary"""
    print("\n" + "="*60)
    print("📋 CURRENT DATA AUDIT SUMMARY")
    print("="*60)
    
    if "error" in results:
        print(f"❌ Audit failed: {results['error']}")
        return
    
    members = results.get("members", {})
    committees = results.get("committees", {})
    quality = results.get("data_quality", {})
    performance = results.get("api_performance", {})
    
    print(f"🕐 Audit Time: {results.get('timestamp', 'Unknown')}")
    print(f"🌐 API Health: {performance.get('health_status', 'Unknown')}")
    print(f"⚡ API Response Time: {performance.get('health_response_time', 'Unknown')}s")
    
    print(f"\n📊 CURRENT DATA STATUS:")
    print(f"   • Members: {members.get('total_count', 0)} total")
    print(f"   • Committees: {committees.get('total_count', 0)} total")
    print(f"   • Completeness: {quality.get('completeness', {}).get('members_percentage', 0)}% of expected 535 members")
    print(f"   • Gap: {quality.get('completeness', {}).get('members_gap', 0)} members needed")
    
    print(f"\n🏛️ CHAMBER BREAKDOWN:")
    chamber_counts = members.get("by_chamber", {})
    for chamber, count in chamber_counts.items():
        print(f"   • {chamber}: {count} members")
    
    print(f"\n🎗️ PARTY BREAKDOWN:")
    party_counts = members.get("by_party", {})
    for party, count in party_counts.items():
        print(f"   • {party}: {count} members")
    
    print(f"\n📋 COMMITTEE BREAKDOWN:")
    committee_chambers = committees.get("by_chamber", {})
    for chamber, count in committee_chambers.items():
        print(f"   • {chamber}: {count} committees")

if __name__ == "__main__":
    print("🚀 Phase 1, Step 1.1: Current Data Audit")
    print("="*50)
    
    # Perform audit
    audit_results = audit_current_data()
    
    # Save results
    filename = save_audit_results(audit_results)
    
    # Print summary
    print_audit_summary(audit_results)
    
    print(f"\n📋 Next Steps:")
    print("   1. Review audit results")
    print("   2. Proceed to Step 1.2: Congress.gov API Capacity Planning")
    print("   3. Plan migration strategy based on current state")