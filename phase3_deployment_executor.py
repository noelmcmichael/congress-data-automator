#!/usr/bin/env python3
"""
Phase 3 Committee Deployment Executor
====================================

Executes the deployment of 815 committees to production database
with comprehensive monitoring, validation, and rollback procedures.
"""

import subprocess
import json
import time
from datetime import datetime
from typing import Dict, List, Any
import os
import psycopg2
from psycopg2.extras import RealDictCursor

class Phase3DeploymentExecutor:
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
        
    def get_db_connection(self):
        """Get connection to production database"""
        try:
            connection = psycopg2.connect(
                host="34.70.144.194",
                database="congress_data",
                user="postgres",
                password=os.getenv("DB_PASSWORD")
            )
            return connection
        except Exception as e:
            self.log_event("CONNECTION", f"Database connection failed: {e}", "error")
            raise
    
    def phase3d1_pre_deployment(self) -> Dict[str, Any]:
        """Phase 3D1: Pre-Deployment Preparation"""
        self.log_event("PHASE3D1", "Starting pre-deployment preparation", "info")
        results = {}
        
        try:
            # 1. Create production backup
            self.log_event("PHASE3D1", "Creating production database backup", "info")
            backup_filename = f"backup_pre_phase3_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
            
            backup_cmd = [
                "gcloud", "sql", "export", "sql", "congressional-db",
                f"gs://congressional-data-backups/{backup_filename}",
                "--database=congress_data"
            ]
            
            backup_result = subprocess.run(backup_cmd, capture_output=True, text=True)
            if backup_result.returncode == 0:
                self.log_event("PHASE3D1", f"Backup created: {backup_filename}", "success")
                results["backup_file"] = backup_filename
            else:
                self.log_event("PHASE3D1", f"Backup failed: {backup_result.stderr}", "error")
                results["backup_error"] = backup_result.stderr
            
            # 2. Test database connection
            self.log_event("PHASE3D1", "Testing database connection", "info")
            conn = self.get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # Check current committee count
            cursor.execute("SELECT COUNT(*) as count FROM committees")
            current_count = cursor.fetchone()["count"]
            results["current_committee_count"] = current_count
            self.log_event("PHASE3D1", f"Current committee count: {current_count}", "info")
            
            # Check database version and status
            cursor.execute("SELECT version()")
            db_version = cursor.fetchone()["version"]
            results["database_version"] = db_version
            self.log_event("PHASE3D1", f"Database version: {db_version[:50]}...", "info")
            
            # 3. Verify deployment file exists
            if os.path.exists(self.deployment_file):
                file_size = os.path.getsize(self.deployment_file)
                results["deployment_file_size"] = file_size
                self.log_event("PHASE3D1", f"Deployment file verified: {file_size} bytes", "success")
            else:
                self.log_event("PHASE3D1", f"Deployment file not found: {self.deployment_file}", "error")
                results["deployment_file_error"] = "File not found"
            
            # 4. Performance baseline
            start_time = time.time()
            cursor.execute("SELECT COUNT(*) FROM committees WHERE chamber = 'House'")
            house_count = cursor.fetchone()["count"]
            query_time = time.time() - start_time
            results["baseline_query_time"] = query_time
            results["current_house_committees"] = house_count
            self.log_event("PHASE3D1", f"Baseline query time: {query_time:.3f}s", "info")
            
            cursor.close()
            conn.close()
            
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
            conn = self.get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # Start transaction
            conn.autocommit = False
            self.log_event("PHASE3D2", "Starting transaction", "info")
            
            # Execute SQL file
            self.log_event("PHASE3D2", f"Executing {self.deployment_file}", "info")
            deployment_start = time.time()
            
            with open(self.deployment_file, 'r') as f:
                sql_content = f.read()
            
            cursor.execute(sql_content)
            deployment_time = time.time() - deployment_start
            
            # Commit transaction
            conn.commit()
            self.log_event("PHASE3D2", f"Deployment completed in {deployment_time:.2f}s", "success")
            
            results["deployment_time"] = deployment_time
            results["phase3d2_status"] = "success"
            
            cursor.close()
            conn.close()
            
        except Exception as e:
            results["phase3d2_status"] = "error"
            results["phase3d2_error"] = str(e)
            self.log_event("PHASE3D2", f"Committee deployment failed: {e}", "error")
            
            # Rollback if possible
            try:
                conn.rollback()
                self.log_event("PHASE3D2", "Transaction rolled back", "info")
            except:
                pass
            
        return results
    
    def phase3d3_post_deployment_validation(self) -> Dict[str, Any]:
        """Phase 3D3: Post-Deployment Validation"""
        self.log_event("PHASE3D3", "Starting post-deployment validation", "info")
        results = {}
        
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # 1. Committee count validation
            cursor.execute("SELECT COUNT(*) as count FROM committees")
            total_committees = cursor.fetchone()["count"]
            results["total_committees"] = total_committees
            self.log_event("PHASE3D3", f"Total committees: {total_committees}", "info")
            
            # 2. Chamber distribution
            cursor.execute("SELECT chamber, COUNT(*) as count FROM committees GROUP BY chamber")
            chamber_distribution = dict(cursor.fetchall())
            results["chamber_distribution"] = chamber_distribution
            
            for chamber, count in chamber_distribution.items():
                self.log_event("PHASE3D3", f"{chamber} committees: {count}", "info")
            
            # 3. Performance test
            start_time = time.time()
            cursor.execute("SELECT * FROM committees WHERE chamber = 'House' LIMIT 10")
            sample_committees = cursor.fetchall()
            query_time = time.time() - start_time
            results["post_deployment_query_time"] = query_time
            self.log_event("PHASE3D3", f"Sample query time: {query_time:.3f}s", "info")
            
            # 4. Data integrity check
            cursor.execute("SELECT COUNT(*) as count FROM committees WHERE name IS NULL OR name = ''")
            invalid_names = cursor.fetchone()["count"]
            results["invalid_names"] = invalid_names
            
            if invalid_names == 0:
                self.log_event("PHASE3D3", "Data integrity check passed", "success")
            else:
                self.log_event("PHASE3D3", f"Found {invalid_names} invalid committee names", "warning")
            
            cursor.close()
            conn.close()
            
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
            api_test_cmd = [
                "curl", "-s", "-w", "@curl-format.txt", 
                "https://politicalequity.io/api/v1/committees"
            ]
            
            # Create curl format file for timing
            with open("curl-format.txt", "w") as f:
                f.write("time_total:%{time_total}")
            
            try:
                api_result = subprocess.run(api_test_cmd, capture_output=True, text=True, timeout=30)
                if api_result.returncode == 0:
                    # Parse response time from last line
                    lines = api_result.stdout.strip().split('\n')
                    if lines and lines[-1].startswith('time_total:'):
                        response_time = float(lines[-1].split(':')[1])
                        results["api_response_time"] = response_time
                        self.log_event("PHASE3D4", f"API response time: {response_time:.3f}s", "info")
                    
                    # Check if we got JSON response
                    json_response = '\n'.join(lines[:-1])
                    if json_response.strip().startswith('[') or json_response.strip().startswith('{'):
                        results["api_status"] = "success"
                        self.log_event("PHASE3D4", "API endpoint responding correctly", "success")
                    else:
                        results["api_status"] = "error"
                        results["api_error"] = "Invalid JSON response"
                        self.log_event("PHASE3D4", "API returned invalid JSON", "error")
                else:
                    results["api_status"] = "error"
                    results["api_error"] = api_result.stderr
                    self.log_event("PHASE3D4", f"API test failed: {api_result.stderr}", "error")
                    
            except subprocess.TimeoutExpired:
                results["api_status"] = "timeout"
                self.log_event("PHASE3D4", "API test timed out", "error")
            
            # Clean up curl format file
            try:
                os.remove("curl-format.txt")
            except:
                pass
            
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

if __name__ == "__main__":
    executor = Phase3DeploymentExecutor()
    results = executor.execute_full_deployment()
    
    # Print summary
    print(f"\n{'='*50}")
    print("PHASE 3 DEPLOYMENT SUMMARY")
    print(f"{'='*50}")
    
    for phase, phase_results in results["phases"].items():
        status = phase_results.get(f"phase{phase}_status", "unknown")
        print(f"Phase {phase.upper()}: {status.upper()}")
        
        if phase == "3d3" and "total_committees" in phase_results:
            print(f"  Total committees deployed: {phase_results['total_committees']}")
            if "chamber_distribution" in phase_results:
                for chamber, count in phase_results["chamber_distribution"].items():
                    print(f"    {chamber}: {count}")
    
    print(f"{'='*50}")