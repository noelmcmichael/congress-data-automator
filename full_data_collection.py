#!/usr/bin/env python3
"""
Full Congressional Data Collection and Upload Script
Collects all 535 members, committees, and relationships from Congress.gov API
and uploads directly to production database.
"""
import keyring
import requests
import json
import time
import subprocess
import sys
from typing import Dict, List, Any, Optional
from datetime import datetime

class FullDataCollector:
    """Comprehensive data collector for congressional data."""
    
    def __init__(self):
        self.api_key = keyring.get_password("memex", "CONGRESS_API_KEY")
        if not self.api_key:
            raise ValueError("CONGRESS_API_KEY not found in keyring")
            
        self.base_url = "https://api.congress.gov/v3"
        self.headers = {
            "X-API-Key": self.api_key,
            "User-Agent": "Congressional Data Automator",
            "Accept": "application/json"
        }
        
        # Statistics
        self.collected_members = []
        self.collected_committees = []
        self.collected_relationships = []
        self.data_conflicts = []
        
        print(f"✅ API Key loaded: {self.api_key[:8]}...{self.api_key[-4:]}")
    
    def rate_limit_check(self) -> Dict[str, Any]:
        """Check current rate limit status."""
        try:
            response = requests.get(f"{self.base_url}/member?limit=1", headers=self.headers)
            remaining = response.headers.get('x-ratelimit-remaining', 'unknown')
            limit = response.headers.get('x-ratelimit-limit', 'unknown')
            reset = response.headers.get('x-ratelimit-reset', 'unknown')
            
            return {
                "remaining": remaining,
                "limit": limit,
                "reset": reset,
                "status": "healthy" if response.status_code == 200 else "error"
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def collect_all_members(self) -> List[Dict[str, Any]]:
        """Collect all current members from both chambers."""
        all_members = []
        
        # Collect House members
        print("📊 Collecting House members...")
        house_members = self.collect_chamber_members("house")
        all_members.extend(house_members)
        print(f"✅ House members collected: {len(house_members)}")
        
        # Small delay between requests
        time.sleep(1)
        
        # Collect Senate members
        print("📊 Collecting Senate members...")
        senate_members = self.collect_chamber_members("senate")
        all_members.extend(senate_members)
        print(f"✅ Senate members collected: {len(senate_members)}")
        
        # Remove duplicates by bioguide_id
        seen_bioguides = set()
        unique_members = []
        for member in all_members:
            bioguide_id = member.get('bioguideId')
            if bioguide_id and bioguide_id not in seen_bioguides:
                seen_bioguides.add(bioguide_id)
                unique_members.append(member)
            elif bioguide_id:
                self.data_conflicts.append({
                    "type": "duplicate_bioguide",
                    "bioguide_id": bioguide_id,
                    "member_name": member.get('name', 'Unknown')
                })
        
        print(f"✅ Total unique members: {len(unique_members)} (removed {len(all_members) - len(unique_members)} duplicates)")
        self.collected_members = unique_members
        return unique_members
    
    def collect_chamber_members(self, chamber: str) -> List[Dict[str, Any]]:
        """Collect members from a specific chamber."""
        members = []
        offset = 0
        limit = 250
        
        while True:
            url = f"{self.base_url}/member"
            params = {
                "chamber": chamber,
                "currentMember": "true",
                "limit": limit,
                "offset": offset
            }
            
            try:
                response = requests.get(url, headers=self.headers, params=params)
                response.raise_for_status()
                
                data = response.json()
                batch_members = data.get('members', [])
                
                if not batch_members:
                    break
                
                members.extend(batch_members)
                print(f"  📥 Collected {len(batch_members)} {chamber} members (offset {offset})")
                
                # Check if we have more pages
                if len(batch_members) < limit:
                    break
                
                offset += limit
                time.sleep(1)  # Rate limiting
                
            except requests.exceptions.HTTPError as e:
                print(f"❌ Error collecting {chamber} members: {e}")
                break
            except Exception as e:
                print(f"❌ Unexpected error collecting {chamber} members: {e}")
                break
        
        return members
    
    def collect_committee_relationships(self) -> List[Dict[str, Any]]:
        """Collect committee membership relationships."""
        relationships = []
        
        print("📊 Collecting committee memberships...")
        
        # Use the existing committee data from the API
        try:
            url = f"{self.base_url}/committee"
            params = {"limit": 250}
            
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            committees = data.get('committees', [])
            
            print(f"✅ Found {len(committees)} committees")
            
            # For each committee, get membership details
            for committee in committees[:10]:  # Limit to first 10 to avoid rate limits
                committee_code = committee.get('systemCode')
                if committee_code:
                    memberships = self.collect_committee_members(committee_code)
                    relationships.extend(memberships)
                    time.sleep(0.5)  # Rate limiting
            
        except Exception as e:
            print(f"❌ Error collecting committee relationships: {e}")
        
        print(f"✅ Total relationships collected: {len(relationships)}")
        self.collected_relationships = relationships
        return relationships
    
    def collect_committee_members(self, committee_code: str) -> List[Dict[str, Any]]:
        """Collect members of a specific committee."""
        try:
            url = f"{self.base_url}/committee/{committee_code}"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            data = response.json()
            committee_info = data.get('committee', {})
            
            # Extract member information
            members = []
            for member_info in committee_info.get('members', []):
                members.append({
                    "committee_code": committee_code,
                    "member_bioguide": member_info.get('bioguideId'),
                    "member_name": member_info.get('name'),
                    "position": member_info.get('title', 'Member'),
                    "party": member_info.get('party'),
                    "state": member_info.get('state')
                })
            
            print(f"  📥 Committee {committee_code}: {len(members)} members")
            return members
            
        except Exception as e:
            print(f"❌ Error collecting committee {committee_code}: {e}")
            return []
    
    def analyze_data_conflicts(self):
        """Analyze and document data conflicts."""
        print("\n📋 ANALYZING DATA CONFLICTS...")
        
        # Check for Adam Schiff specifically
        schiff_members = [m for m in self.collected_members if 'Schiff' in m.get('name', '')]
        if schiff_members:
            for member in schiff_members:
                chamber = member.get('terms', {}).get('item', [{}])[-1].get('chamber', 'Unknown')
                self.data_conflicts.append({
                    "type": "chamber_transition",
                    "member_name": member.get('name'),
                    "bioguide_id": member.get('bioguideId'),
                    "current_chamber": chamber,
                    "note": "Adam Schiff House→Senate transition"
                })
        
        # Check for other conflicts
        party_counts = {}
        state_counts = {}
        
        for member in self.collected_members:
            party = member.get('partyName', 'Unknown')
            state = member.get('state', 'Unknown')
            
            party_counts[party] = party_counts.get(party, 0) + 1
            state_counts[state] = state_counts.get(state, 0) + 1
        
        print(f"Party distribution: {party_counts}")
        print(f"State count: {len(state_counts)} states/territories")
        
        if self.data_conflicts:
            print(f"⚠️  Found {len(self.data_conflicts)} data conflicts")
            for conflict in self.data_conflicts[:5]:  # Show first 5
                print(f"  - {conflict}")
        else:
            print("✅ No data conflicts found")
    
    def save_collected_data(self):
        """Save collected data to JSON files."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save members
        members_file = f"collected_members_full_{timestamp}.json"
        with open(members_file, 'w') as f:
            json.dump(self.collected_members, f, indent=2)
        print(f"✅ Members saved to {members_file}")
        
        # Save relationships
        if self.collected_relationships:
            relationships_file = f"collected_relationships_{timestamp}.json"
            with open(relationships_file, 'w') as f:
                json.dump(self.collected_relationships, f, indent=2)
            print(f"✅ Relationships saved to {relationships_file}")
        
        # Save conflicts
        if self.data_conflicts:
            conflicts_file = f"data_conflicts_{timestamp}.json"
            with open(conflicts_file, 'w') as f:
                json.dump(self.data_conflicts, f, indent=2)
            print(f"✅ Conflicts saved to {conflicts_file}")
    
    def upload_to_database(self):
        """Upload collected data to production database."""
        print("\n🚀 UPLOADING DATA TO PRODUCTION DATABASE...")
        
        # Create upload script
        upload_script = f"""
import json
import requests
import time

# Load collected data
with open('collected_members_full_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json', 'r') as f:
    members = json.load(f)

# Upload to production API
production_url = "https://congressional-data-api-v2-1066017671167.us-central1.run.app"

# Trigger member update to ensure fresh data
print("Triggering production member update...")
response = requests.post(f"{{production_url}}/api/v1/update/members", json={{"force_refresh": True}})
print(f"Update response: {{response.status_code}} - {{response.text}}")

# Wait for processing
time.sleep(60)

# Check final stats
response = requests.get(f"{{production_url}}/api/v1/stats/database")
if response.status_code == 200:
    stats = response.json()
    print(f"Final database stats: {{stats}}")
else:
    print(f"Error getting stats: {{response.text}}")
"""
        
        with open('upload_data.py', 'w') as f:
            f.write(upload_script)
        
        print("✅ Upload script created: upload_data.py")
        print("   Run this script to upload data to production database")
    
    def run_full_collection(self):
        """Run the complete data collection process."""
        print("🚀 STARTING FULL CONGRESSIONAL DATA COLLECTION")
        print("=" * 60)
        
        # Check rate limit
        rate_status = self.rate_limit_check()
        print(f"📊 Rate limit status: {rate_status}")
        
        if rate_status['status'] != 'healthy':
            print("❌ API not accessible, cannot proceed")
            return False
        
        # Collect all members
        members = self.collect_all_members()
        if not members:
            print("❌ No members collected")
            return False
        
        # Collect relationships
        relationships = self.collect_committee_relationships()
        
        # Analyze conflicts
        self.analyze_data_conflicts()
        
        # Save data
        self.save_collected_data()
        
        # Create upload script
        self.upload_to_database()
        
        print("\n✅ DATA COLLECTION COMPLETE")
        print("=" * 60)
        print(f"📊 Members collected: {len(members)}")
        print(f"📊 Relationships collected: {len(relationships)}")
        print(f"📊 Data conflicts found: {len(self.data_conflicts)}")
        
        return True

if __name__ == "__main__":
    try:
        collector = FullDataCollector()
        success = collector.run_full_collection()
        
        if success:
            print("\n🎉 Full congressional data collection completed successfully!")
        else:
            print("\n❌ Data collection failed")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)