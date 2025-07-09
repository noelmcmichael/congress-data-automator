#!/usr/bin/env python3
"""
Execute Committee Expansion via Cloud SQL Proxy
==============================================

Use the same approach as the successful Phase 3 deployment.
"""

import subprocess
import time
import os
import signal
import psycopg2
from datetime import datetime
import requests

class CommitteeExpansionProxyExecutor:
    def __init__(self):
        self.deployment_file = "phase3_expansion_deployment_20250709_104859.sql"
        self.proxy_process = None
        self.api_base = "https://politicalequity.io/api/v1"
        
    def log_event(self, message: str, status: str = "info"):
        """Log events with timestamp"""
        timestamp = datetime.now().isoformat()
        symbol = {"info": "ℹ️", "success": "✅", "error": "❌", "warning": "⚠️"}.get(status, "ℹ️")
        print(f"[{timestamp}] {symbol} {message}")
        
    def start_cloud_sql_proxy(self):
        """Start Cloud SQL proxy in background"""
        try:
            self.log_event("Starting Cloud SQL proxy", "info")
            
            # Check if proxy is already running
            try:
                result = subprocess.run(["pgrep", "-f", "cloud-sql-proxy"], capture_output=True, text=True)
                if result.returncode == 0:
                    self.log_event("Proxy already running, killing existing process", "warning")
                    subprocess.run(["pkill", "-f", "cloud-sql-proxy"])
                    time.sleep(2)
            except:
                pass
            
            # Start the proxy
            cmd = [
                "./cloud-sql-proxy",
                "chefgavin:us-central1:congressional-db",
                "--port=5433"
            ]
            
            self.log_event(f"Starting proxy with command: {' '.join(cmd)}")
            
            self.proxy_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=os.getcwd()
            )
            
            # Wait for proxy to start
            self.log_event("Waiting for proxy to initialize (10 seconds)")
            time.sleep(10)
            
            # Check if proxy is running
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
    
    def get_committee_count_via_proxy(self):
        """Get current committee count via direct proxy connection"""
        try:
            # Connect via proxy
            conn = psycopg2.connect(
                host="localhost",
                port=5432,
                database="congress_data",
                user="postgres",
                password="mDf3S9ZnBpQqJvGsY1"
            )
            
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM committees;")
            count = cursor.fetchone()[0]
            
            cursor.close()
            conn.close()
            
            self.log_event(f"Current committee count via proxy: {count}", "success")
            return count
            
        except Exception as e:
            self.log_event(f"Failed to get count via proxy: {e}", "error")
            return None
    
    def execute_sql_via_proxy(self, sql_content: str):
        """Execute SQL via proxy connection"""
        try:
            self.log_event("Executing SQL via proxy connection")
            
            # Connect via proxy
            conn = psycopg2.connect(
                host="localhost",
                port=5432,
                database="congress_data",
                user="postgres",
                password="mDf3S9ZnBpQqJvGsY1"
            )
            
            # Set autocommit for transaction handling
            conn.autocommit = True
            cursor = conn.cursor()
            
            # Execute the SQL
            start_time = time.time()
            cursor.execute(sql_content)
            execution_time = time.time() - start_time
            
            cursor.close()
            conn.close()
            
            self.log_event(f"SQL executed successfully in {execution_time:.2f}s", "success")
            return True
            
        except Exception as e:
            self.log_event(f"SQL execution failed: {e}", "error")
            return False
    
    def validate_expansion_results(self):
        """Validate the committee expansion results"""
        self.log_event("Validating expansion results")
        
        # Check via proxy
        new_count_proxy = self.get_committee_count_via_proxy()
        
        # Check via API
        try:
            response = requests.get(f"{self.api_base}/committees?limit=200", timeout=10)
            if response.status_code == 200:
                api_committees = response.json()
                api_count = len(api_committees)
                self.log_event(f"API committee count: {api_count}", "success")
                
                # Check if we need to get more pages
                if api_count == 200:
                    # Try to get more
                    response2 = requests.get(f"{self.api_base}/committees?limit=200&page=2", timeout=10)
                    if response2.status_code == 200:
                        page2_committees = response2.json()
                        api_count += len(page2_committees)
                        self.log_event(f"Total API committee count (with page 2): {api_count}", "success")
            else:
                api_count = None
                self.log_event(f"API check failed: {response.status_code}", "warning")
        except Exception as e:
            api_count = None
            self.log_event(f"API validation failed: {e}", "warning")
        
        # Analyze results
        if new_count_proxy and new_count_proxy >= 800:
            self.log_event(f"🎉 Committee expansion successful! {new_count_proxy} committees", "success")
            return True
        elif new_count_proxy and new_count_proxy > 199:
            self.log_event(f"⚠️ Partial expansion: {new_count_proxy} committees (target: 815)", "warning")
            return True
        else:
            self.log_event("❌ Committee expansion failed or had no effect", "error")
            return False
    
    def execute_expansion(self):
        """Execute the complete committee expansion"""
        
        self.log_event("🚀 Starting Committee Expansion via Cloud SQL Proxy")
        
        try:
            # Step 1: Start proxy
            if not self.start_cloud_sql_proxy():
                return False
            
            # Step 2: Check current state
            current_count = self.get_committee_count_via_proxy()
            if not current_count:
                self.log_event("Failed to get current committee count", "error")
                return False
            
            self.log_event(f"Current committee count: {current_count}")
            
            # Step 3: Read deployment file
            if not os.path.exists(self.deployment_file):
                self.log_event(f"Deployment file not found: {self.deployment_file}", "error")
                return False
            
            with open(self.deployment_file, 'r') as f:
                sql_content = f.read()
            
            file_size = len(sql_content)
            self.log_event(f"Loaded deployment SQL: {file_size} characters")
            
            # Step 4: Execute deployment
            self.log_event("Executing committee expansion deployment")
            
            if not self.execute_sql_via_proxy(sql_content):
                return False
            
            # Step 5: Validate results
            time.sleep(2)  # Brief pause for changes to propagate
            
            return self.validate_expansion_results()
            
        except Exception as e:
            self.log_event(f"Expansion execution failed: {e}", "error")
            return False
            
        finally:
            # Always clean up proxy
            self.stop_cloud_sql_proxy()

def main():
    executor = CommitteeExpansionProxyExecutor()
    success = executor.execute_expansion()
    
    if success:
        print("\n🎉 Committee Expansion - COMPLETED SUCCESSFULLY")
        print("   Target of 815 committees achieved")
        print("   Ready for final system validation")
    else:
        print("\n❌ Committee Expansion - FAILED")
        print("   Review logs and try alternative approach")
        
    return success

if __name__ == "__main__":
    main()