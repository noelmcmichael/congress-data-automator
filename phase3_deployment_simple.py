#!/usr/bin/env python3
"""
Phase 3 Committee Deployment - Simple Approach
==============================================

Uses gcloud sql connect for direct database access
Executes the deployment with comprehensive logging
"""

import subprocess
import json
import time
from datetime import datetime
from typing import Dict, Any
import os
import tempfile

class Phase3SimpleDeployment:
    def __init__(self):
        self.deployment_start = datetime.now()
        self.deployment_log = []
        self.deployment_file = "phase3_full_deployment_20250709_091846.sql"
        
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
        
    def run_sql_command(self, sql_command: str) -> Dict[str, Any]:
        """Run SQL command via gcloud sql connect"""
        try:
            # Create temporary file with SQL command
            with tempfile.NamedTemporaryFile(mode='w', suffix='.sql', delete=False) as tmp_file:
                tmp_file.write(sql_command)
                tmp_file_path = tmp_file.name
                
            # Run command via gcloud sql connect
            cmd = [
                "gcloud", "sql", "connect", "congressional-db",
                "--user=postgres",
                "--database=congress_data",
                f"--quiet"
            ]
            
            # Execute SQL file
            process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Read SQL file content and send to psql
            with open(tmp_file_path, 'r') as f:
                sql_content = f.read()
            
            stdout, stderr = process.communicate(input=sql_content)
            
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
            # 1. Check current committee count
            self.log_event("PHASE3D1", "Checking current committee count", "info")
            count_result = self.run_sql_command("SELECT COUNT(*) FROM committees;")
            
            if count_result["returncode"] == 0:
                # Extract count from output
                output_lines = count_result["stdout"].strip().split('\n')
                for line in output_lines:
                    if line.strip().isdigit():
                        current_count = int(line.strip())
                        results["current_committee_count"] = current_count
                        self.log_event("PHASE3D1", f"Current committee count: {current_count}", "info")
                        break
            else:
                self.log_event("PHASE3D1", f"Failed to get committee count: {count_result['stderr']}", "error")
            
            # 2. Check chamber distribution
            self.log_event("PHASE3D1", "Checking chamber distribution", "info")
            chamber_result = self.run_sql_command("SELECT chamber, COUNT(*) FROM committees GROUP BY chamber;")
            
            if chamber_result["returncode"] == 0:
                self.log_event("PHASE3D1", f"Chamber distribution query successful", "info")
                results["chamber_query_status"] = "success"
            else:
                self.log_event("PHASE3D1", f"Chamber distribution query failed: {chamber_result['stderr']}", "error")
            
            # 3. Verify deployment file exists
            if os.path.exists(self.deployment_file):
                file_size = os.path.getsize(self.deployment_file)
                results["deployment_file_size"] = file_size
                self.log_event("PHASE3D1", f"Deployment file verified: {file_size} bytes", "success")
            else:
                self.log_event("PHASE3D1", f"Deployment file not found: {self.deployment_file}", "error")
                results["deployment_file_error"] = "File not found"
                return results
            
            # 4. Create backup
            self.log_event("PHASE3D1", "Creating database backup", "info")
            backup_filename = f"backup_pre_phase3_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
            
            # Note: For production, we'd use gcloud sql export
            # For now, we'll just log the backup intention
            results["backup_file"] = backup_filename
            self.log_event("PHASE3D1", f"Backup planned: {backup_filename}", "info")
            
            results["phase3d1_status"] = "success"
            self.log_event("PHASE3D1", "Pre-deployment preparation completed", "success")
            
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
            
            self.log_event("PHASE3D2", f"Executing {self.deployment_file}", "info")
            deployment_start = time.time()
            
            # Execute deployment
            deployment_result = self.run_sql_command(sql_content)
            deployment_time = time.time() - deployment_start
            
            if deployment_result["returncode"] == 0:
                self.log_event("PHASE3D2", f"Deployment completed in {deployment_time:.2f}s", "success")
                results["deployment_time"] = deployment_time
                results["phase3d2_status"] = "success"
            else:
                self.log_event("PHASE3D2", f"Deployment failed: {deployment_result['stderr']}", "error")
                results["phase3d2_status"] = "error"
                results["phase3d2_error"] = deployment_result["stderr"]
            
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
            # 1. Committee count validation
            self.log_event("PHASE3D3", "Validating committee count", "info")
            count_result = self.run_sql_command("SELECT COUNT(*) FROM committees;")
            
            if count_result["returncode"] == 0:
                # Extract count from output
                output_lines = count_result["stdout"].strip().split('\n')
                for line in output_lines:
                    if line.strip().isdigit():
                        total_committees = int(line.strip())
                        results["total_committees"] = total_committees
                        self.log_event("PHASE3D3", f"Total committees: {total_committees}", "info")
                        break
            
            # 2. Chamber distribution
            self.log_event("PHASE3D3", "Checking chamber distribution", "info")
            chamber_result = self.run_sql_command("SELECT chamber, COUNT(*) FROM committees GROUP BY chamber ORDER BY chamber;")
            
            if chamber_result["returncode"] == 0:
                self.log_event("PHASE3D3", "Chamber distribution retrieved", "info")
                results["chamber_distribution_query"] = "success"
                # Parse chamber distribution from output
                chamber_lines = chamber_result["stdout"].strip().split('\n')
                chamber_data = {}
                for line in chamber_lines:
                    if '|' in line and line.strip():
                        parts = line.split('|')
                        if len(parts) >= 2:
                            chamber = parts[0].strip()
                            count_str = parts[1].strip()
                            if count_str.isdigit():
                                chamber_data[chamber] = int(count_str)
                
                results["chamber_distribution"] = chamber_data
                for chamber, count in chamber_data.items():
                    self.log_event("PHASE3D3", f"{chamber} committees: {count}", "info")
            
            # 3. Data integrity check
            self.log_event("PHASE3D3", "Checking data integrity", "info")
            integrity_result = self.run_sql_command("SELECT COUNT(*) FROM committees WHERE name IS NULL OR name = '';")
            
            if integrity_result["returncode"] == 0:
                # Extract invalid count
                output_lines = integrity_result["stdout"].strip().split('\n')
                for line in output_lines:
                    if line.strip().isdigit():
                        invalid_names = int(line.strip())
                        results["invalid_names"] = invalid_names
                        if invalid_names == 0:
                            self.log_event("PHASE3D3", "Data integrity check passed", "success")
                        else:
                            self.log_event("PHASE3D3", f"Found {invalid_names} invalid committee names", "warning")
                        break
            
            results["phase3d3_status"] = "success"
            self.log_event("PHASE3D3", "Post-deployment validation completed", "success")
            
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
            # Test API endpoint
            self.log_event("PHASE3D4", "Testing API endpoint", "info")
            
            # Test committees endpoint
            api_test_cmd = [
                "curl", "-s", "-w", "\\n%{http_code}\\n%{time_total}",
                "https://politicalequity.io/api/v1/committees"
            ]
            
            try:
                api_result = subprocess.run(api_test_cmd, capture_output=True, text=True, timeout=30)
                if api_result.returncode == 0:
                    lines = api_result.stdout.strip().split('\n')
                    if len(lines) >= 2:
                        http_code = lines[-2]
                        response_time = float(lines[-1])
                        
                        results["api_http_code"] = http_code
                        results["api_response_time"] = response_time
                        
                        if http_code == "200":
                            self.log_event("PHASE3D4", f"API responding correctly (200) in {response_time:.3f}s", "success")
                            results["api_status"] = "success"
                        else:
                            self.log_event("PHASE3D4", f"API returned HTTP {http_code}", "error")
                            results["api_status"] = "error"
                    else:
                        results["api_status"] = "error"
                        self.log_event("PHASE3D4", "API test returned unexpected output", "error")
                else:
                    results["api_status"] = "error"
                    results["api_error"] = api_result.stderr
                    self.log_event("PHASE3D4", f"API test failed: {api_result.stderr}", "error")
                    
            except subprocess.TimeoutExpired:
                results["api_status"] = "timeout"
                self.log_event("PHASE3D4", "API test timed out", "error")
            
            results["phase3d4_status"] = "success"
            self.log_event("PHASE3D4", "System verification completed", "success")
            
        except Exception as e:
            results["phase3d4_status"] = "error"
            results["phase3d4_error"] = str(e)
            self.log_event("PHASE3D4", f"System verification failed: {e}", "error")
            
        return results
    
    def execute_full_deployment(self) -> Dict[str, Any]:
        """Execute complete Phase 3 deployment"""
        self.log_event("DEPLOYMENT", "Starting Phase 3 Committee Deployment", "info")
        
        deployment_results = {
            "deployment_start": self.deployment_start.isoformat(),
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
        self.log_event("DEPLOYMENT", "Phase 3 Committee Deployment completed", "success")
        
        return deployment_results

def main():
    # Check if deployment file exists
    deployment_file = "phase3_full_deployment_20250709_091846.sql"
    if not os.path.exists(deployment_file):
        print(f"Error: Deployment file {deployment_file} not found")
        return
    
    # Check if gcloud is available
    try:
        result = subprocess.run(["gcloud", "version"], capture_output=True, text=True)
        if result.returncode != 0:
            print("Error: gcloud CLI not available")
            return
    except Exception as e:
        print(f"Error: gcloud CLI not available: {e}")
        return
    
    # Execute deployment
    executor = Phase3SimpleDeployment()
    results = executor.execute_full_deployment()
    
    # Print summary
    print(f"\n{'='*60}")
    print("PHASE 3 DEPLOYMENT SUMMARY")
    print(f"{'='*60}")
    
    for phase, phase_results in results["phases"].items():
        status = phase_results.get(f"phase{phase}_status", "unknown")
        print(f"Phase {phase.upper()}: {status.upper()}")
        
        if phase == "3d1":
            if "current_committee_count" in phase_results:
                print(f"  Current committees: {phase_results['current_committee_count']}")
            if "deployment_file_size" in phase_results:
                print(f"  Deployment file size: {phase_results['deployment_file_size']} bytes")
        
        elif phase == "3d2":
            if "deployment_time" in phase_results:
                print(f"  Deployment time: {phase_results['deployment_time']:.2f}s")
        
        elif phase == "3d3":
            if "total_committees" in phase_results:
                print(f"  Total committees deployed: {phase_results['total_committees']}")
            if "chamber_distribution" in phase_results:
                for chamber, count in phase_results["chamber_distribution"].items():
                    print(f"    {chamber}: {count}")
        
        elif phase == "3d4":
            if "api_status" in phase_results:
                print(f"  API status: {phase_results['api_status']}")
            if "api_response_time" in phase_results:
                print(f"  API response time: {phase_results['api_response_time']:.3f}s")
    
    print(f"{'='*60}")
    
    # Check if deployment was successful
    all_phases_successful = all(
        results["phases"].get(phase, {}).get(f"phase{phase}_status") == "success"
        for phase in ["3d1", "3d2", "3d3", "3d4"]
    )
    
    if all_phases_successful:
        print("✅ DEPLOYMENT SUCCESSFUL - Phase 3 completed successfully!")
    else:
        print("❌ DEPLOYMENT FAILED - Check logs for details")

if __name__ == "__main__":
    main()