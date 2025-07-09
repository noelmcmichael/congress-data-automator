#!/usr/bin/env python3
"""
Phase 3: Complete Committee Structure Expansion
Comprehensive implementation of committee data collection and integration
"""

import os
import sys
import json
import time
import asyncio
import aiohttp
from datetime import datetime
from typing import List, Dict, Optional
import subprocess
import requests
from urllib.parse import urljoin

# Add the project root to the Python path
sys.path.append('/Users/noelmcmichael/Workspace/congress_data_automator')

class Phase3Implementation:
    def __init__(self):
        self.congress_api_key = os.getenv('CONGRESS_API_KEY')
        self.congress_base_url = "https://api.congress.gov/v3"
        self.api_base_url = "https://politicalequity.io/api/v1"
        self.results = {}
        
        if not self.congress_api_key:
            print("❌ CONGRESS_API_KEY not found in environment")
            sys.exit(1)
    
    def run_command(self, cmd: str, description: str) -> tuple:
        """Run a command and return success status and output"""
        print(f"\n🔧 {description}")
        print(f"Command: {cmd}")
        
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)
            if result.returncode == 0:
                print(f"✅ Success: {description}")
                return True, result.stdout
            else:
                print(f"❌ Failed: {description}")
                print(f"Error: {result.stderr}")
                return False, result.stderr
        except Exception as e:
            print(f"💥 Exception: {e}")
            return False, str(e)
    
    def test_api_endpoint(self, endpoint: str, description: str) -> Optional[Dict]:
        """Test an API endpoint and return response data"""
        print(f"\n🧪 Testing: {description}")
        print(f"URL: {endpoint}")
        
        try:
            response = requests.get(endpoint, timeout=15)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {description} - Status: {response.status_code}")
                print(f"📊 Response: {len(data) if isinstance(data, list) else 'Object'}")
                return data
            else:
                print(f"❌ {description} - Status: {response.status_code}")
                return None
        except Exception as e:
            print(f"💥 {description} - Error: {e}")
            return None
    
    async def fetch_congress_committees(self) -> List[Dict]:
        """Fetch all committees from Congress.gov API"""
        print("\n📡 Fetching Committees from Congress.gov API")
        print("=" * 50)
        
        headers = {
            'X-API-Key': self.congress_api_key,
            'Accept': 'application/json'
        }
        
        all_committees = []
        
        try:
            async with aiohttp.ClientSession() as session:
                # Fetch committees with pagination
                offset = 0
                limit = 250  # Maximum allowed by API
                
                while True:
                    url = f"{self.congress_base_url}/committee"
                    params = {
                        'offset': offset,
                        'limit': limit
                    }
                    
                    print(f"📡 Fetching batch: offset={offset}, limit={limit}")
                    
                    async with session.get(url, headers=headers, params=params) as response:
                        if response.status == 200:
                            data = await response.json()
                            committees = data.get('committees', [])
                            
                            if not committees:
                                print(f"📊 No more committees found at offset {offset}")
                                break
                            
                            all_committees.extend(committees)
                            print(f"📊 Collected {len(committees)} committees (total: {len(all_committees)})")
                            
                            # Check if we've reached the end
                            if len(committees) < limit:
                                print(f"📊 Reached end of results (got {len(committees)} < {limit})")
                                break
                            
                            offset += limit
                            
                            # Rate limiting
                            await asyncio.sleep(1)
                            
                        else:
                            print(f"❌ API Error: {response.status}")
                            break
                
                print(f"✅ Total committees collected: {len(all_committees)}")
                return all_committees
                
        except Exception as e:
            print(f"❌ Committee collection failed: {e}")
            return []
    
    def analyze_committee_structure(self, committees: List[Dict]) -> Dict:
        """Analyze the structure of collected committees"""
        print("\n🔍 Analyzing Committee Structure")
        print("=" * 50)
        
        analysis = {
            'total_count': len(committees),
            'by_chamber': {},
            'by_congress': {},
            'sample_committees': []
        }
        
        for committee in committees:
            # Chamber analysis
            chamber = committee.get('chamber', 'Unknown')
            analysis['by_chamber'][chamber] = analysis['by_chamber'].get(chamber, 0) + 1
            
            # Congress session analysis
            congress = committee.get('congress', 'Unknown')
            analysis['by_congress'][congress] = analysis['by_congress'].get(congress, 0) + 1
        
        # Sample committees
        analysis['sample_committees'] = committees[:10]
        
        # Print analysis
        print(f"📊 Total Committees: {analysis['total_count']}")
        
        print("\n📋 By Chamber:")
        for chamber, count in analysis['by_chamber'].items():
            print(f"   {chamber}: {count}")
        
        print("\n📋 By Congress:")
        for congress, count in analysis['by_congress'].items():
            print(f"   {congress}: {count}")
        
        print("\n📋 Sample Committees:")
        for i, committee in enumerate(analysis['sample_committees']):
            name = committee.get('name', 'Unknown')
            chamber = committee.get('chamber', 'Unknown')
            congress = committee.get('congress', 'Unknown')
            print(f"   {i+1}. {chamber} ({congress}): {name}")
        
        return analysis
    
    def filter_119th_congress_committees(self, committees: List[Dict]) -> List[Dict]:
        """Filter committees for 119th Congress"""
        print("\n🔍 Filtering for 119th Congress")
        print("=" * 50)
        
        filtered = []
        for committee in committees:
            congress = committee.get('congress')
            if congress == 119:
                filtered.append(committee)
        
        print(f"📊 119th Congress committees: {len(filtered)}")
        return filtered
    
    def process_committee_data(self, committees: List[Dict]) -> List[Dict]:
        """Process and standardize committee data"""
        print("\n🔧 Processing Committee Data")
        print("=" * 50)
        
        processed = []
        
        for committee in committees:
            # Extract and standardize data
            processed_committee = {
                'name': committee.get('name', ''),
                'chamber': committee.get('chamber', ''),
                'congress': committee.get('congress', 119),
                'system_code': committee.get('systemCode', ''),
                'parent_committee_id': committee.get('parentCommitteeId'),
                'type': committee.get('type', ''),
                'url': committee.get('url', ''),
                'is_subcommittee': bool(committee.get('parentCommitteeId')),
                'is_active': True,  # Assume active if from current congress
                'raw_data': committee
            }
            
            processed.append(processed_committee)
        
        print(f"📊 Processed {len(processed)} committees")
        return processed
    
    def create_committee_update_sql(self, committees: List[Dict]) -> str:
        """Create SQL statements for committee updates"""
        print("\n📝 Creating Committee Update SQL")
        print("=" * 50)
        
        sql_statements = []
        
        # Clear existing committees (optional - depends on strategy)
        # sql_statements.append("DELETE FROM committees WHERE congress_session = 119;")
        
        for committee in committees:
            # Insert statement
            insert_sql = f"""
            INSERT INTO committees (
                name, chamber, committee_code, congress_gov_id, is_active, 
                is_subcommittee, parent_committee_id, website, created_at
            ) VALUES (
                '{committee['name'].replace("'", "''")}',
                '{committee['chamber']}',
                '{committee['system_code']}',
                '{committee['url']}',
                {committee['is_active']},
                {committee['is_subcommittee']},
                {committee['parent_committee_id'] if committee['parent_committee_id'] else 'NULL'},
                '{committee['url']}',
                NOW()
            ) ON CONFLICT (name, chamber) DO UPDATE SET
                committee_code = EXCLUDED.committee_code,
                congress_gov_id = EXCLUDED.congress_gov_id,
                is_active = EXCLUDED.is_active,
                is_subcommittee = EXCLUDED.is_subcommittee,
                parent_committee_id = EXCLUDED.parent_committee_id,
                website = EXCLUDED.website,
                updated_at = NOW();
            """
            
            sql_statements.append(insert_sql)
        
        full_sql = "\n".join(sql_statements)
        
        # Save to file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        sql_file = f"phase3_committee_updates_{timestamp}.sql"
        
        with open(sql_file, 'w') as f:
            f.write(full_sql)
        
        print(f"📝 SQL file created: {sql_file}")
        return sql_file
    
    def deploy_committee_updates(self, sql_file: str) -> bool:
        """Deploy committee updates to production"""
        print("\n🚀 Deploying Committee Updates")
        print("=" * 50)
        
        # First, create a backup
        backup_cmd = f"""
        gcloud sql export sql congressional-db \
        gs://congressional-data-backups/committees_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql \
        --database=congress_data \
        --table=committees
        """
        
        success, output = self.run_command(backup_cmd, "Creating database backup")
        if not success:
            print("❌ Backup failed - aborting deployment")
            return False
        
        # Execute the SQL updates
        execute_cmd = f"""
        gcloud sql connect congressional-db --user=postgres --quiet << 'EOF'
        \\c congress_data
        \\i {sql_file}
        EOF
        """
        
        success, output = self.run_command(execute_cmd, "Executing committee updates")
        return success
    
    def validate_deployment(self) -> bool:
        """Validate the committee deployment"""
        print("\n✅ Validating Committee Deployment")
        print("=" * 50)
        
        # Test API endpoint
        committee_data = self.test_api_endpoint(
            f"{self.api_base_url}/committees?limit=10",
            "Committee API endpoint"
        )
        
        if not committee_data:
            print("❌ API validation failed")
            return False
        
        # Test performance
        start_time = time.time()
        response = requests.get(f"{self.api_base_url}/committees?limit=100", timeout=10)
        duration = time.time() - start_time
        
        if response.status_code == 200:
            print(f"✅ Performance test: {duration:.3f}s for 100 committees")
            if duration > 1.0:
                print("⚠️  Performance warning: response time > 1s")
        else:
            print(f"❌ Performance test failed: {response.status_code}")
            return False
        
        return True
    
    async def execute_phase3(self):
        """Execute complete Phase 3 implementation"""
        print("🚀 Phase 3: Complete Committee Structure Expansion")
        print("=" * 60)
        
        # Phase 3A: Assessment (already done above)
        print("\n📋 Phase 3A: Assessment Complete")
        
        # Phase 3B: Data Collection
        print("\n📋 Phase 3B: Data Collection")
        committees = await self.fetch_congress_committees()
        
        if not committees:
            print("❌ No committees collected - aborting")
            return False
        
        # Phase 3C: Data Processing
        print("\n📋 Phase 3C: Data Processing")
        analysis = self.analyze_committee_structure(committees)
        
        # Filter for 119th Congress
        congress_119_committees = self.filter_119th_congress_committees(committees)
        
        # Process data
        processed_committees = self.process_committee_data(congress_119_committees)
        
        # Phase 3D: Database Integration
        print("\n📋 Phase 3D: Database Integration")
        sql_file = self.create_committee_update_sql(processed_committees)
        
        # Save results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        results_file = f"phase3_results_{timestamp}.json"
        
        self.results = {
            'execution_time': timestamp,
            'total_committees_collected': len(committees),
            'congress_119_committees': len(congress_119_committees),
            'processed_committees': len(processed_committees),
            'analysis': analysis,
            'sql_file': sql_file,
            'status': 'completed'
        }
        
        with open(results_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n📊 Phase 3 Results saved to: {results_file}")
        
        # Phase 3E: Deployment (optional - requires user confirmation)
        print("\n📋 Phase 3E: Deployment Ready")
        print(f"✅ {len(processed_committees)} committees ready for deployment")
        print(f"📝 SQL file: {sql_file}")
        print("\n🎯 Next Steps:")
        print("1. Review the generated SQL file")
        print("2. Execute deployment if satisfied")
        print("3. Validate API performance")
        
        return True

def main():
    """Main execution function"""
    print("🚀 Phase 3: Complete Committee Structure Expansion")
    print("=" * 60)
    
    # Initialize implementation
    phase3 = Phase3Implementation()
    
    # Execute asynchronously
    result = asyncio.run(phase3.execute_phase3())
    
    if result:
        print("\n🎉 Phase 3 Implementation Complete!")
        print("Committee structure expansion ready for deployment.")
    else:
        print("\n❌ Phase 3 Implementation Failed!")
        print("Review errors above and retry.")

if __name__ == "__main__":
    main()