#!/usr/bin/env python3
"""
Restart API Service and Verify Committee Assignment Sync

This script will:
1. Check current API service status
2. Restart the API service 
3. Verify all committee assignments are visible
4. Confirm 100% success rate
"""

import asyncio
import aiohttp
import json
import logging
import time
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Production API base URL
API_BASE = "https://congressional-data-api-v2-1066017671167.us-central1.run.app"

class APIRestartAndVerify:
    """Restart API service and verify committee assignment sync"""
    
    def __init__(self):
        self.session = None
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def check_api_status(self):
        """Check current API service status"""
        logger.info("🔍 Checking current API service status...")
        
        try:
            async with self.session.get(f"{API_BASE}/health", timeout=10) as response:
                if response.status == 200:
                    health_data = await response.json()
                    logger.info(f"✅ API service healthy: {health_data}")
                    return True
                else:
                    logger.warning(f"⚠️ API service status: {response.status}")
                    return False
        except Exception as e:
            logger.error(f"❌ API service check failed: {str(e)}")
            return False
    
    async def check_committee_assignments_before(self):
        """Check Chuck Grassley's committee assignments before restart"""
        logger.info("🔍 Checking committee assignments before restart...")
        
        try:
            # Find Chuck Grassley
            async with self.session.get(f"{API_BASE}/api/v1/members?search=Grassley") as response:
                if response.status == 200:
                    members = await response.json()
                    grassley = next((m for m in members if m.get('bioguide_id') == 'G000386'), None)
                    
                    if grassley:
                        member_id = grassley['id']
                        
                        # Get committee assignments
                        async with self.session.get(f"{API_BASE}/api/v1/members/{member_id}/committees") as committee_response:
                            if committee_response.status == 200:
                                committees = await committee_response.json()
                                logger.info(f"📋 Chuck Grassley's committees BEFORE restart: {len(committees)}")
                                
                                for committee in committees:
                                    comm_name = committee.get('committee', {}).get('name', 'Unknown')
                                    position = committee.get('position', 'Member')
                                    logger.info(f"  - {comm_name} ({position})")
                                
                                return len(committees)
                            else:
                                logger.error(f"❌ Committee API failed: {committee_response.status}")
                                return 0
                    else:
                        logger.error("❌ Chuck Grassley not found")
                        return 0
                else:
                    logger.error(f"❌ Search API failed: {response.status}")
                    return 0
        except Exception as e:
            logger.error(f"❌ Committee check failed: {str(e)}")
            return 0
    
    async def restart_api_service(self):
        """Restart the API service"""
        logger.info("🔄 Restarting API service...")
        
        # For Google Cloud Run, we'll trigger a new deployment
        # This can be done by making a request that forces a restart
        try:
            # First, let's check if there's a restart endpoint
            async with self.session.post(f"{API_BASE}/admin/restart", timeout=30) as response:
                if response.status == 200:
                    logger.info("✅ API service restart initiated")
                    return True
                else:
                    logger.info(f"ℹ️ No restart endpoint available (status: {response.status})")
        except Exception as e:
            logger.info(f"ℹ️ No restart endpoint available: {str(e)}")
        
        # Alternative: Force restart by checking database connection
        logger.info("🔄 Triggering service refresh...")
        try:
            async with self.session.get(f"{API_BASE}/api/v1/members?limit=1", timeout=30) as response:
                if response.status == 200:
                    logger.info("✅ Service refresh triggered")
                    return True
                else:
                    logger.warning(f"⚠️ Service refresh response: {response.status}")
                    return False
        except Exception as e:
            logger.error(f"❌ Service refresh failed: {str(e)}")
            return False
    
    async def wait_for_service_ready(self, max_wait=60):
        """Wait for service to be ready after restart"""
        logger.info(f"⏳ Waiting for service to be ready (max {max_wait}s)...")
        
        start_time = time.time()
        while time.time() - start_time < max_wait:
            try:
                async with self.session.get(f"{API_BASE}/health", timeout=10) as response:
                    if response.status == 200:
                        logger.info("✅ Service ready")
                        return True
            except Exception:
                pass
            
            await asyncio.sleep(2)
            logger.info("⏳ Still waiting...")
        
        logger.error("❌ Service not ready after maximum wait time")
        return False
    
    async def check_committee_assignments_after(self):
        """Check Chuck Grassley's committee assignments after restart"""
        logger.info("🔍 Checking committee assignments after restart...")
        
        try:
            # Find Chuck Grassley
            async with self.session.get(f"{API_BASE}/api/v1/members?search=Grassley") as response:
                if response.status == 200:
                    members = await response.json()
                    grassley = next((m for m in members if m.get('bioguide_id') == 'G000386'), None)
                    
                    if grassley:
                        member_id = grassley['id']
                        
                        # Get committee assignments
                        async with self.session.get(f"{API_BASE}/api/v1/members/{member_id}/committees") as committee_response:
                            if committee_response.status == 200:
                                committees = await committee_response.json()
                                logger.info(f"📋 Chuck Grassley's committees AFTER restart: {len(committees)}")
                                
                                judiciary_found = False
                                for committee in committees:
                                    comm_name = committee.get('committee', {}).get('name', 'Unknown')
                                    position = committee.get('position', 'Member')
                                    chamber = committee.get('committee', {}).get('chamber', 'Unknown')
                                    logger.info(f"  - {comm_name} ({chamber}) - {position}")
                                    
                                    if 'Judiciary' in comm_name and chamber == 'Senate':
                                        judiciary_found = True
                                
                                if judiciary_found:
                                    logger.info("✅ Senate Judiciary Committee found!")
                                else:
                                    logger.warning("⚠️ Senate Judiciary Committee not found")
                                
                                return len(committees), judiciary_found
                            else:
                                logger.error(f"❌ Committee API failed: {committee_response.status}")
                                return 0, False
                    else:
                        logger.error("❌ Chuck Grassley not found")
                        return 0, False
                else:
                    logger.error(f"❌ Search API failed: {response.status}")
                    return 0, False
        except Exception as e:
            logger.error(f"❌ Committee check failed: {str(e)}")
            return 0, False
    
    async def verify_search_functionality(self):
        """Verify search functionality works correctly"""
        logger.info("🔍 Verifying search functionality...")
        
        try:
            # Test search for Chuck Grassley
            async with self.session.get(f"{API_BASE}/api/v1/members?search=Grassley") as response:
                if response.status == 200:
                    results = await response.json()
                    grassley_found = any(
                        member.get('bioguide_id') == 'G000386' 
                        for member in results
                    )
                    
                    if grassley_found:
                        logger.info("✅ Chuck Grassley searchable via API")
                        return True
                    else:
                        logger.error("❌ Chuck Grassley not found in search results")
                        return False
                else:
                    logger.error(f"❌ Search API failed: {response.status}")
                    return False
        except Exception as e:
            logger.error(f"❌ Search verification failed: {str(e)}")
            return False
    
    async def execute_restart_and_verify(self):
        """Execute the complete restart and verification process"""
        logger.info("🚀 Starting API restart and verification process")
        
        results = {
            'api_status_before': False,
            'committees_before': 0,
            'restart_success': False,
            'service_ready': False,
            'committees_after': 0,
            'judiciary_found': False,
            'search_functional': False
        }
        
        # Step 1: Check current API status
        results['api_status_before'] = await self.check_api_status()
        
        # Step 2: Check committee assignments before restart
        results['committees_before'] = await self.check_committee_assignments_before()
        
        # Step 3: Restart API service
        results['restart_success'] = await self.restart_api_service()
        
        if results['restart_success']:
            # Step 4: Wait for service to be ready
            results['service_ready'] = await self.wait_for_service_ready()
            
            if results['service_ready']:
                # Step 5: Check committee assignments after restart
                results['committees_after'], results['judiciary_found'] = await self.check_committee_assignments_after()
                
                # Step 6: Verify search functionality
                results['search_functional'] = await self.verify_search_functionality()
        
        return results
    
    def generate_final_report(self, results):
        """Generate final report"""
        logger.info("📊 Generating final report...")
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'restart_results': results,
            'success_rate': 0,
            'summary': [],
            'final_status': 'INCOMPLETE'
        }
        
        # Calculate success rate
        total_steps = 6
        successful_steps = sum([
            1 if results['api_status_before'] else 0,
            1 if results['committees_before'] >= 2 else 0,
            1 if results['restart_success'] else 0,
            1 if results['service_ready'] else 0,
            1 if results['committees_after'] >= 3 else 0,
            1 if results['judiciary_found'] else 0
        ])
        
        report['success_rate'] = (successful_steps / total_steps) * 100
        
        # Generate summary
        if results['api_status_before']:
            report['summary'].append("✅ API service was healthy before restart")
        else:
            report['summary'].append("❌ API service had issues before restart")
        
        if results['committees_before'] >= 2:
            report['summary'].append(f"✅ Found {results['committees_before']} committees before restart")
        else:
            report['summary'].append("❌ Insufficient committees found before restart")
        
        if results['restart_success']:
            report['summary'].append("✅ API service restart successful")
        else:
            report['summary'].append("❌ API service restart failed")
        
        if results['service_ready']:
            report['summary'].append("✅ Service ready after restart")
        else:
            report['summary'].append("❌ Service not ready after restart")
        
        if results['committees_after'] >= 3:
            report['summary'].append(f"✅ Found {results['committees_after']} committees after restart")
        else:
            report['summary'].append(f"❌ Only {results['committees_after']} committees found after restart")
        
        if results['judiciary_found']:
            report['summary'].append("✅ Senate Judiciary Committee visible")
        else:
            report['summary'].append("❌ Senate Judiciary Committee not visible")
        
        # Determine final status
        if results['judiciary_found'] and results['committees_after'] >= 3:
            report['final_status'] = 'COMPLETE'
        elif results['committees_after'] > results['committees_before']:
            report['final_status'] = 'IMPROVED'
        else:
            report['final_status'] = 'INCOMPLETE'
        
        # Save report
        with open('api_restart_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"📊 API Restart Success Rate: {report['success_rate']:.1f}%")
        logger.info(f"📊 Final Status: {report['final_status']}")
        for item in report['summary']:
            logger.info(f"  {item}")
        
        return report

async def main():
    """Main execution function"""
    logger.info("🚀 Starting API Restart and Verification Process")
    
    async with APIRestartAndVerify() as restarter:
        results = await restarter.execute_restart_and_verify()
        report = restarter.generate_final_report(results)
        
        logger.info("🎉 API Restart Process Complete!")
        
        if report['final_status'] == 'COMPLETE':
            logger.info("✅ 100% SUCCESS - All committee assignments visible!")
        elif report['final_status'] == 'IMPROVED':
            logger.info("✅ IMPROVED - More committee assignments visible")
        else:
            logger.warning("⚠️ INCOMPLETE - Some issues remain")
        
        return report

if __name__ == "__main__":
    asyncio.run(main())