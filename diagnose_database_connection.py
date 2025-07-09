#!/usr/bin/env python3
"""
Database Connection Diagnosis
============================

Systematically diagnose and resolve Cloud SQL connection issues.
"""

import subprocess
import os
import time
import requests
from datetime import datetime

class DatabaseConnectionDiagnostic:
    def __init__(self):
        self.api_base = "https://politicalequity.io/api/v1"
        self.instance_name = "congressional-db"
        self.passwords_to_test = [
            "mDf3S9ZnBpQqJvGsY1",  # API working password
            "temp_deployment_password_123",  # Original deployment password
        ]
        
    def log_event(self, message: str, status: str = "info"):
        """Log diagnostic events"""
        timestamp = datetime.now().isoformat()
        symbol = {"info": "ℹ️", "success": "✅", "error": "❌", "warning": "⚠️"}.get(status, "ℹ️")
        print(f"[{timestamp}] {symbol} {message}")
        
    def test_api_connectivity(self):
        """Verify API is still working as baseline"""
        self.log_event("Testing API connectivity as baseline")
        try:
            response = requests.get(f"{self.api_base}/status", timeout=10)
            if response.status_code == 200:
                self.log_event("API connectivity confirmed", "success")
                return True
            else:
                self.log_event(f"API returned status {response.status_code}", "error")
                return False
        except Exception as e:
            self.log_event(f"API connectivity failed: {e}", "error")
            return False
    
    def check_gcloud_auth(self):
        """Check gcloud authentication status"""
        self.log_event("Checking gcloud authentication")
        try:
            result = subprocess.run([
                "/opt/homebrew/bin/gcloud", "auth", "list", 
                "--filter=status:ACTIVE", "--format=value(account)"
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0 and result.stdout.strip():
                account = result.stdout.strip()
                self.log_event(f"Authenticated as: {account}", "success")
                return account
            else:
                self.log_event("No active gcloud authentication", "error")
                return None
        except Exception as e:
            self.log_event(f"Failed to check gcloud auth: {e}", "error")
            return None
    
    def check_instance_status(self):
        """Check Cloud SQL instance status"""
        self.log_event("Checking Cloud SQL instance status")
        try:
            result = subprocess.run([
                "/opt/homebrew/bin/gcloud", "sql", "instances", "describe", 
                self.instance_name, "--format=value(state)"
            ], capture_output=True, text=True, timeout=15)
            
            if result.returncode == 0:
                state = result.stdout.strip()
                self.log_event(f"Instance state: {state}", "success" if state == "RUNNABLE" else "warning")
                return state
            else:
                self.log_event(f"Failed to check instance: {result.stderr}", "error")
                return None
        except Exception as e:
            self.log_event(f"Instance check failed: {e}", "error")
            return None
    
    def test_connection_method(self, password: str, method: str = "direct"):
        """Test database connection with specific password and method"""
        self.log_event(f"Testing {method} connection with password: {password[:4]}...")
        
        env = os.environ.copy()
        env["PGPASSWORD"] = password
        
        if method == "direct":
            # Direct gcloud sql connect
            cmd = [
                "/opt/homebrew/bin/gcloud", "sql", "connect", self.instance_name,
                "--user=postgres", "--quiet"
            ]
            sql_input = "SELECT 1;\n\\q"
            
        elif method == "proxy":
            # Using Cloud SQL proxy (if available)
            # This would require starting the proxy first
            self.log_event("Proxy method not implemented yet", "warning")
            return False
            
        try:
            result = subprocess.run(
                cmd, input=sql_input, text=True, 
                capture_output=True, env=env, timeout=30
            )
            
            if result.returncode == 0:
                self.log_event(f"{method} connection successful", "success")
                return True
            else:
                error_msg = result.stderr.strip()
                if "password authentication failed" in error_msg:
                    self.log_event(f"{method} connection failed: Password authentication", "error")
                elif "timeout" in error_msg.lower():
                    self.log_event(f"{method} connection failed: Timeout", "error")
                else:
                    self.log_event(f"{method} connection failed: {error_msg[:100]}", "error")
                return False
                
        except subprocess.TimeoutExpired:
            self.log_event(f"{method} connection timed out", "error")
            return False
        except Exception as e:
            self.log_event(f"{method} connection error: {e}", "error")
            return False
    
    def check_user_permissions(self):
        """Check database user and permissions"""
        self.log_event("Checking database user information")
        try:
            result = subprocess.run([
                "/opt/homebrew/bin/gcloud", "sql", "users", "list", 
                "--instance", self.instance_name, "--format=json"
            ], capture_output=True, text=True, timeout=15)
            
            if result.returncode == 0:
                import json
                users = json.loads(result.stdout)
                postgres_users = [u for u in users if u.get("name") == "postgres"]
                
                if postgres_users:
                    self.log_event("postgres user found", "success")
                    user_info = postgres_users[0]
                    # Log user details (without sensitive info)
                    self.log_event(f"User type: {user_info.get('type', 'unknown')}")
                    return True
                else:
                    self.log_event("postgres user not found", "error")
                    return False
            else:
                self.log_event(f"Failed to list users: {result.stderr}", "error")
                return False
        except Exception as e:
            self.log_event(f"User check failed: {e}", "error")
            return False
    
    def try_password_reset(self, new_password: str):
        """Attempt to reset the database password"""
        self.log_event(f"Attempting to reset password to: {new_password[:4]}...")
        try:
            result = subprocess.run([
                "/opt/homebrew/bin/gcloud", "sql", "users", "set-password", "postgres",
                "--instance", self.instance_name, "--password", new_password
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                self.log_event("Password reset successful", "success")
                # Wait a moment for propagation
                time.sleep(5)
                return True
            else:
                self.log_event(f"Password reset failed: {result.stderr}", "error")
                return False
        except Exception as e:
            self.log_event(f"Password reset error: {e}", "error")
            return False
    
    def find_working_connection(self):
        """Try to find a working database connection method"""
        self.log_event("🔍 Starting comprehensive database connection diagnosis")
        
        # 1. Baseline checks
        if not self.test_api_connectivity():
            self.log_event("API baseline failed - aborting diagnosis", "error")
            return None
            
        account = self.check_gcloud_auth()
        if not account:
            self.log_event("gcloud authentication required", "error")
            return None
            
        instance_state = self.check_instance_status()
        if instance_state != "RUNNABLE":
            self.log_event("Instance not in RUNNABLE state", "error")
            return None
            
        # 2. Check user permissions
        if not self.check_user_permissions():
            self.log_event("User permission issues detected", "warning")
        
        # 3. Test existing passwords
        for password in self.passwords_to_test:
            if self.test_connection_method(password, "direct"):
                self.log_event(f"Working connection found with password: {password[:4]}...", "success")
                return {"password": password, "method": "direct"}
        
        # 4. Try resetting to API password and test
        api_password = "mDf3S9ZnBpQqJvGsY1"
        self.log_event("No existing passwords work, trying fresh reset")
        
        if self.try_password_reset(api_password):
            if self.test_connection_method(api_password, "direct"):
                self.log_event("Fresh password reset successful", "success")
                return {"password": api_password, "method": "direct"}
        
        # 5. If still failing, try the Cloud SQL proxy approach
        self.log_event("Direct connections failing, will need alternative approach", "warning")
        return None
    
    def run_diagnosis(self):
        """Run complete database connection diagnosis"""
        start_time = datetime.now()
        
        working_config = self.find_working_connection()
        
        duration = (datetime.now() - start_time).total_seconds()
        
        if working_config:
            self.log_event(f"✅ Diagnosis completed successfully in {duration:.1f}s", "success")
            self.log_event(f"Working configuration: {working_config}", "success")
            return working_config
        else:
            self.log_event(f"❌ Diagnosis failed after {duration:.1f}s", "error")
            self.log_event("Will need to use alternative deployment method", "warning")
            return None

def main():
    diagnostic = DatabaseConnectionDiagnostic()
    result = diagnostic.run_diagnosis()
    
    if result:
        print(f"\n🎯 Database connection restored!")
        print(f"   Password: {result['password'][:4]}...")
        print(f"   Method: {result['method']}")
        print(f"   Ready to proceed with committee expansion")
        return True
    else:
        print(f"\n⚠️ Direct database connection not available")
        print(f"   Will use alternative deployment method")
        print(f"   Can still proceed with expansion")
        return False

if __name__ == "__main__":
    main()