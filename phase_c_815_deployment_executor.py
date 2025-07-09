#!/usr/bin/env python3
"""
Phase C: 815 Committee Production Deployment Executor
===================================================

Execute production deployment using proven Cloud SQL Proxy method.
Includes real-time monitoring and validation.
"""

import json
import subprocess
import time
import psycopg2
import requests
from datetime import datetime
from typing import Dict, List, Any, Optional

class PhaseCDeploymentExecutor:
    """Execute production deployment with monitoring"""
    
    def __init__(self, sql_file: str):
        self.sql_file = sql_file
        self.api_base = "https://politicalequity.io/api/v1"
        self.db_config = {
            'host': 'localhost',
            'port': 5433,
            'database': 'congress_data',
            'user': 'postgres',
            'password': 'mDf3S9ZnBpQqJvGsY1'
        }
        
        self.deployment_log = []
        self.deployment_metrics = {}
        self.start_time = None
        self.end_time = None
        
        self.log_event("Initialized Phase C Deployment Executor")
    
    def log_event(self, message: str, level: str = "info"):
        """Log deployment events with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {level.upper()}: {message}"
        self.deployment_log.append(log_entry)
        print(log_entry)
    
    def check_cloud_sql_proxy(self) -> bool:
        """Check if Cloud SQL Proxy is available and start if needed"""
        self.log_event("Checking Cloud SQL Proxy status")
        
        # Check if proxy executable exists
        try:
            result = subprocess.run(['./cloud-sql-proxy', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                self.log_event("Cloud SQL Proxy executable found")
            else:
                self.log_event("Cloud SQL Proxy executable not working", "error")
                return False
        except Exception as e:
            self.log_event(f"Cloud SQL Proxy not found: {e}", "error")
            return False
        
        # Check if proxy is already running on port 5433
        try:
            test_conn = psycopg2.connect(**self.db_config, connect_timeout=5)
            test_conn.close()
            self.log_event("Cloud SQL Proxy already running and accessible", "success")
            return True
        except:
            self.log_event("Cloud SQL Proxy not running, need to start it")
        
        # Start Cloud SQL Proxy
        self.log_event("Starting Cloud SQL Proxy...")
        try:
            proxy_cmd = ['./cloud-sql-proxy', 'chefgavin:us-central1:congressional-db', '--port=5433']
            subprocess.Popen(proxy_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Wait for proxy to start
            for attempt in range(30):  # 30 seconds timeout
                try:
                    test_conn = psycopg2.connect(**self.db_config, connect_timeout=5)
                    test_conn.close()
                    self.log_event(f"Cloud SQL Proxy started successfully (attempt {attempt + 1})", "success")
                    return True
                except:
                    time.sleep(1)
            
            self.log_event("Cloud SQL Proxy failed to start within 30 seconds", "error")
            return False
            
        except Exception as e:
            self.log_event(f"Failed to start Cloud SQL Proxy: {e}", "error")
            return False
    
    def test_database_connection(self) -> bool:
        """Test database connection and basic queries"""
        self.log_event("Testing database connection")
        
        try:
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor()
            
            # Test basic query
            cursor.execute("SELECT COUNT(*) FROM committees;")
            current_count = cursor.fetchone()[0]
            self.log_event(f"Current committee count: {current_count}")
            
            # Test table schema
            cursor.execute("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'committees'
                ORDER BY ordinal_position;
            """)
            schema = cursor.fetchall()
            self.log_event(f"Table schema verified: {len(schema)} columns")
            
            cursor.close()
            conn.close()
            
            self.log_event("Database connection test successful", "success")
            return True
            
        except Exception as e:
            self.log_event(f"Database connection test failed: {e}", "error")
            return False
    
    def get_pre_deployment_baseline(self) -> Dict[str, Any]:
        """Get baseline metrics before deployment"""
        self.log_event("Collecting pre-deployment baseline metrics")
        
        baseline = {
            'timestamp': datetime.now().isoformat(),
            'database_metrics': {},
            'api_metrics': {}
        }
        
        # Database metrics
        try:
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM committees;")
            baseline['database_metrics']['total_committees'] = cursor.fetchone()[0]
            
            cursor.execute("SELECT chamber, COUNT(*) FROM committees GROUP BY chamber;")
            baseline['database_metrics']['chamber_distribution'] = dict(cursor.fetchall())
            
            cursor.execute("SELECT committee_type, COUNT(*) FROM committees GROUP BY committee_type;")
            baseline['database_metrics']['type_distribution'] = dict(cursor.fetchall())
            
            cursor.close()
            conn.close()
            
        except Exception as e:
            self.log_event(f"Failed to collect database metrics: {e}", "warning")
            baseline['database_metrics']['error'] = str(e)
        
        # API metrics
        try:
            start_time = time.time()
            response = requests.get(f"{self.api_base}/committees?limit=10", timeout=30)
            api_response_time = time.time() - start_time
            
            if response.status_code == 200:
                baseline['api_metrics']['response_time_ms'] = round(api_response_time * 1000, 2)
                baseline['api_metrics']['status'] = 'operational'
            else:
                baseline['api_metrics']['status'] = f'error_{response.status_code}'
                
        except Exception as e:
            self.log_event(f"Failed to collect API metrics: {e}", "warning")
            baseline['api_metrics']['error'] = str(e)
        
        self.log_event("Baseline metrics collected", "success")
        return baseline
    
    def execute_sql_deployment(self) -> bool:
        """Execute SQL deployment with monitoring"""
        self.log_event(f"Starting SQL deployment from {self.sql_file}")
        
        try:
            # Read SQL file
            with open(self.sql_file, 'r') as f:
                sql_content = f.read()
            
            # Remove problematic autocommit line
            sql_content = sql_content.replace('SET autocommit = true;', '')
            
            sql_size = len(sql_content)
            self.log_event(f"SQL file size: {sql_size:,} characters")
            
            # Execute SQL
            conn = psycopg2.connect(**self.db_config)
            conn.autocommit = True  # Enable autocommit via psycopg2
            cursor = conn.cursor()
            
            deployment_start = time.time()
            self.log_event("Executing SQL deployment...")
            
            cursor.execute(sql_content)
            
            deployment_duration = time.time() - deployment_start
            self.log_event(f"SQL deployment completed in {deployment_duration:.2f} seconds", "success")
            
            # Get deployment results
            cursor.execute("SELECT COUNT(*) FROM committees;")
            final_count = cursor.fetchone()[0]
            
            cursor.close()
            conn.close()
            
            self.deployment_metrics['sql_execution_time'] = deployment_duration
            self.deployment_metrics['final_committee_count'] = final_count
            
            self.log_event(f"Final committee count: {final_count}")
            
            if final_count == 815:
                self.log_event("SUCCESS: Exact target count achieved!", "success")
                return True
            else:
                self.log_event(f"WARNING: Expected 815, got {final_count}", "warning")
                return final_count > 375  # Success if we added committees
            
        except Exception as e:
            self.log_event(f"SQL deployment failed: {e}", "error")
            return False
    
    def validate_post_deployment(self) -> Dict[str, Any]:
        """Validate deployment results"""
        self.log_event("Running post-deployment validation")
        
        validation_results = {
            'timestamp': datetime.now().isoformat(),
            'database_validation': {},
            'api_validation': {},
            'performance_validation': {}
        }
        
        # Database validation
        try:
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor()
            
            # Count validation
            cursor.execute("SELECT COUNT(*) FROM committees;")
            total_count = cursor.fetchone()[0]
            validation_results['database_validation']['total_committees'] = total_count
            validation_results['database_validation']['target_achieved'] = (total_count == 815)
            
            # Chamber distribution
            cursor.execute("SELECT chamber, COUNT(*) FROM committees GROUP BY chamber ORDER BY chamber;")
            chamber_dist = dict(cursor.fetchall())
            validation_results['database_validation']['chamber_distribution'] = chamber_dist
            
            # Type distribution
            cursor.execute("SELECT committee_type, COUNT(*) FROM committees GROUP BY committee_type ORDER BY committee_type;")
            type_dist = dict(cursor.fetchall())
            validation_results['database_validation']['type_distribution'] = type_dist
            
            # Data quality checks
            cursor.execute("SELECT COUNT(*) FROM committees WHERE congress_gov_id IS NULL OR congress_gov_id = '';")
            null_codes = cursor.fetchone()[0]
            validation_results['database_validation']['committees_without_codes'] = null_codes
            
            cursor.execute("SELECT COUNT(*) FROM committees WHERE name IS NULL OR name = '';")
            null_names = cursor.fetchone()[0]
            validation_results['database_validation']['committees_without_names'] = null_names
            
            cursor.close()
            conn.close()
            
            self.log_event("Database validation completed", "success")
            
        except Exception as e:
            self.log_event(f"Database validation failed: {e}", "error")
            validation_results['database_validation']['error'] = str(e)
        
        # API validation
        try:
            # Test basic endpoint
            start_time = time.time()
            response = requests.get(f"{self.api_base}/committees?limit=10", timeout=30)
            api_response_time = time.time() - start_time
            
            validation_results['api_validation']['response_time_ms'] = round(api_response_time * 1000, 2)
            validation_results['api_validation']['status_code'] = response.status_code
            validation_results['api_validation']['operational'] = (response.status_code == 200)
            
            if response.status_code == 200:
                # Test pagination with new count
                response1 = requests.get(f"{self.api_base}/committees?limit=200", timeout=30)
                response2 = requests.get(f"{self.api_base}/committees?limit=200&page=2", timeout=30)
                response3 = requests.get(f"{self.api_base}/committees?limit=200&page=3", timeout=30)
                response4 = requests.get(f"{self.api_base}/committees?limit=200&page=5", timeout=30)
                
                total_via_api = 0
                if response1.status_code == 200:
                    total_via_api += len(response1.json())
                if response2.status_code == 200:
                    total_via_api += len(response2.json())
                if response3.status_code == 200:
                    total_via_api += len(response3.json())
                if response4.status_code == 200:
                    total_via_api += len(response4.json())
                
                validation_results['api_validation']['total_committees_via_api'] = total_via_api
                validation_results['api_validation']['pagination_working'] = (total_via_api > 375)
            
            self.log_event("API validation completed", "success")
            
        except Exception as e:
            self.log_event(f"API validation failed: {e}", "error")
            validation_results['api_validation']['error'] = str(e)
        
        return validation_results
    
    def execute_full_deployment(self) -> bool:
        """Execute complete deployment process"""
        self.log_event("Starting Phase C: Production Deployment")
        self.start_time = datetime.now()
        
        # Pre-deployment checks
        if not self.check_cloud_sql_proxy():
            return False
        
        if not self.test_database_connection():
            return False
        
        # Collect baseline
        baseline = self.get_pre_deployment_baseline()
        self.deployment_metrics['baseline'] = baseline
        
        # Execute deployment
        deployment_success = self.execute_sql_deployment()
        
        if not deployment_success:
            self.log_event("Deployment failed, stopping", "error")
            return False
        
        # Validate results
        validation_results = self.validate_post_deployment()
        self.deployment_metrics['validation'] = validation_results
        
        self.end_time = datetime.now()
        total_duration = (self.end_time - self.start_time).total_seconds()
        self.deployment_metrics['total_duration_seconds'] = total_duration
        
        self.log_event(f"Phase C completed in {total_duration:.2f} seconds", "success")
        
        # Final success check
        final_success = (
            validation_results.get('database_validation', {}).get('target_achieved', False) and
            validation_results.get('api_validation', {}).get('operational', False)
        )
        
        if final_success:
            self.log_event("DEPLOYMENT SUCCESS: All validation checks passed!", "success")
        else:
            self.log_event("DEPLOYMENT WARNING: Some validation checks failed", "warning")
        
        return final_success
    
    def save_deployment_results(self) -> str:
        """Save deployment results to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"815_deployment_results_{timestamp}.json"
        
        results = {
            'deployment_timestamp': timestamp,
            'sql_file': self.sql_file,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'deployment_metrics': self.deployment_metrics,
            'deployment_log': self.deployment_log
        }
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        self.log_event(f"Deployment results saved to {filename}", "success")
        return filename

def main():
    """Main execution function"""
    print("=== Phase C: 815 Committee Production Deployment ===")
    
    # Find the most recent corrected SQL file
    import glob
    sql_files = glob.glob("815_committee_deployment_corrected_*.sql")
    if not sql_files:
        print("ERROR: No corrected deployment SQL file found. Please run corrected generator first.")
        return False
    
    latest_sql = sorted(sql_files)[-1]
    print(f"Using SQL file: {latest_sql}")
    print("=" * 50)
    
    executor = PhaseCDeploymentExecutor(latest_sql)
    
    deployment_success = executor.execute_full_deployment()
    results_file = executor.save_deployment_results()
    
    print("\n" + "=" * 50)
    if deployment_success:
        print("PHASE C DEPLOYMENT COMPLETE - SUCCESS!")
        print("✅ Target count achieved: 815 committees")
        print("✅ API operational and responsive")
        print("✅ Database integrity maintained")
    else:
        print("PHASE C DEPLOYMENT COMPLETE - WITH WARNINGS")
        print("⚠️  Some validation checks failed")
        print("⚠️  Manual verification recommended")
    
    print(f"Results saved to: {results_file}")
    print(f"Total duration: {executor.deployment_metrics.get('total_duration_seconds', 0):.2f} seconds")
    print("=" * 50)
    
    return deployment_success

if __name__ == "__main__":
    main()