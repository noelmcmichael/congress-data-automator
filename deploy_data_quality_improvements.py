#!/usr/bin/env python3
"""
Deploy data quality improvements to production
"""

import subprocess
import os
import sys
import requests
import time
import json
from datetime import datetime

# Configuration
CLOUD_SQL_INSTANCE = "chefgavin:us-central1:congressional-db"
DATABASE_NAME = "congress_data"
API_URL = "https://congressional-data-api-v2-1066017671167.us-central1.run.app"

def start_cloud_sql_proxy():
    """Start the Cloud SQL Proxy"""
    try:
        print("🔄 Starting Cloud SQL Proxy...")
        
        # Check if already running
        result = subprocess.run(['pgrep', '-f', 'cloud-sql-proxy'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Cloud SQL Proxy already running")
            return True
        
        # Start proxy in background
        proxy_process = subprocess.Popen([
            './cloud-sql-proxy',
            CLOUD_SQL_INSTANCE,
            '--private-ip'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a few seconds for proxy to start
        time.sleep(5)
        
        # Check if proxy is running
        if proxy_process.poll() is None:
            print("✅ Cloud SQL Proxy started successfully")
            return True
        else:
            print("❌ Cloud SQL Proxy failed to start")
            return False
            
    except Exception as e:
        print(f"❌ Error starting Cloud SQL Proxy: {e}")
        return False

def check_api_functionality():
    """Check current API functionality"""
    try:
        # Check health
        response = requests.get(f"{API_URL}/health", timeout=10)
        if response.status_code != 200:
            print(f"❌ API health check failed: {response.status_code}")
            return False
        
        print("✅ API is healthy")
        
        # Check current hearing committee coverage
        response = requests.get(f"{API_URL}/api/v1/hearings?limit=50", timeout=10)
        if response.status_code != 200:
            print(f"❌ Hearings endpoint failed: {response.status_code}")
            return False
        
        hearings = response.json()
        hearings_with_committee = sum(1 for h in hearings if h.get('committee_id'))
        coverage = (hearings_with_committee / len(hearings)) * 100 if hearings else 0
        
        print(f"📊 Current hearing committee coverage: {coverage:.1f}%")
        
        return True
        
    except Exception as e:
        print(f"❌ API functionality check failed: {e}")
        return False

def deploy_via_api_service():
    """Deploy by updating the existing API service"""
    try:
        print("🔄 Deploying via API service update...")
        
        # Build and deploy the API service with updated data
        # This would involve rebuilding the container with the SQL updates
        
        # For now, we'll create a deployment script that can be run manually
        deployment_script = f"""#!/bin/bash
# Deploy data quality improvements
set -e

echo "🚀 Deploying data quality improvements..."

# Build new container with SQL updates
echo "📦 Building container with SQL updates..."
docker build -t gcr.io/chefgavin/congress-api:data-quality-update .

# Push to registry
echo "📤 Pushing to registry..."
docker push gcr.io/chefgavin/congress-api:data-quality-update

# Deploy to Cloud Run
echo "🚀 Deploying to Cloud Run..."
gcloud run deploy congressional-data-api-v2 \\
  --image gcr.io/chefgavin/congress-api:data-quality-update \\
  --platform managed \\
  --region us-central1 \\
  --allow-unauthenticated \\
  --set-cloudsql-instances={CLOUD_SQL_INSTANCE} \\
  --set-env-vars DATABASE_URL="postgresql://postgres:mDf3S9ZnBpQqJvGsY1@localhost:5432/{DATABASE_NAME}?host=/cloudsql/{CLOUD_SQL_INSTANCE}"

echo "✅ Deployment complete!"
"""

        with open('deploy_data_quality.sh', 'w') as f:
            f.write(deployment_script)
        
        os.chmod('deploy_data_quality.sh', 0o755)
        
        print("✅ Deployment script created: deploy_data_quality.sh")
        return True
        
    except Exception as e:
        print(f"❌ Deployment script creation failed: {e}")
        return False

def create_sql_migration_script():
    """Create a comprehensive SQL migration script"""
    try:
        print("🔄 Creating SQL migration script...")
        
        # Read the hearing committee updates
        with open('hearing_committee_updates_20250708_101829.sql', 'r') as f:
            hearing_updates = f.read()
        
        # Create comprehensive migration script
        migration_script = f"""-- Congressional Data Quality Improvement Migration
-- Generated: {datetime.now().isoformat()}
-- Purpose: Deploy hearing committee relationships (0% → 48.5% coverage)

-- Begin transaction
BEGIN;

-- Add audit log table for tracking changes
CREATE TABLE IF NOT EXISTS data_quality_audit (
    id SERIAL PRIMARY KEY,
    operation_type VARCHAR(50) NOT NULL,
    table_name VARCHAR(50) NOT NULL,
    record_id INTEGER NOT NULL,
    old_value TEXT,
    new_value TEXT,
    executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    executed_by VARCHAR(50) DEFAULT 'data_quality_migration'
);

-- Create index for performance if not exists
CREATE INDEX IF NOT EXISTS idx_hearings_committee_id ON hearings(committee_id);

-- Apply hearing committee updates
{hearing_updates}

-- Log the migration
INSERT INTO data_quality_audit (operation_type, table_name, record_id, new_value) 
VALUES ('migration', 'hearings', 0, 'Applied hearing committee relationships - 97 updates');

-- Create view for data quality monitoring
CREATE OR REPLACE VIEW data_quality_status AS
SELECT 
    'hearings' as table_name,
    COUNT(*) as total_records,
    COUNT(committee_id) as records_with_committee,
    ROUND(COUNT(committee_id) * 100.0 / COUNT(*), 2) as coverage_percentage
FROM hearings
UNION ALL
SELECT 
    'members' as table_name,
    COUNT(*) as total_records,
    COUNT(CASE WHEN EXISTS (SELECT 1 FROM committee_memberships cm WHERE cm.member_id = members.id) THEN 1 END) as records_with_committee,
    ROUND(COUNT(CASE WHEN EXISTS (SELECT 1 FROM committee_memberships cm WHERE cm.member_id = members.id) THEN 1 END) * 100.0 / COUNT(*), 2) as coverage_percentage
FROM members;

-- Verify the changes
SELECT * FROM data_quality_status;

-- Commit transaction
COMMIT;

-- Final verification
SELECT 
    'Data Quality Improvement Migration Complete' as status,
    COUNT(*) as total_hearings,
    COUNT(committee_id) as hearings_with_committee,
    ROUND(COUNT(committee_id) * 100.0 / COUNT(*), 2) as coverage_percentage
FROM hearings;
"""
        
        with open('data_quality_migration.sql', 'w') as f:
            f.write(migration_script)
        
        print("✅ SQL migration script created: data_quality_migration.sql")
        return True
        
    except Exception as e:
        print(f"❌ SQL migration script creation failed: {e}")
        return False

def create_deployment_summary():
    """Create a deployment summary"""
    summary = {
        "deployment_date": datetime.now().isoformat(),
        "deployment_type": "data_quality_improvements",
        "scope": {
            "member_committee_coverage": "Already deployed (100%)",
            "hearing_committee_coverage": "To be deployed (0% → 48.5%)",
            "total_hearing_updates": 97
        },
        "files_created": [
            "deploy_data_quality.sh",
            "data_quality_migration.sql",
            "hearing_committee_deployment_20250708_103421.sql"
        ],
        "deployment_steps": [
            "1. Execute data_quality_migration.sql against production database",
            "2. Restart API service to pick up changes",
            "3. Validate hearing committee coverage improved to ~48.5%",
            "4. Test API endpoints for hearing committee filtering"
        ],
        "expected_improvements": {
            "hearing_committee_coverage": "48.5%",
            "total_relationships": 97,
            "api_functionality": "Hearing committee filtering enabled"
        }
    }
    
    with open('deployment_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print("✅ Deployment summary created: deployment_summary.json")
    return summary

def main():
    print("🚀 DATA QUALITY IMPROVEMENTS DEPLOYMENT")
    print("=" * 50)
    
    # Check current API functionality
    if not check_api_functionality():
        print("❌ API functionality check failed")
        return
    
    # Create SQL migration script
    if not create_sql_migration_script():
        print("❌ SQL migration script creation failed")
        return
    
    # Create deployment script  
    if not deploy_via_api_service():
        print("❌ Deployment script creation failed")
        return
    
    # Create deployment summary
    summary = create_deployment_summary()
    
    print("\n" + "=" * 50)
    print("📋 DEPLOYMENT PREPARATION COMPLETE")
    print("=" * 50)
    
    print("✅ Files created:")
    print("   - data_quality_migration.sql (comprehensive migration)")
    print("   - deploy_data_quality.sh (deployment script)")
    print("   - deployment_summary.json (summary)")
    
    print("\n🎯 DEPLOYMENT EXECUTION:")
    print("1. Execute SQL migration: data_quality_migration.sql")
    print("2. Restart API service (or run deploy_data_quality.sh)")
    print("3. Validate improvements")
    
    print("\n📈 EXPECTED RESULTS:")
    print("   - Hearing committee coverage: 0% → 48.5%")
    print("   - Total hearing updates: 97")
    print("   - API functionality: Hearing committee filtering enabled")
    
    print("\n🔧 MANUAL EXECUTION OPTIONS:")
    print("   A. Run SQL migration directly against database")
    print("   B. Execute ./deploy_data_quality.sh for full deployment")
    print("   C. Apply changes through Cloud Run container update")

if __name__ == "__main__":
    main()