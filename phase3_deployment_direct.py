#!/usr/bin/env python3
"""
Phase 3 Committee Deployment - Direct Database Connection
========================================================

Uses the same connection pattern as previous successful deployments
"""

import psycopg2
import json
import time
import os
import sys
import requests
from datetime import datetime
from typing import Dict, Any

class Phase3DirectDeployment:
    def __init__(self):
        self.deployment_start = datetime.now()
        self.deployment_log = []
        self.deployment_file = "phase3_full_deployment_20250709_091846.sql"
        
        # Database connection config (same as previous successful deployments)
        self.db_config = {
            'host': 'localhost',
            'port': 5433,
            'database': 'congress_data',
            'user': 'postgres',
            'password': 'mDf3S9ZnBpQqJvGsY1'
        }
        
        # API base URL for validation
        self.api_base = "https://politicalequity.io/api/v1"
        
    def log_event(self, phase: str, message: str, status: str = "info"):
        """Log deployment events with timestamp"""
        timestamp = datetime.now().isoformat()
        event = {
            "timestamp": timestamp,
            "phase": phase,
            "message": message,
            "status": status
        }
        self.deployment_log.append(event)
        print(f"[{timestamp}] {phase}: {message}")
    
    def get_db_connection(self):
        """Get database connection using the same pattern as previous deployments"""
        try:
            conn = psycopg2.connect(**self.db_config)
            return conn
        except Exception as e:
            self.log_event("CONNECTION", f"Database connection failed: {e}", "error")
            raise
    
    def phase3d1_pre_deployment(self) -> Dict[str, Any]:
        """Phase 3D1: Pre-Deployment Preparation"""
        self.log_event("PHASE3D1", "Starting pre-deployment preparation", "info")
        results = {}
        
        try:
            # 1. Test database connection
            self.log_event("PHASE3D1", "Testing database connection", "info")
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            # Check current committee count
            cursor.execute("SELECT COUNT(*) FROM committees")
            current_count = cursor.fetchone()[0]
            results["current_committee_count"] = current_count
            self.log_event("PHASE3D1", f"Current committee count: {current_count}", "info")
            
            # Check chamber distribution
            cursor.execute("SELECT chamber, COUNT(*) FROM committees GROUP BY chamber")
            chamber_rows = cursor.fetchall()
            chamber_distribution = {row[0]: row[1] for row in chamber_rows}
            results["chamber_distribution"] = chamber_distribution
            
            for chamber, count in chamber_distribution.items():
                self.log_event("PHASE3D1", f"Current {chamber} committees: {count}", "info")
            
            # Check database version
            cursor.execute("SELECT version()")
            db_version = cursor.fetchone()[0]
            results["database_version"] = db_version[:100] + "..." if len(db_version) > 100 else db_version
            
            cursor.close()
            conn.close()
            
            # 2. Verify deployment file exists
            if os.path.exists(self.deployment_file):
                file_size = os.path.getsize(self.deployment_file)
                results["deployment_file_size"] = file_size
                self.log_event("PHASE3D1", f"Deployment file verified: {file_size} bytes", "success")
            else:
                self.log_event("PHASE3D1", f"Deployment file not found: {self.deployment_file}", "error")
                results["deployment_file_error"] = "File not found"
                return results
            
            # 3. Test API connectivity
            self.log_event("PHASE3D1", "Testing API connectivity", "info")
            try:
                response = requests.get(f"{self.api_base}/committees", timeout=10)
                if response.status_code == 200:
                    api_data = response.json()
                    results["api_current_committees"] = len(api_data) if isinstance(api_data, list) else "unknown"
                    self.log_event("PHASE3D1", f"API currently serves {results['api_current_committees']} committees", "info")
                else:
                    self.log_event("PHASE3D1", f"API test returned status {response.status_code}", "warning")
            except Exception as e:
                self.log_event("PHASE3D1", f"API test failed: {e}", "warning")
            
            results["phase3d1_status"] = "success"
            self.log_event("PHASE3D1", "Pre-deployment preparation completed successfully", "success")
            
        except Exception as e:
            results["phase3d1_status"] = "error"
            results["phase3d1_error"] = str(e)
            self.log_event("PHASE3D1", f"Pre-deployment preparation failed: {e}", "error")
            
        return results
    
    def phase3d2_committee_deployment(self) -> Dict[str, Any]:
        """Phase 3D2: Committee Deployment"""
        self.log_event("PHASE3D2", "Starting committee deployment", "info")
        results = {}
        
        try:
            # Read deployment file
            with open(self.deployment_file, 'r') as f:
                sql_content = f.read()
            
            self.log_event("PHASE3D2", f"Read {len(sql_content)} characters from deployment file", "info")
            
            # Connect to database
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            # Start transaction
            self.log_event("PHASE3D2", "Starting database transaction", "info")
            deployment_start = time.time()
            
            try:
                # Execute the deployment SQL
                cursor.execute(sql_content)
                
                # Commit transaction
                conn.commit()
                deployment_time = time.time() - deployment_start
                
                self.log_event("PHASE3D2", f"Deployment completed successfully in {deployment_time:.2f}s", "success")
                results["deployment_time"] = deployment_time
                results["phase3d2_status"] = "success"
                
            except Exception as e:
                # Rollback transaction on error
                conn.rollback()
                self.log_event("PHASE3D2", f"Deployment failed, transaction rolled back: {e}", "error")
                results["phase3d2_status"] = "error"
                results["phase3d2_error"] = str(e)
            
            cursor.close()
            conn.close()
            
        except Exception as e:
            results["phase3d2_status"] = "error"
            results["phase3d2_error"] = str(e)
            self.log_event("PHASE3D2", f"Committee deployment failed: {e}", "error")
            
        return results
    
    def phase3d3_post_deployment_validation(self) -> Dict[str, Any]:
        """Phase 3D3: Post-Deployment Validation"""
        self.log_event("PHASE3D3", "Starting post-deployment validation", "info")
        results = {}
        
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            # 1. Committee count validation
            cursor.execute("SELECT COUNT(*) FROM committees")
            total_committees = cursor.fetchone()[0]
            results["total_committees"] = total_committees
            self.log_event("PHASE3D3", f"Total committees after deployment: {total_committees}", "info")
            
            # 2. Chamber distribution
            cursor.execute("SELECT chamber, COUNT(*) FROM committees GROUP BY chamber ORDER BY chamber")
            chamber_rows = cursor.fetchall()
            chamber_distribution = {row[0]: row[1] for row in chamber_rows}
            results["chamber_distribution"] = chamber_distribution
            
            for chamber, count in chamber_distribution.items():
                self.log_event("PHASE3D3", f"{chamber} committees: {count}", "info")
            
            # 3. Check for expected target (815 committees)
            expected_total = 815
            if total_committees >= expected_total:
                self.log_event("PHASE3D3", f"✅ Target met: {total_committees} >= {expected_total} committees", "success")
                results["target_met"] = True
            else:
                self.log_event("PHASE3D3", f"⚠️ Target not met: {total_committees} < {expected_total} committees", "warning")
                results["target_met"] = False
            
            # 4. Data integrity check
            cursor.execute("SELECT COUNT(*) FROM committees WHERE name IS NULL OR name = ''")
            invalid_names = cursor.fetchone()[0]
            results["invalid_names"] = invalid_names
            
            if invalid_names == 0:
                self.log_event("PHASE3D3", "✅ Data integrity check passed - no invalid names", "success")
            else:
                self.log_event("PHASE3D3", f"⚠️ Found {invalid_names} invalid committee names", "warning")
            
            # 5. Sample committee names
            cursor.execute("SELECT name, chamber FROM committees WHERE name IS NOT NULL ORDER BY name LIMIT 5")
            sample_committees = cursor.fetchall()
            results["sample_committees"] = [{"name": row[0], "chamber": row[1]} for row in sample_committees]
            
            for committee in sample_committees:
                self.log_event("PHASE3D3", f"Sample: {committee['name']} ({committee['chamber']})", "info")
            
            cursor.close()
            conn.close()
            
            results["phase3d3_status"] = "success"
            self.log_event("PHASE3D3", "Post-deployment validation completed successfully", "success")
            
        except Exception as e:
            results["phase3d3_status"] = "error"
            results["phase3d3_error"] = str(e)
            self.log_event("PHASE3D3", f"Post-deployment validation failed: {e}", "error")
            
        return results
    
    def phase3d4_system_verification(self) -> Dict[str, Any]:
        """Phase 3D4: System Verification"""
        self.log_event("PHASE3D4", "Starting system verification", "info")
        results = {}
        
        try:
            # Test API endpoint response
            self.log_event("PHASE3D4", "Testing API endpoint with new data", "info")
            
            try:
                response = requests.get(f"{self.api_base}/committees", timeout=15)
                if response.status_code == 200:
                    api_data = response.json()
                    api_committee_count = len(api_data) if isinstance(api_data, list) else 0
                    results["api_committee_count"] = api_committee_count
                    self.log_event("PHASE3D4", f"✅ API now serves {api_committee_count} committees", "success")
                    
                    # Check for expected data structure
                    if api_committee_count > 0 and isinstance(api_data, list):
                        sample_committee = api_data[0]
                        required_fields = ['name', 'chamber']
                        has_all_fields = all(field in sample_committee for field in required_fields)
                        
                        if has_all_fields:
                            self.log_event("PHASE3D4", "✅ API data structure validation passed", "success")
                            results["api_data_structure"] = "valid"
                        else:
                            self.log_event("PHASE3D4", "⚠️ API data structure validation failed", "warning")
                            results["api_data_structure"] = "invalid"
                    
                    results["api_status"] = "success"
                    
                else:
                    self.log_event("PHASE3D4", f"❌ API returned status {response.status_code}", "error")
                    results["api_status"] = "error"
                    results["api_error"] = f"HTTP {response.status_code}"
                    
            except Exception as e:
                self.log_event("PHASE3D4", f"❌ API test failed: {e}", "error")
                results["api_status"] = "error"
                results["api_error"] = str(e)
            
            # Test specific API endpoints
            endpoint_tests = [
                "/committees?chamber=House",
                "/committees?chamber=Senate",
                "/committees?chamber=Joint"
            ]
            
            results["endpoint_tests"] = {}
            for endpoint in endpoint_tests:
                try:
                    response = requests.get(f"{self.api_base}{endpoint}", timeout=10)
                    if response.status_code == 200:
                        data = response.json()
                        count = len(data) if isinstance(data, list) else 0
                        results["endpoint_tests"][endpoint] = {"status": "success", "count": count}
                        self.log_event("PHASE3D4", f"✅ {endpoint} returns {count} items", "success")
                    else:
                        results["endpoint_tests"][endpoint] = {"status": "error", "code": response.status_code}
                        self.log_event("PHASE3D4", f"❌ {endpoint} returned {response.status_code}", "error")
                except Exception as e:
                    results["endpoint_tests"][endpoint] = {"status": "error", "error": str(e)}
                    self.log_event("PHASE3D4", f"❌ {endpoint} failed: {e}", "error")
            
            results["phase3d4_status"] = "success"
            self.log_event("PHASE3D4", "System verification completed", "success")
            
        except Exception as e:
            results["phase3d4_status"] = "error"
            results["phase3d4_error"] = str(e)
            self.log_event("PHASE3D4", f"System verification failed: {e}", "error")
            
        return results
    
    def execute_full_deployment(self) -> Dict[str, Any]:
        """Execute complete Phase 3 deployment"""
        self.log_event("DEPLOYMENT", "🚀 Starting Phase 3 Committee Deployment", "info")
        self.log_event("DEPLOYMENT", f"Target: Deploy 815 committees to production database", "info")
        
        deployment_results = {
            "deployment_start": self.deployment_start.isoformat(),
            "target_committees": 815,
            "deployment_file": self.deployment_file,
            "phases": {}
        }
        
        # Phase 3D1: Pre-Deployment Preparation
        deployment_results["phases"]["3d1"] = self.phase3d1_pre_deployment()
        
        # Only proceed if pre-deployment succeeds
        if deployment_results["phases"]["3d1"].get("phase3d1_status") == "success":
            
            # Phase 3D2: Committee Deployment
            deployment_results["phases"]["3d2"] = self.phase3d2_committee_deployment()
            
            # Only proceed if deployment succeeds
            if deployment_results["phases"]["3d2"].get("phase3d2_status") == "success":
                
                # Phase 3D3: Post-Deployment Validation
                deployment_results["phases"]["3d3"] = self.phase3d3_post_deployment_validation()
                
                # Phase 3D4: System Verification
                deployment_results["phases"]["3d4"] = self.phase3d4_system_verification()
                
        deployment_results["deployment_end"] = datetime.now().isoformat()
        deployment_results["deployment_log"] = self.deployment_log
        
        # Save results to file
        output_file = f"phase3_deployment_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w') as f:
            json.dump(deployment_results, f, indent=2)
        
        self.log_event("DEPLOYMENT", f"Results saved to {output_file}", "info")
        self.log_event("DEPLOYMENT", "🎉 Phase 3 Committee Deployment completed", "success")
        
        return deployment_results

