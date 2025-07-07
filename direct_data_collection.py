#!/usr/bin/env python3
"""
Direct data collection script that bypasses the service and collects data directly.
"""

import os
import sys
import requests
import json
from datetime import datetime
import time

# Add the backend directory to the Python path
sys.path.insert(0, '/Users/noelmcmichael/Workspace/congress_data_automator/backend')

def setup_environment():
    """Set up the environment for direct data collection."""
    print("🔧 Setting up environment for direct data collection...")
    
    # Set environment variables
    os.environ['CONGRESS_API_KEY'] = 'NcMVmULsduvTXfEIXhKgAb1uWDDFdzOcPI57jpRG'
    os.environ['DATABASE_URL'] = 'postgresql://postgres:mDf3S9ZnBpQqJvGsY1@localhost:5432/congress_data?host=/cloudsql/chefgavin:us-central1:congressional-db'
    os.environ['ENVIRONMENT'] = 'production'
    
    print("✅ Environment variables set")

def collect_full_member_data():
    """Collect full member data from Congress.gov API."""
    print("📊 Collecting full member data from Congress.gov API...")
    
    api_key = os.environ.get('CONGRESS_API_KEY')
    if not api_key:
        print("❌ No API key found")
        return False
    
    headers = {
        'X-API-Key': api_key
    }
    
    all_members = []
    
    # Collect House members
    print("🏛️ Collecting House members...")
    try:
        response = requests.get(
            'https://api.congress.gov/v3/member',
            headers=headers,
            params={
                'limit': 250,
                'chamber': 'house',
                'currentMember': 'true'
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            house_members = data.get('members', [])
            all_members.extend(house_members)
            print(f"✅ Collected {len(house_members)} House members")
        else:
            print(f"❌ Failed to collect House members: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error collecting House members: {e}")
        return False
    
    # Collect Senate members
    print("🏛️ Collecting Senate members...")
    try:
        response = requests.get(
            'https://api.congress.gov/v3/member',
            headers=headers,
            params={
                'limit': 250,
                'chamber': 'senate',
                'currentMember': 'true'
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            senate_members = data.get('members', [])
            all_members.extend(senate_members)
            print(f"✅ Collected {len(senate_members)} Senate members")
        else:
            print(f"❌ Failed to collect Senate members: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error collecting Senate members: {e}")
        return False
    
    # Save the data
    total_members = len(all_members)
    print(f"📝 Total members collected: {total_members}")
    
    # Save to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"full_congress_data_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(all_members, f, indent=2)
    
    print(f"✅ Data saved to {filename}")
    
    return all_members

def upload_to_production_api():
    """Upload the collected data to the production API."""
    print("🚀 Uploading data to production API...")
    
    # Use the production API endpoint to trigger data collection
    api_base = "https://congressional-data-api-v2-1066017671167.us-central1.run.app"
    
    try:
        # Trigger member update
        response = requests.post(
            f"{api_base}/api/v1/update/members",
            params={"force_refresh": True},
            timeout=300
        )
        
        if response.status_code == 200:
            print("✅ Member update triggered successfully")
            
            # Wait for completion
            print("⏳ Waiting for update to complete...")
            time.sleep(30)
            
            # Check the result
            response = requests.get(f"{api_base}/api/v1/members", timeout=30)
            if response.status_code == 200:
                members = response.json()
                print(f"✅ Members now in database: {len(members)}")
                return True
            else:
                print(f"❌ Failed to verify member count: {response.status_code}")
                return False
                
        else:
            print(f"❌ Failed to trigger member update: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error uploading to production API: {e}")
        return False

def main():
    """Main function for direct data collection."""
    print("🚀 Congressional Data - Direct Collection Phase 2")
    print("=" * 50)
    
    # Step 1: Setup environment
    setup_environment()
    
    # Step 2: Collect full data
    members_data = collect_full_member_data()
    
    if not members_data:
        print("❌ Failed to collect member data")
        return False
    
    # Step 3: Upload to production
    success = upload_to_production_api()
    
    if success:
        print("🎉 Phase 2 Step 1 & 2 Complete!")
        print("✅ Full congressional data collected and uploaded")
        print("🔗 Production API: https://congressional-data-api-v2-1066017671167.us-central1.run.app")
        return True
    else:
        print("❌ Failed to upload data to production")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)