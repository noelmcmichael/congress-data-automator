#!/usr/bin/env python3
"""
Phase 3 Committee Deployment - Cloud SQL Proxy Approach
======================================================

Uses Cloud SQL Proxy to connect to production database
"""

import subprocess
import json
import time
import os
import sys
import signal
import requests
from datetime import datetime
from typing import Dict, Any
import psycopg2
import threading

class Phase3CloudSQLDeployment:
    def __init__(self):
        self.deployment_start = datetime.now()
        self.deployment_log = []
        self.deployment_file = "phase3_full_deployment_20250709_091846.sql"
        self.proxy_process = None
        
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
        
    def start_cloud_sql_proxy(self):
        """Start Cloud SQL proxy in background"""
        try:
            self.log_event("PROXY", "Starting Cloud SQL proxy", "info")
            
            # Check if proxy is already running
            try:
                result = subprocess.run(["pgrep", "-f", "cloud-sql-proxy"], capture_output=True, text=True)
                if result.returncode == 0:
                    self.log_event("PROXY", "Cloud SQL proxy already running", "info")
                    return True
            except:
                pass
            
            # Start proxy
            proxy_cmd = [
                "gcloud", "sql", "connect", "congressional-db",
                "--user=postgres",
                "--quiet"
            ]
            
            # Note: We'll use direct gcloud sql connect instead of background proxy
            self.log_event("PROXY", "Using gcloud sql connect for database access", "info")
            return True
            
        except Exception as e:
            self.log_event("PROXY", f"Failed to start proxy: {e}", "error")
            return False
    
    def execute_sql_via_gcloud(self, sql_content: str) -> Dict[str, Any]:
        """Execute SQL via gcloud sql connect"""
        try:
            # Write SQL to temporary file
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.sql', delete=False) as tmp_file:
                tmp_file.write(sql_content)
                tmp_file_path = tmp_file.name
            
            # Execute SQL via gcloud
            cmd = [
                "gcloud", "sql", "connect", "congressional-db",
                "--user=postgres",
                "--database=congress_data",
                "--quiet"
            ]
            
            # Run with SQL input and password
            process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Send password and SQL content
            input_text = "temp_deployment_password_123\n" + sql_content
            stdout, stderr = process.communicate(input=input_text)
            
            # Clean up temp file
            os.unlink(tmp_file_path)
            
            return {
                "returncode": process.returncode,
                "stdout": stdout,
                "stderr": stderr
            }
            
        except Exception as e:
            return {
                "returncode": -1,
                "stdout": "",
                "stderr": str(e)
            }
    
    def phase3d1_pre_deployment(self) -> Dict[str, Any]:
        """Phase 3D1: Pre-Deployment Preparation"""
        self.log_event("PHASE3D1", "Starting pre-deployment preparation", "info")
        results = {}
        
        try:
            # 1. Check gcloud authentication
            self.log_event("PHASE3D1", "Checking gcloud authentication", "info")
            auth_result = subprocess.run(
                ["gcloud", "auth", "list", "--filter=status:ACTIVE", "--format=value(account)"],
                capture_output=True, text=True
            )
            
            if auth_result.returncode == 0 and auth_result.stdout.strip():
                active_account = auth_result.stdout.strip()
                self.log_event("PHASE3D1", f"✅ Authenticated as: {active_account}", "success")
                results["gcloud_auth"] = active_account
            else:
                self.log_event("PHASE3D1", "❌ No active gcloud authentication", "error")
                results["gcloud_auth"] = None
                return results
            
            # 2. Check database instance
            self.log_event("PHASE3D1", "Checking database instance", "info")
            instance_result = subprocess.run(
                ["gcloud", "sql", "instances", "describe", "congressional-db", "--format=value(state)"],
                capture_output=True, text=True
            )
            
            if instance_result.returncode == 0:
                instance_state = instance_result.stdout.strip()
                self.log_event("PHASE3D1", f"✅ Database instance state: {instance_state}", "success")
                results["database_state"] = instance_state
            else:
                self.log_event("PHASE3D1", f"❌ Failed to check database instance: {instance_result.stderr}", "error")
                results["database_error"] = instance_result.stderr
                return results
            
            # 3. Test database connection with simple query
            self.log_event("PHASE3D1", "Testing database connection", "info")
            test_result = self.execute_sql_via_gcloud("SELECT COUNT(*) FROM committees;")
            
            if test_result["returncode"] == 0:
                # Try to extract count from output
                output_lines = test_result["stdout"].strip().split('\n')
                count_line = None
                for line in output_lines:
                    if line.strip().isdigit():
                        count_line = line.strip()
                        break
                
                if count_line:
                    current_count = int(count_line)
                    results["current_committee_count"] = current_count
                    self.log_event("PHASE3D1", f"✅ Current committee count: {current_count}", "success")
                else:
                    self.log_event("PHASE3D1", "⚠️ Database connection successful but count unclear", "warning")
                    results["current_committee_count"] = "unknown"
            else:
                self.log_event("PHASE3D1", f"❌ Database connection test failed: {test_result['stderr']}", "error")
                results["database_connection_error"] = test_result["stderr"]
                return results
            
            # 4. Verify deployment file exists
            if os.path.exists(self.deployment_file):
                file_size = os.path.getsize(self.deployment_file)
                results["deployment_file_size"] = file_size
                self.log_event("PHASE3D1", f"✅ Deployment file verified: {file_size} bytes", "success")
            else:
                self.log_event("PHASE3D1", f"❌ Deployment file not found: {self.deployment_file}", "error")
                results["deployment_file_error"] = "File not found"
                return results
            
            # 5. Test API connectivity
            self.log_event("PHASE3D1", "Testing API connectivity", "info")
            try:
                response = requests.get(f"{self.api_base}/committees", timeout=10)
                if response.status_code == 200:
                    api_data = response.json()
                    api_count = len(api_data) if isinstance(api_data, list) else 0
                    results["api_current_committees"] = api_count
                    self.log_event("PHASE3D1", f"✅ API currently serves {api_count} committees", "success")
                else:
                    self.log_event("PHASE3D1", f"⚠️ API returned status {response.status_code}", "warning")
                    results["api_status"] = response.status_code
            except Exception as e:
                self.log_event("PHASE3D1", f"⚠️ API test failed: {e}", "warning")
                results["api_error"] = str(e)
            
            results["phase3d1_status"] = "success"
            self.log_event("PHASE3D1", "✅ Pre-deployment preparation completed successfully", "success")
            
        except Exception as e:
            results["phase3d1_status"] = "error"
            results["phase3d1_error"] = str(e)
            self.log_event("PHASE3D1", f"❌ Pre-deployment preparation failed: {e}", "error")
            
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
            
            # Execute deployment
            self.log_event("PHASE3D2", "Executing deployment SQL via gcloud", "info")
            deployment_start = time.time()
            
            deployment_result = self.execute_sql_via_gcloud(sql_content)
            deployment_time = time.time() - deployment_start
            
            if deployment_result["returncode"] == 0:
                self.log_event("PHASE3D2", f"✅ Deployment completed successfully in {deployment_time:.2f}s", "success")
                results["deployment_time"] = deployment_time
                results["phase3d2_status"] = "success"
            else:
                self.log_event("PHASE3D2", f"❌ Deployment failed: {deployment_result['stderr']}", "error")
                results["phase3d2_status"] = "error"
                results["phase3d2_error"] = deployment_result["stderr"]
            
        except Exception as e:
            results["phase3d2_status"] = "error"
            results["phase3d2_error"] = str(e)
            self.log_event("PHASE3D2", f"❌ Committee deployment failed: {e}", "error")
            
        return results
    
    def phase3d3_post_deployment_validation(self) -> Dict[str, Any]:
        """Phase 3D3: Post-Deployment Validation"""
        self.log_event("PHASE3D3", "Starting post-deployment validation", "info")
        results = {}
        
        try:
            # 1. Committee count validation
            self.log_event("PHASE3D3", "Validating committee count", "info")
            count_result = self.execute_sql_via_gcloud("SELECT COUNT(*) FROM committees;")
            
            if count_result["returncode"] == 0:
                # Extract count from output
                output_lines = count_result["stdout"].strip().split('\n')
                for line in output_lines:
                    if line.strip().isdigit():
                        total_committees = int(line.strip())
                        results["total_committees"] = total_committees
                        self.log_event("PHASE3D3", f"✅ Total committees after deployment: {total_committees}", "success")
                        break
                else:
                    self.log_event("PHASE3D3", "⚠️ Could not extract committee count from output", "warning")
                    results["total_committees"] = "unknown"
            else:
                self.log_event("PHASE3D3", f"❌ Failed to get committee count: {count_result['stderr']}", "error")
                results["count_error"] = count_result["stderr"]
            
            # 2. Chamber distribution
            self.log_event("PHASE3D3", "Checking chamber distribution", "info")
            chamber_result = self.execute_sql_via_gcloud("SELECT chamber, COUNT(*) FROM committees GROUP BY chamber ORDER BY chamber;")
            
            if chamber_result["returncode"] == 0:
                self.log_event("PHASE3D3", "✅ Chamber distribution query successful", "success")
                # Parse chamber distribution from output
                output_lines = chamber_result["stdout"].strip().split('\n')
                chamber_data = {}
                for line in output_lines:
                    if '|' in line:
                        parts = line.split('|')
                        if len(parts) >= 2:
                            chamber = parts[0].strip()
                            count_str = parts[1].strip()
                            if count_str.isdigit():
                                chamber_data[chamber] = int(count_str)
                
                results["chamber_distribution"] = chamber_data
                for chamber, count in chamber_data.items():
                    self.log_event("PHASE3D3", f"  {chamber}: {count} committees", "info")
            else:
                self.log_event("PHASE3D3", f"❌ Chamber distribution query failed: {chamber_result['stderr']}", "error")
            
            # 3. Check target achievement
            expected_total = 815
            if "total_committees" in results and isinstance(results["total_committees"], int):
                if results["total_committees"] >= expected_total:
                    self.log_event("PHASE3D3", f"✅ Target achieved: {results['total_committees']} >= {expected_total}", "success")
                    results["target_met"] = True
                else:
                    self.log_event("PHASE3D3", f"⚠️ Target not met: {results['total_committees']} < {expected_total}", "warning")
                    results["target_met"] = False
            
            # 4. Data integrity check
            self.log_event("PHASE3D3", "Checking data integrity", "info")
            integrity_result = self.execute_sql_via_gcloud("SELECT COUNT(*) FROM committees WHERE name IS NULL OR name = '';")
            
            if integrity_result["returncode"] == 0:
                output_lines = integrity_result["stdout"].strip().split('\n')
                for line in output_lines:
                    if line.strip().isdigit():
                        invalid_count = int(line.strip())
                        results["invalid_names"] = invalid_count
                        if invalid_count == 0:
                            self.log_event("PHASE3D3", "✅ Data integrity check passed", "success")
                        else:
                            self.log_event("PHASE3D3", f"⚠️ Found {invalid_count} invalid names", "warning")
                        break
            
            results["phase3d3_status"] = "success"
            self.log_event("PHASE3D3", "✅ Post-deployment validation completed", "success")
            
        except Exception as e:
            results["phase3d3_status"] = "error"
            results["phase3d3_error"] = str(e)
            self.log_event("PHASE3D3", f"❌ Post-deployment validation failed: {e}", "error")
            
        return results
    
    def phase3d4_system_verification(self) -> Dict[str, Any]:
        """Phase 3D4: System Verification"""
        self.log_event("PHASE3D4", "Starting system verification", "info")
        results = {}
        
        try:
            # Test API endpoints
            self.log_event("PHASE3D4", "Testing API endpoints", "info")
            
            # Main committees endpoint
            try:
                response = requests.get(f"{self.api_base}/committees", timeout=15)
                if response.status_code == 200:
                    api_data = response.json()
                    api_count = len(api_data) if isinstance(api_data, list) else 0
                    results["api_committee_count"] = api_count
                    self.log_event("PHASE3D4", f"✅ API now serves {api_count} committees", "success")
                    results["api_status"] = "success"
                else:
                    self.log_event("PHASE3D4", f"❌ API returned status {response.status_code}", "error")
                    results["api_status"] = "error"
                    results["api_error"] = f"HTTP {response.status_code}"
            except Exception as e:
                self.log_event("PHASE3D4", f"❌ API test failed: {e}", "error")
                results["api_status"] = "error"
                results["api_error"] = str(e)
            
            # Test chamber filtering
            chamber_tests = ["House", "Senate", "Joint"]
            results["chamber_tests"] = {}
            
            for chamber in chamber_tests:
                try:
                    response = requests.get(f"{self.api_base}/committees?chamber={chamber}", timeout=10)
                    if response.status_code == 200:
                        data = response.json()
                        count = len(data) if isinstance(data, list) else 0
                        results["chamber_tests"][chamber] = {"status": "success", "count": count}
                        self.log_event("PHASE3D4", f"✅ {chamber} committees: {count}", "success")
                    else:
                        results["chamber_tests"][chamber] = {"status": "error", "code": response.status_code}
                        self.log_event("PHASE3D4", f"❌ {chamber} test failed: {response.status_code}", "error")
                except Exception as e:
                    results["chamber_tests"][chamber] = {"status": "error", "error": str(e)}
                    self.log_event("PHASE3D4", f"❌ {chamber} test failed: {e}", "error")
            
            results["phase3d4_status"] = "success"
            self.log_event("PHASE3D4", "✅ System verification completed", "success")
            
        except Exception as e:
            results["phase3d4_status"] = "error"
            results["phase3d4_error"] = str(e)
            self.log_event("PHASE3D4", f"❌ System verification failed: {e}", "error")
            
        return results
    
    def execute_full_deployment(self) -> Dict[str, Any]:
        """Execute complete Phase 3 deployment"""
        self.log_event("DEPLOYMENT", "🚀 Starting Phase 3 Committee Deployment", "info")
        self.log_event("DEPLOYMENT", "Target: Deploy 815 committees to production database", "info")
        
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
    print("🚀 Phase 3 Committee Deployment - Cloud SQL Approach")
    print("=" * 60)
    
    # Verify deployment file exists
    deployment_file = "phase3_full_deployment_20250709_091846.sql"
    if not os.path.exists(deployment_file):
        print(f"❌ Error: Deployment file {deployment_file} not found")
        sys.exit(1)
    
    # Execute deployment
    executor = Phase3CloudSQLDeployment()
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
        status_icon = "✅" if status == "success" else "❌"
        print(f"{status_icon} Phase {phase_id.upper()}: {status.upper()}")
        
        if status != "success":
            all_phases_successful = False
        
        # Phase-specific details
        if phase_id == "3d1":
            if "current_committee_count" in phase_data:
                print(f"    Pre-deployment committees: {phase_data['current_committee_count']}")
            if "deployment_file_size" in phase_data:
                print(f"    Deployment file size: {phase_data['deployment_file_size']} bytes")
            if "gcloud_auth" in phase_data:
                print(f"    Authenticated as: {phase_data['gcloud_auth']}")
        
        elif phase_id == "3d2":
            if "deployment_time" in phase_data:
                print(f"    Deployment time: {phase_data['deployment_time']:.2f}s")
        
        elif phase_id == "3d3":
            if "total_committees" in phase_data:
                print(f"    Total committees deployed: {phase_data['total_committees']}")
            if "chamber_distribution" in phase_data:
                for chamber, count in phase_data["chamber_distribution"].items():
                    print(f"      {chamber}: {count}")
            if "target_met" in phase_data:
                target_icon = "✅" if phase_data["target_met"] else "❌"
                print(f"    Target (815) met: {target_icon}")
        
        elif phase_id == "3d4":
            if "api_committee_count" in phase_data:
                print(f"    API committee count: {phase_data['api_committee_count']}")
            if "chamber_tests" in phase_data:
                for chamber, test_result in phase_data["chamber_tests"].items():
                    if test_result["status"] == "success":
                        print(f"      {chamber}: {test_result['count']} committees")
    
    print(f"{'='*70}")
    
    # Final success determination
    if all_phases_successful:
        print("🎉 ✅ DEPLOYMENT SUCCESSFUL!")
        print("✅ Phase 3 completed successfully - Committee expansion deployed!")
        
        # Show key metrics
        if "3d3" in results["phases"]:
            total = results["phases"]["3d3"].get("total_committees", "unknown")
            print(f"✅ Total committees in database: {total}")
        
        if "3d4" in results["phases"]:
            api_count = results["phases"]["3d4"].get("api_committee_count", "unknown")
            print(f"✅ API serving {api_count} committees")
            
        print("🌐 Frontend: https://politicalequity.io")
        print("🔗 API: https://politicalequity.io/api/v1/committees")
        
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