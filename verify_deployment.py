#!/usr/bin/env python3
"""
Verify deployment success
"""

import requests
import json

def verify_deployment():
    print("🔍 Verifying deployment success...")
    
    # Check hearing coverage
    response = requests.get("https://congressional-data-api-v2-1066017671167.us-central1.run.app/api/v1/hearings?limit=100")
    hearings = response.json()
    
    hearings_with_committee = sum(1 for h in hearings if h.get('committee_id'))
    coverage = (hearings_with_committee / len(hearings)) * 100 if hearings else 0
    
    print(f"📊 Post-deployment hearing coverage: {coverage:.1f}%")
    
    # Check specific hearing that should be updated
    response = requests.get("https://congressional-data-api-v2-1066017671167.us-central1.run.app/api/v1/hearings/120")
    if response.status_code == 200:
        hearing_120 = response.json()
        committee_id = hearing_120.get('committee_id')
        if committee_id == 134:
            print("✅ Hearing 120 correctly assigned to committee 134")
        else:
            print(f"❌ Hearing 120 committee_id: {committee_id} (expected: 134)")
    
    if coverage >= 40:
        print("🎉 DEPLOYMENT SUCCESSFUL!")
        return True
    else:
        print("❌ Deployment did not achieve expected coverage")
        return False

if __name__ == "__main__":
    verify_deployment()
