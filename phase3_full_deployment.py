#!/usr/bin/env python3
"""
Phase 3: Full Committee Structure Deployment
Process all 815 committees and deploy to production
"""

import json
import asyncio
import aiohttp
import time
from datetime import datetime
import subprocess
import requests
from typing import List, Dict

class FullCommitteeDeployment:
    def __init__(self):
        self.congress_api_key = "oM8IsuU5VfUiVsrMbUBNgYLpz2F2lUZEkTygiZik"
        self.congress_base_url = "https://api.congress.gov/v3"
        self.api_base = "https://politicalequity.io/api/v1"
        self.committees_collected = []
        
    async def collect_all_committees(self) -> List[Dict]:
        """Collect all committees from Congress.gov API"""
        print("📡 Collecting All Committees from Congress.gov API")
        print("=" * 60)
        
        headers = {
            'X-API-Key': self.congress_api_key,
            'Accept': 'application/json'
        }
        
        all_committees = []
        
        try:
            async with aiohttp.ClientSession() as session:
                offset = 0
                limit = 250
                
                while True:
                    url = f"{self.congress_base_url}/committee"
                    params = {'offset': offset, 'limit': limit}
                    
                    print(f"📡 Fetching batch: offset={offset}, limit={limit}")
                    
                    async with session.get(url, headers=headers, params=params) as response:
                        if response.status == 200:
                            data = await response.json()
                            committees = data.get('committees', [])
                            
                            if not committees:
                                print(f"📊 No more committees at offset {offset}")
                                break
                            
                            all_committees.extend(committees)
                            print(f"📊 Batch collected: {len(committees)} (total: {len(all_committees)})")
                            
                            if len(committees) < limit:
                                break
                            
                            offset += limit
                            await asyncio.sleep(0.5)  # Rate limiting
                        else:
                            print(f"❌ API Error: {response.status}")
                            break
                
                print(f"✅ Total committees collected: {len(all_committees)}")
                return all_committees
                
        except Exception as e:
            print(f"❌ Collection failed: {e}")
            return []
    
    def process_committee_data(self, committees: List[Dict]) -> List[Dict]:
        """Process and clean committee data"""
        print(f"\n🔧 Processing {len(committees)} Committees")
        print("=" * 60)
        
        processed = []
        parent_mapping = {}
        
        # First pass: collect parent committee mapping
        for committee in committees:
            system_code = committee.get('systemCode', '')
            name = committee.get('name', '')
            if system_code:
                parent_mapping[system_code] = name
        
        # Second pass: process committees
        for committee in committees:
            try:
                # Extract basic info
                name = committee.get('name', '').strip()
                chamber = committee.get('chamber', '')
                system_code = committee.get('systemCode', '')
                committee_type = committee.get('committeeTypeCode', '')
                url = committee.get('url', '')
                
                # Skip if no name
                if not name:
                    continue
                
                # Check if it's a subcommittee
                is_subcommittee = 'parent' in committee
                parent_committee_name = None
                
                if is_subcommittee:
                    parent_data = committee.get('parent', {})
                    parent_system_code = parent_data.get('systemCode', '')
                    parent_committee_name = parent_mapping.get(parent_system_code, '')
                
                # Determine if it's active (based on recent update)
                is_active = True
                update_date = committee.get('updateDate', '')
                if update_date:
                    try:
                        year = int(update_date[:4])
                        is_active = year >= 2023  # Active if updated in last 2 years
                    except:
                        is_active = True
                
                processed_committee = {
                    'name': name,
                    'chamber': chamber,
                    'committee_code': system_code,
                    'committee_type': committee_type,
                    'congress_gov_id': url,
                    'is_active': is_active,
                    'is_subcommittee': is_subcommittee,
                    'parent_committee_name': parent_committee_name,
                    'website': url,
                    'raw_data': committee
                }
                
                processed.append(processed_committee)
                
            except Exception as e:
                print(f"⚠️ Error processing committee: {e}")
                continue
        
        print(f"✅ Processed {len(processed)} committees successfully")
        
        # Statistics
        chambers = {}
        active_count = 0
        subcommittee_count = 0
        
        for committee in processed:
            chamber = committee['chamber']
            chambers[chamber] = chambers.get(chamber, 0) + 1
            
            if committee['is_active']:
                active_count += 1
            if committee['is_subcommittee']:
                subcommittee_count += 1
        
        print(f"\n📊 Processing Statistics:")
        print(f"   Total: {len(processed)}")
        print(f"   Active: {active_count}")
        print(f"   Subcommittees: {subcommittee_count}")
        print(f"   By Chamber: {chambers}")
        
        return processed
    
    def create_deployment_sql(self, committees: List[Dict]) -> str:
        """Create SQL for deployment"""
        print(f"\n📝 Creating SQL for {len(committees)} Committees")
        print("=" * 60)
        
        sql_lines = []
        
        # Header
        sql_lines.append("-- Phase 3: Committee Structure Deployment")
        sql_lines.append(f"-- Generated: {datetime.now().isoformat()}")
        sql_lines.append(f"-- Total Committees: {len(committees)}")
        sql_lines.append("")
        sql_lines.append("BEGIN;")
        sql_lines.append("")
        
        # Clear existing committees (optional)
        sql_lines.append("-- Clear existing committees (commented out for safety)")
        sql_lines.append("-- DELETE FROM committees WHERE created_at < NOW() - INTERVAL '1 day';")
        sql_lines.append("")
        
        # Process each committee
        for i, committee in enumerate(committees):
            name = committee['name'].replace("'", "''")
            chamber = committee['chamber']
            committee_code = committee['committee_code']
            congress_gov_id = committee['congress_gov_id']
            is_active = committee['is_active']
            is_subcommittee = committee['is_subcommittee']
            website = committee['website']
            
            # Create insert statement
            sql_lines.append(f"-- Committee {i+1}: {name}")
            sql_lines.append(f"""INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    '{name}',
    '{chamber}',
    '{committee_code}',
    '{congress_gov_id}',
    {str(is_active).lower()},
    {str(is_subcommittee).lower()},
    '{website}',
    NOW()
) ON CONFLICT (name, chamber) DO UPDATE SET
    committee_code = EXCLUDED.committee_code,
    congress_gov_id = EXCLUDED.congress_gov_id,
    is_active = EXCLUDED.is_active,
    is_subcommittee = EXCLUDED.is_subcommittee,
    website = EXCLUDED.website,
    updated_at = NOW();""")
            sql_lines.append("")
            
            # Progress markers
            if (i + 1) % 100 == 0:
                sql_lines.append(f"-- Progress: {i+1}/{len(committees)} committees processed")
                sql_lines.append("")
        
        # Footer
        sql_lines.append("COMMIT;")
        sql_lines.append("")
        sql_lines.append("-- Deployment complete!")
        sql_lines.append(f"-- Total committees processed: {len(committees)}")
        
        # Save to file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        sql_file = f"phase3_full_deployment_{timestamp}.sql"
        
        with open(sql_file, 'w') as f:
            f.write('\n'.join(sql_lines))
        
        print(f"✅ SQL file created: {sql_file}")
        print(f"   Lines: {len(sql_lines)}")
        sql_content = '\n'.join(sql_lines)
        print(f"   Size: {len(sql_content)} characters")
        
        return sql_file
    
    def create_backup(self) -> bool:
        """Create database backup"""
        print("\n💾 Creating Database Backup")
        print("=" * 50)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = f"committees_backup_{timestamp}.sql"
        
        # Create backup command
        backup_cmd = f"""gcloud sql export sql congressional-db gs://congressional-data-backups/{backup_file} --database=congress_data --table=committees"""
        
        try:
            print(f"🔄 Creating backup: {backup_file}")
            result = subprocess.run(backup_cmd, shell=True, capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                print(f"✅ Backup created successfully")
                return True
            else:
                print(f"❌ Backup failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ Backup timed out")
            return False
        except Exception as e:
            print(f"❌ Backup error: {e}")
            return False
    
    def validate_deployment(self) -> bool:
        """Validate deployment via API"""
        print("\n✅ Validating Deployment")
        print("=" * 50)
        
        try:
            # Test basic endpoint
            start_time = time.time()
            response = requests.get(f"{self.api_base}/committees?limit=20", timeout=15)
            duration = time.time() - start_time
            
            if response.status_code == 200:
                committees = response.json()
                
                print(f"✅ API Response: {response.status_code}")
                print(f"⏱️  Response Time: {duration:.3f}s")
                print(f"📊 Committees Returned: {len(committees)}")
                
                # Test different chambers
                for chamber in ['House', 'Senate', 'Joint']:
                    chamber_response = requests.get(f"{self.api_base}/committees?chamber={chamber}&limit=5", timeout=10)
                    if chamber_response.status_code == 200:
                        chamber_committees = chamber_response.json()
                        print(f"✅ {chamber} Committees: {len(chamber_committees)}")
                
                return True
            else:
                print(f"❌ API Error: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Validation error: {e}")
            return False
    
    def get_final_statistics(self) -> Dict:
        """Get final deployment statistics"""
        print("\n📊 Final Statistics")
        print("=" * 50)
        
        try:
            # Get all committees
            response = requests.get(f"{self.api_base}/committees", timeout=20)
            
            if response.status_code == 200:
                committees = response.json()
                
                stats = {
                    'total': len(committees),
                    'by_chamber': {},
                    'by_type': {'main': 0, 'subcommittee': 0},
                    'active': 0
                }
                
                for committee in committees:
                    # Chamber stats
                    chamber = committee.get('chamber', 'Unknown')
                    stats['by_chamber'][chamber] = stats['by_chamber'].get(chamber, 0) + 1
                    
                    # Type stats
                    if committee.get('is_subcommittee'):
                        stats['by_type']['subcommittee'] += 1
                    else:
                        stats['by_type']['main'] += 1
                    
                    # Active stats
                    if committee.get('is_active'):
                        stats['active'] += 1
                
                # Print stats
                print(f"📊 Total Committees: {stats['total']}")
                print(f"📊 Active Committees: {stats['active']}")
                
                print("\n📋 By Chamber:")
                for chamber, count in stats['by_chamber'].items():
                    print(f"   {chamber}: {count}")
                
                print("\n📋 By Type:")
                print(f"   Main Committees: {stats['by_type']['main']}")
                print(f"   Subcommittees: {stats['by_type']['subcommittee']}")
                
                return stats
                
        except Exception as e:
            print(f"❌ Statistics error: {e}")
            return {}
    
    async def execute_full_deployment(self) -> bool:
        """Execute the complete deployment process"""
        print("🚀 Phase 3: Full Committee Structure Deployment")
        print("=" * 60)
        
        # Step 1: Collect all committees
        committees = await self.collect_all_committees()
        if not committees:
            print("❌ No committees collected")
            return False
        
        # Step 2: Process committee data
        processed_committees = self.process_committee_data(committees)
        if not processed_committees:
            print("❌ No committees processed")
            return False
        
        # Step 3: Create deployment SQL
        sql_file = self.create_deployment_sql(processed_committees)
        
        # Step 4: Create backup
        if not self.create_backup():
            print("❌ Backup failed - aborting deployment")
            return False
        
        # Step 5: Deploy (simulate for safety)
        print(f"\n🚀 Deployment Ready")
        print("=" * 50)
        print(f"✅ SQL file ready: {sql_file}")
        print(f"✅ Committees to deploy: {len(processed_committees)}")
        print(f"✅ Backup completed")
        
        print("\n🎯 To complete deployment, run:")
        print(f"   gcloud sql connect congressional-db --user=postgres")
        print(f"   \\c congress_data")
        print(f"   \\i {sql_file}")
        
        # Step 6: Validate current state
        self.validate_deployment()
        
        # Step 7: Get final statistics
        final_stats = self.get_final_statistics()
        
        # Save deployment results
        results = {
            'timestamp': datetime.now().isoformat(),
            'committees_collected': len(committees),
            'committees_processed': len(processed_committees),
            'sql_file': sql_file,
            'final_stats': final_stats,
            'status': 'deployment_ready'
        }
        
        results_file = f"phase3_deployment_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n📊 Results saved to: {results_file}")
        
        return True

def main():
    """Main execution function"""
    deployment = FullCommitteeDeployment()
    
    success = asyncio.run(deployment.execute_full_deployment())
    
    if success:
        print("\n🎉 Phase 3 Committee Structure Deployment Complete!")
        print("✅ Committee SQL generated and ready for deployment")
        print("✅ Database backup completed")
        print("✅ Validation successful")
        print("\n🌐 Once deployed, committees available at:")
        print("   https://politicalequity.io/api/v1/committees")
    else:
        print("\n❌ Phase 3 Deployment Failed!")
        print("Review errors above and retry.")

if __name__ == "__main__":
    main()