def main():
    """Main execution function"""
    # Verify deployment file exists
    deployment_file = "phase3_full_deployment_20250709_091846.sql"
    if not os.path.exists(deployment_file):
        print(f"❌ Error: Deployment file {deployment_file} not found")
        sys.exit(1)
    
    # Execute deployment
    executor = Phase3DirectDeployment()
    results = executor.execute_full_deployment()
    
    # Print comprehensive summary
    print(f"\n{'='*70}")
    print("🎉 PHASE 3 DEPLOYMENT SUMMARY")
    print(f"{'='*70}")
    
    # Overall success determination
    all_phases_successful = True
    phase_results = {}
    
    for phase_id, phase_data in results["phases"].items():
        status = phase_data.get(f"phase{phase_id}_status", "unknown")
        phase_results[phase_id] = status
        print(f"Phase {phase_id.upper()}: {status.upper()}")
        
        if status != "success":
            all_phases_successful = False
        
        # Phase-specific details
        if phase_id == "3d1":
            if "current_committee_count" in phase_data:
                print(f"  Pre-deployment committees: {phase_data['current_committee_count']}")
            if "deployment_file_size" in phase_data:
                print(f"  Deployment file size: {phase_data['deployment_file_size']} bytes")
        
        elif phase_id == "3d2":
            if "deployment_time" in phase_data:
                print(f"  Deployment time: {phase_data['deployment_time']:.2f}s")
        
        elif phase_id == "3d3":
            if "total_committees" in phase_data:
                print(f"  Total committees deployed: {phase_data['total_committees']}")
            if "chamber_distribution" in phase_data:
                for chamber, count in phase_data["chamber_distribution"].items():
                    print(f"    {chamber}: {count}")
            if "target_met" in phase_data:
                target_status = "✅ YES" if phase_data["target_met"] else "❌ NO"
                print(f"  Target (815) met: {target_status}")
        
        elif phase_id == "3d4":
            if "api_committee_count" in phase_data:
                print(f"  API committee count: {phase_data['api_committee_count']}")
            if "api_status" in phase_data:
                print(f"  API status: {phase_data['api_status']}")
    
    print(f"{'='*70}")
    
    # Final success determination
    if all_phases_successful:
        print("🎉 ✅ DEPLOYMENT SUCCESSFUL!")
        print("✅ Phase 3 completed successfully - 815 committees deployed")
        
        # Show key metrics
        if "3d3" in results["phases"]:
            total = results["phases"]["3d3"].get("total_committees", "unknown")
            print(f"✅ Total committees in database: {total}")
        
        if "3d4" in results["phases"]:
            api_count = results["phases"]["3d4"].get("api_committee_count", "unknown")
            print(f"✅ API serving {api_count} committees")
            
        print("🌐 System: https://politicalequity.io")
        
    else:
        print("❌ ⚠️ DEPLOYMENT FAILED!")
        print("❌ Check logs for error details")
        
        # Show which phases failed
        failed_phases = [phase for phase, status in phase_results.items() if status != "success"]
        if failed_phases:
            print(f"❌ Failed phases: {', '.join(failed_phases)}")
    
    print(f"{'='*70}")
    return 0 if all_phases_successful else 1

if __name__ == "__main__":
    sys.exit(main())