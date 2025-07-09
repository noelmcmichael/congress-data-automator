#!/usr/bin/env python3
"""
Execute Committee Expansion Deployment
=====================================

Deploy the modified SQL to add new committees to the database.
"""

import subprocess
import time
import os
from datetime import datetime

class CommitteeExpansionExecutor:
    def __init__(self):
        self.deployment_file = "phase3_expansion_deployment_20250709_104859.sql"
        self.start_time = datetime.now()
        
    def log_event(self, message: str, status: str = "info"):
        """Log events with timestamp"""
        timestamp = datetime.now().isoformat()
        print(f"[{timestamp}] {message}")
        
    def execute_sql_via_gcloud(self, sql_file: str):
        """Execute SQL file via gcloud"""
        try:
            self.log_event(f"Executing SQL file: {sql_file}")
            
            # Set password in environment
            env = os.environ.copy()
            env["PGPASSWORD"] = "mDf3S9ZnBpQqJvGsY1"
            
            # Execute with input from file
            with open(sql_file, 'r') as f:
                sql_content = f.read()
            
            result = subprocess.run([
                "/opt/homebrew/bin/gcloud", "sql", "connect", "congressional-db", 
                "--user=postgres", "--quiet"
            ], 
            input=sql_content, 
            text=True, 
            capture_output=True,
            env=env
            )
            
            return {
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
            
        except Exception as e:
            return {
                "returncode": -1,
                "stdout": "",
                "stderr": str(e)
            }
    
    def check_committee_count(self):
        """Check current committee count"""
        try:
            env = os.environ.copy()
            env["PGPASSWORD"] = "mDf3S9ZnBpQqJvGsY1"
            
            result = subprocess.run([
                "/opt/homebrew/bin/gcloud", "sql", "connect", "congressional-db", 
                "--user=postgres", "--quiet"
            ], 
            input="SELECT COUNT(*) FROM committees;\n\\q", 
            text=True, 
            capture_output=True,
            env=env
            )
            
            if result.returncode == 0:
                # Extract count from output
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if line.strip().isdigit():
                        return int(line.strip())
            return None
        except Exception as e:
            self.log_event(f"Error checking committee count: {e}", "error")
            return None
    
    def check_chamber_distribution(self):
        """Check committee distribution by chamber"""
        try:
            env = os.environ.copy()
            env["PGPASSWORD"] = "mDf3S9ZnBpQqJvGsY1"
            
            result = subprocess.run([
                "/opt/homebrew/bin/gcloud", "sql", "connect", "congressional-db", 
                "--user=postgres", "--quiet"
            ], 
            input="SELECT chamber, COUNT(*) FROM committees GROUP BY chamber ORDER BY chamber;\n\\q", 
            text=True, 
            capture_output=True,
            env=env
            )
            
            if result.returncode == 0:
                distribution = {}
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if '|' in line and not line.startswith('-'):
                        parts = [p.strip() for p in line.split('|')]
                        if len(parts) >= 2 and parts[0] not in ['chamber', '']:
                            distribution[parts[0]] = int(parts[1])
                return distribution
            return None
        except Exception as e:
            self.log_event(f"Error checking chamber distribution: {e}", "error")
            return None
    
    def execute_expansion(self):
        """Execute the complete committee expansion"""
        
        self.log_event("🚀 Starting Committee Expansion Deployment", "info")
        
        # Phase E3.1: Pre-deployment validation
        self.log_event("Phase E3.1: Pre-deployment validation", "info")
        
        if not os.path.exists(self.deployment_file):
            self.log_event(f"❌ Deployment file not found: {self.deployment_file}", "error")
            return False
        
        file_size = os.path.getsize(self.deployment_file)
        self.log_event(f"✅ Deployment file verified: {file_size} bytes", "success")
        
        # Check current committee count
        current_count = self.check_committee_count()
        if current_count is not None:
            self.log_event(f"✅ Current committee count: {current_count}", "success")
        else:
            self.log_event("❌ Failed to check current committee count", "error")
            return False
        
        # Phase E3.2: Execute deployment
        self.log_event("Phase E3.2: Executing committee expansion deployment", "info")
        
        start_time = time.time()
        result = self.execute_sql_via_gcloud(self.deployment_file)
        execution_time = time.time() - start_time
        
        if result["returncode"] == 0:
            self.log_event(f"✅ Deployment executed successfully ({execution_time:.1f}s)", "success")
        else:
            self.log_event(f"❌ Deployment failed: {result['stderr']}", "error")
            return False
        
        # Phase E3.3: Post-deployment validation
        self.log_event("Phase E3.3: Post-deployment validation", "info")
        
        # Check new committee count
        new_count = self.check_committee_count()
        if new_count is not None:
            added_committees = new_count - current_count
            self.log_event(f"✅ New committee count: {new_count} (+{added_committees} added)", "success")
            
            if new_count >= 800:  # Should be close to 815
                self.log_event("✅ Committee expansion successful", "success")
            else:
                self.log_event(f"⚠️ Committee count lower than expected (target: 815)", "warning")
        else:
            self.log_event("❌ Failed to verify new committee count", "error")
            return False
        
        # Check chamber distribution
        distribution = self.check_chamber_distribution()
        if distribution:
            self.log_event("✅ Chamber distribution:", "success")
            for chamber, count in distribution.items():
                self.log_event(f"   {chamber}: {count} committees", "info")
        else:
            self.log_event("⚠️ Failed to check chamber distribution", "warning")
        
        # Phase E3.4: API validation
        self.log_event("Phase E3.4: Testing API with expanded dataset", "info")
        
        try:
            import requests
            
            # Test API with high limit
            response = requests.get("https://politicalequity.io/api/v1/committees?limit=1000", timeout=15)
            if response.status_code == 200:
                api_data = response.json()
                api_count = len(api_data) if isinstance(api_data, list) else 0
                self.log_event(f"✅ API returns {api_count} committees", "success")
                
                if api_count >= new_count - 10:  # Allow small discrepancy
                    self.log_event("✅ API data consistent with database", "success")
                else:
                    self.log_event(f"⚠️ API count ({api_count}) differs from database ({new_count})", "warning")
            else:
                self.log_event(f"❌ API test failed: {response.status_code}", "error")
        except Exception as e:
            self.log_event(f"⚠️ API test failed: {e}", "warning")
        
        total_time = time.time() - time.mktime(self.start_time.timetuple())
        self.log_event(f"🎯 Committee expansion completed in {total_time:.1f}s", "success")
        
        return True

def main():
    executor = CommitteeExpansionExecutor()
    success = executor.execute_expansion()
    
    if success:
        print("\n🎉 Priority 2: Committee Expansion - COMPLETED SUCCESSFULLY")
        print("   Ready to proceed to Priority 3: System Verification")
    else:
        print("\n❌ Priority 2: Committee Expansion - FAILED")
        print("   Review logs and address issues before proceeding")

if __name__ == "__main__":
    main()