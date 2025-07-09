#!/usr/bin/env python3
"""
Phase C: Deployment Executor for Full Committee Expansion
=========================================================

Execute SQL deployment using proven Cloud SQL Proxy methodology.
"""

import subprocess
import time
import os
import signal
import psycopg2
from datetime import datetime
import requests
import json
from typing import Dict

class FullExpansionDeploymentExecutor:
    """Execute full committee expansion deployment"""
    
    def __init__(self, sql_file: str):
        self.sql_file = sql_file
        self.proxy_process = None
        self.api_base = "https://politicalequity.io/api/v1"
        self.deployment_log = []
        
    def log_event(self, message: str, status: str = "info"):
        """Log deployment events"""
        timestamp = datetime.now().isoformat()
        symbol = {"info": "ℹ️", "success": "✅", "error": "❌", "warning": "⚠️"}.get(status, "ℹ️")
        log_entry = f"[{timestamp}] {symbol} {message}"
        print(log_entry)
        self.deployment_log.append({
            'timestamp': timestamp,
            'status': status,
            'message': message
        })
        
    def start_cloud_sql_proxy(self) -> bool:
        """Start Cloud SQL proxy using proven method"""
        try:
            self.log_event("Starting Cloud SQL proxy", "info")
            
            # Check if proxy is already running
            try:
                result = subprocess.run(["pgrep", "-f", "cloud-sql-proxy"], capture_output=True, text=True)
                if result.returncode == 0:
                    self.log_event("Proxy already running, killing existing process", "warning")
                    subprocess.run(["pkill", "-f", "cloud-sql-proxy"])
                    time.sleep(3)
            except:
                pass
            
            # Start the proxy using proven configuration
            cmd = [
                "./cloud-sql-proxy",
                "chefgavin:us-central1:congressional-db",
                "--port=5433"
            ]
            
            self.log_event(f"Starting proxy: {' '.join(cmd)}")
            
            self.proxy_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=os.getcwd()
            )
            
            # Wait for proxy to initialize
            self.log_event("Waiting for proxy initialization (12 seconds)")
            time.sleep(12)
            
            # Verify proxy is running
            if self.proxy_process.poll() is None:
                self.log_event("Cloud SQL proxy started successfully", "success")
                return True
            else:
                stdout, stderr = self.proxy_process.communicate()
                self.log_event(f"Proxy failed to start: {stderr.decode()}", "error")
                return False
                
        except Exception as e:
            self.log_event(f"Failed to start proxy: {e}", "error")
            return False
    
    def stop_cloud_sql_proxy(self):
        """Stop Cloud SQL proxy"""
        if self.proxy_process:
            try:
                self.log_event("Stopping Cloud SQL proxy")
                self.proxy_process.terminate()
                self.proxy_process.wait(timeout=5)
                self.log_event("Proxy stopped successfully", "success")
            except subprocess.TimeoutExpired:
                self.log_event("Force killing proxy")
                self.proxy_process.kill()
            except Exception as e:
                self.log_event(f"Error stopping proxy: {e}", "warning")
    
    def get_database_connection(self):
        """Get database connection via proxy using proven credentials"""
        try:
            conn = psycopg2.connect(
                host="localhost",
                port=5433,
                database="congress_data",
                user="postgres",
                password="mDf3S9ZnBpQqJvGsY1"  # Proven working password
            )
            return conn
        except Exception as e:
            self.log_event(f"Database connection failed: {e}", "error")
            return None
    
    def get_current_committee_count(self) -> int:
        """Get current committee count before deployment"""
        try:
            conn = self.get_database_connection()
            if not conn:
                return 0
            
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM committees;")
            count = cursor.fetchone()[0]
            
            cursor.close()
            conn.close()
            
            self.log_event(f"Current committee count: {count}", "success")
            return count
            
        except Exception as e:
            self.log_event(f"Failed to get current count: {e}", "error")
            return 0
    
    def execute_sql_deployment(self) -> bool:
        """Execute SQL deployment via proxy connection"""
        try:
            # Verify SQL file exists
            if not os.path.exists(self.sql_file):
                self.log_event(f"SQL file not found: {self.sql_file}", "error")
                return False
            
            # Read SQL content
            with open(self.sql_file, 'r') as f:
                sql_content = f.read()
            
            sql_size = len(sql_content)
            self.log_event(f"Loaded SQL deployment: {sql_size} characters")
            
            # Get database connection
            conn = self.get_database_connection()
            if not conn:
                return False
            
            # Execute deployment
            self.log_event("Executing SQL deployment via proxy connection")
            
            # Set autocommit for transaction handling
            conn.autocommit = True
            cursor = conn.cursor()
            
            # Execute the SQL
            start_time = time.time()
            cursor.execute(sql_content)
            execution_time = time.time() - start_time
            
            cursor.close()
            conn.close()
            
            self.log_event(f"SQL deployment completed in {execution_time:.2f}s", "success")
            return True
            
        except Exception as e:
            self.log_event(f"SQL deployment failed: {e}", "error")
            return False
    
    def validate_deployment_via_database(self) -> Dict:
        """Validate deployment by checking database directly"""
        try:
            self.log_event("Validating deployment via database")
            
            conn = self.get_database_connection()
            if not conn:
                return {}
            
            cursor = conn.cursor()
            
            # Get total count
            cursor.execute("SELECT COUNT(*) FROM committees;")
            total_count = cursor.fetchone()[0]
            
            # Get chamber breakdown
            cursor.execute("""
                SELECT chamber, COUNT(*) 
                FROM committees 
                GROUP BY chamber 
                ORDER BY chamber;
            """)
            chamber_breakdown = dict(cursor.fetchall())
            
            # Get type breakdown
            cursor.execute("""
                SELECT 
                    CASE 
                        WHEN committee_type IS NULL THEN 'NULL'
                        ELSE committee_type 
                    END as type,
                    COUNT(*) 
                FROM committees 
                GROUP BY committee_type 
                ORDER BY committee_type;
            """)
            type_breakdown = dict(cursor.fetchall())
            
            # Get missing congress_gov_id count
            cursor.execute("""
                SELECT COUNT(*) 
                FROM committees 
                WHERE congress_gov_id IS NULL OR congress_gov_id = '';
            """)
            missing_ids = cursor.fetchone()[0]
            
            cursor.close()
            conn.close()
            
            validation_results = {
                'total_committees': total_count,
                'chamber_breakdown': chamber_breakdown,
                'type_breakdown': type_breakdown,
                'missing_congress_gov_ids': missing_ids,
                'validation_timestamp': datetime.now().isoformat()
            }
            
            self.log_event(f"Database validation complete: {total_count} total committees", "success")
            return validation_results
            
        except Exception as e:
            self.log_event(f"Database validation failed: {e}", "error")
            return {}
    
    def validate_deployment_via_api(self) -> Dict:
        """Validate deployment by testing API endpoints"""
        try:
            self.log_event("Validating deployment via API")
            
            # Test main committees endpoint
            response = requests.get(f"{self.api_base}/committees?limit=200", timeout=30)
            if response.status_code != 200:
                self.log_event(f"API validation failed: {response.status_code}", "error")
                return {}
            
            page1_data = response.json()
            api_count = len(page1_data)
            
            # Try to get second page
            response2 = requests.get(f"{self.api_base}/committees?limit=200&page=2", timeout=30)
            if response2.status_code == 200:
                page2_data = response2.json()
                api_count += len(page2_data)
            
            # Try to get third page (if needed)
            response3 = requests.get(f"{self.api_base}/committees?limit=200&page=3", timeout=30)
            if response3.status_code == 200:
                page3_data = response3.json()
                api_count += len(page3_data)
            
            # Test chamber filtering
            house_response = requests.get(f"{self.api_base}/committees?chamber=House&limit=200", timeout=30)
            senate_response = requests.get(f"{self.api_base}/committees?chamber=Senate&limit=200", timeout=30)
            joint_response = requests.get(f"{self.api_base}/committees?chamber=Joint&limit=200", timeout=30)
            
            api_validation = {
                'api_total_committees': api_count,
                'api_response_success': response.status_code == 200,
                'chamber_filtering_works': {
                    'house': house_response.status_code == 200,
                    'senate': senate_response.status_code == 200,
                    'joint': joint_response.status_code == 200
                },
                'api_validation_timestamp': datetime.now().isoformat()
            }
            
            self.log_event(f"API validation complete: {api_count} committees accessible", "success")
            return api_validation
            
        except Exception as e:
            self.log_event(f"API validation failed: {e}", "error")
            return {}
    
    def run_full_deployment(self) -> Dict:
        """Run complete deployment process"""
        self.log_event("🚀 Starting full committee expansion deployment", "info")
        
        deployment_start = datetime.now()
        
        try:
            # Phase 1: Pre-deployment checks
            self.log_event("Phase 1: Pre-deployment checks")
            
            if not os.path.exists(self.sql_file):
                self.log_event(f"SQL file not found: {self.sql_file}", "error")
                return {}
            
            # Phase 2: Start proxy
            self.log_event("Phase 2: Starting Cloud SQL Proxy")
            if not self.start_cloud_sql_proxy():
                return {}
            
            # Phase 3: Get baseline counts
            self.log_event("Phase 3: Getting baseline committee count")
            baseline_count = self.get_current_committee_count()
            
            # Phase 4: Execute deployment
            self.log_event("Phase 4: Executing SQL deployment")
            if not self.execute_sql_deployment():
                return {}
            
            # Phase 5: Validation
            self.log_event("Phase 5: Validating deployment")
            
            # Brief pause for changes to propagate
            time.sleep(3)
            
            db_validation = self.validate_deployment_via_database()
            api_validation = self.validate_deployment_via_api()
            
            # Calculate results
            new_committees_added = db_validation.get('total_committees', 0) - baseline_count
            deployment_success = new_committees_added > 0
            
            deployment_end = datetime.now()
            deployment_duration = (deployment_end - deployment_start).total_seconds()
            
            # Compile final results
            results = {
                'deployment_successful': deployment_success,
                'deployment_start': deployment_start.isoformat(),
                'deployment_end': deployment_end.isoformat(),
                'deployment_duration_seconds': deployment_duration,
                'baseline_committee_count': baseline_count,
                'new_committees_added': new_committees_added,
                'final_committee_count': db_validation.get('total_committees', 0),
                'database_validation': db_validation,
                'api_validation': api_validation,
                'deployment_log': self.deployment_log
            }
            
            if deployment_success:
                self.log_event(f"✅ Deployment successful! Added {new_committees_added} committees", "success")
                self.log_event(f"   Final count: {results['final_committee_count']} committees")
                self.log_event(f"   Duration: {deployment_duration:.1f} seconds")
            else:
                self.log_event("❌ Deployment failed or had no effect", "error")
            
            return results
            
        except Exception as e:
            self.log_event(f"Deployment process failed: {e}", "error")
            return {}
            
        finally:
            # Always clean up proxy
            self.stop_cloud_sql_proxy()
    
    def save_deployment_results(self, results: Dict, filename: str = None):
        """Save deployment results to file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"full_expansion_deployment_results_{timestamp}.json"
        
        filepath = os.path.join(os.getcwd(), filename)
        
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        self.log_event(f"Deployment results saved to: {filepath}", "success")
        return filepath

def main():
    """Main execution function"""
    # Use the latest SQL deployment file
    sql_file = "full_committee_expansion_deployment_20250709_115958.sql"
    
    if not os.path.exists(sql_file):
        print(f"❌ SQL deployment file not found: {sql_file}")
        print("   Run phase_b_sql_deployment_generator.py first")
        return False
    
    # Execute deployment
    executor = FullExpansionDeploymentExecutor(sql_file)
    results = executor.run_full_deployment()
    
    if not results:
        print("\n❌ Deployment execution failed")
        return False
    
    # Save results
    results_file = executor.save_deployment_results(results)
    
    # Summary
    success = results.get('deployment_successful', False)
    baseline = results.get('baseline_committee_count', 0)
    added = results.get('new_committees_added', 0)
    final = results.get('final_committee_count', 0)
    duration = results.get('deployment_duration_seconds', 0)
    
    print(f"\n🎯 Full Expansion Deployment Summary:")
    print(f"   Status: {'✅ SUCCESS' if success else '❌ FAILED'}")
    print(f"   Baseline Count: {baseline}")
    print(f"   Added: {added}")
    print(f"   Final Count: {final}")
    print(f"   Duration: {duration:.1f}s")
    print(f"   Results File: {results_file}")
    
    if success:
        db_validation = results.get('database_validation', {})
        chamber_breakdown = db_validation.get('chamber_breakdown', {})
        
        print(f"\n📊 Chamber Distribution:")
        for chamber, count in chamber_breakdown.items():
            print(f"   {chamber}: {count}")
        
        print(f"\n✅ Phase C complete - Full expansion deployed successfully!")
        print(f"   Ready for system verification and production use")
        return True
    else:
        print(f"\n❌ Phase C failed - Review deployment logs")
        return False

if __name__ == "__main__":
    main()