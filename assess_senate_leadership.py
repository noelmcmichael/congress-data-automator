#!/usr/bin/env python3
"""
Assess Current Senate Committee Leadership
Identify 118th vs 119th Congress leadership discrepancies
"""

import requests
import json
from datetime import datetime

API_BASE = "https://congressional-data-api-v2-1066017671167.us-central1.run.app"

def get_senate_committees():
    """Get all Senate standing committees"""
    response = requests.get(f"{API_BASE}/api/v1/committees?chamber=Senate&limit=100")
    if response.status_code == 200:
        committees = response.json()
        # Filter for standing committees (not subcommittees)
        standing = [c for c in committees if not c.get('is_subcommittee', True)]
        return standing
    return []

def get_committee_members(committee_id):
    """Get members of a specific committee"""
    response = requests.get(f"{API_BASE}/api/v1/committees/{committee_id}/members")
    if response.status_code == 200:
        return response.json()
    return []

def analyze_leadership():
    """Analyze current Senate committee leadership"""
    print("=" * 60)
    print("119TH CONGRESS SENATE LEADERSHIP ASSESSMENT")
    print("=" * 60)
    print(f"Assessment Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    committees = get_senate_committees()
    
    leadership_issues = []
    total_committees = 0
    democratic_chairs = 0
    republican_chairs = 0
    
    print("SENATE STANDING COMMITTEES LEADERSHIP:")
    print("-" * 60)
    
    for committee in committees:
        committee_id = committee['id']
        committee_name = committee['name']
        total_committees += 1
        
        members = get_committee_members(committee_id)
        
        chair = None
        ranking_member = None
        
        for member_info in members:
            position = member_info.get('position', 'member').lower()
            member = member_info['member']
            
            if position == 'chair':
                chair = member
            elif position == 'ranking_member':
                ranking_member = member
        
        # Analyze leadership
        chair_party = chair['party'] if chair else 'Unknown'
        ranking_party = ranking_member['party'] if ranking_member else 'Unknown'
        
        if chair and chair['party'] == 'Democratic':
            democratic_chairs += 1
            leadership_issues.append({
                'committee': committee_name,
                'issue': '118th Congress leadership (Democratic Chair)',
                'current_chair': f"{chair['first_name']} {chair['last_name']} (D)",
                'expected': 'Republican Chair for 119th Congress'
            })
        elif chair and chair['party'] == 'Republican':
            republican_chairs += 1
        
        print(f"Committee: {committee_name}")
        if chair:
            print(f"  Chair: {chair['first_name']} {chair['last_name']} ({chair['party'][0]})")
        if ranking_member:
            print(f"  Ranking: {ranking_member['first_name']} {ranking_member['last_name']} ({ranking_member['party'][0]})")
        print()
    
    print("=" * 60)
    print("LEADERSHIP SUMMARY:")
    print("=" * 60)
    print(f"Total Senate Standing Committees: {total_committees}")
    print(f"Democratic Chairs (118th Congress): {democratic_chairs}")
    print(f"Republican Chairs (119th Congress): {republican_chairs}")
    print(f"Committees Needing Leadership Updates: {len(leadership_issues)}")
    
    if leadership_issues:
        print()
        print("COMMITTEES WITH 118TH CONGRESS LEADERSHIP:")
        print("-" * 40)
        for issue in leadership_issues:
            print(f"• {issue['committee']}")
            print(f"  Current: {issue['current_chair']}")
            print(f"  Needed: {issue['expected']}")
            print()
    
    # Save results
    results = {
        'assessment_time': datetime.now().isoformat(),
        'total_committees': total_committees,
        'democratic_chairs': democratic_chairs,
        'republican_chairs': republican_chairs,
        'leadership_issues': leadership_issues,
        'committees_analyzed': committees
    }
    
    with open('senate_leadership_assessment.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Assessment saved to: senate_leadership_assessment.json")
    
    return results

if __name__ == "__main__":
    analyze_leadership()