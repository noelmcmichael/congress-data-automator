#!/usr/bin/env python3
"""
Upload full congressional dataset to production database.
"""
import json
import subprocess
import sys
import os
from datetime import datetime

def upload_dataset():
    """Upload the collected dataset to production database."""
    
    # Find the most recent collected members file
    import glob
    member_files = glob.glob("collected_members_full_*.json")
    if not member_files:
        print("❌ No collected members file found")
        return False
    
    latest_file = max(member_files, key=os.path.getctime)
    print(f"📄 Using dataset: {latest_file}")
    
    # Load the data
    with open(latest_file, 'r') as f:
        members = json.load(f)
    
    print(f"📊 Total members to upload: {len(members)}")
    
    # Create SQL script to upload members
    sql_script = """
-- Clear existing members (they'll be replaced with complete dataset)
DELETE FROM committee_memberships;
DELETE FROM members;

-- Insert all collected members
"""
    
    # Convert members to SQL INSERT statements
    for member in members:
        # Extract member data
        bioguide_id = member.get('bioguideId', '')
        name = member.get('name', '').replace("'", "''")
        first_name = member.get('firstName', '').replace("'", "''")
        last_name = member.get('lastName', '').replace("'", "''")
        party = member.get('partyName', '').replace("'", "''")
        state = member.get('state', '').replace("'", "''")
        
        # Get chamber from latest term
        terms = member.get('terms', {}).get('item', [])
        chamber = 'Unknown'
        if terms:
            latest_term = terms[-1]
            chamber_full = latest_term.get('chamber', '')
            if 'House' in chamber_full:
                chamber = 'House'
            elif 'Senate' in chamber_full:
                chamber = 'Senate'
        
        # Get district (for House members)
        district = member.get('district', 0) if member.get('district') else 0
        
        # Get image URL
        image_url = member.get('depiction', {}).get('imageUrl', '')
        
        # Create INSERT statement
        sql_script += f"""
INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
VALUES ('{bioguide_id}', '{name}', '{first_name}', '{last_name}', '{party}', '{state}', '{chamber}', {district}, '{image_url}', true);
"""
    
    # Write SQL script to file
    sql_file = f"upload_members_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
    with open(sql_file, 'w') as f:
        f.write(sql_script)
    
    print(f"✅ SQL script created: {sql_file}")
    
    # Execute SQL script using cloud-sql-proxy
    print("🚀 Uploading to production database...")
    try:
        # Start cloud-sql-proxy in background
        proxy_cmd = [
            "./cloud-sql-proxy", 
            "chefgavin:us-central1:congressional-db",
            "--port=5432"
        ]
        
        print("Starting Cloud SQL Proxy...")
        proxy_process = subprocess.Popen(proxy_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a moment for proxy to start
        import time
        time.sleep(5)
        
        # Execute SQL script
        psql_cmd = [
            "psql",
            "-h", "localhost",
            "-p", "5432", 
            "-U", "postgres",
            "-d", "congress_data",
            "-f", sql_file
        ]
        
        # Set password environment variable
        env = os.environ.copy()
        env['PGPASSWORD'] = 'mDf3S9ZnBpQqJvGsY1'
        
        print("Executing SQL script...")
        result = subprocess.run(psql_cmd, capture_output=True, text=True, env=env)
        
        if result.returncode == 0:
            print("✅ Database upload successful!")
            print(f"Output: {result.stdout}")
        else:
            print(f"❌ Database upload failed: {result.stderr}")
            return False
        
        # Stop proxy
        proxy_process.terminate()
        proxy_process.wait()
        
        return True
        
    except Exception as e:
        print(f"❌ Error uploading to database: {e}")
        return False

def verify_upload():
    """Verify the upload was successful."""
    import requests
    
    print("\n🔍 Verifying upload...")
    
    # Check production database stats
    production_url = "https://congressional-data-api-v2-1066017671167.us-central1.run.app"
    
    try:
        response = requests.get(f"{production_url}/api/v1/stats/database")
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ Production database stats: {stats}")
            
            members_total = stats.get('members', {}).get('total', 0)
            if members_total >= 535:
                print("✅ Upload verification successful!")
                return True
            else:
                print(f"⚠️  Only {members_total} members found, expected 535+")
                return False
        else:
            print(f"❌ Error getting stats: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error verifying upload: {e}")
        return False

if __name__ == "__main__":
    print("🚀 UPLOADING FULL CONGRESSIONAL DATASET")
    print("=" * 50)
    
    try:
        # Upload the dataset
        if upload_dataset():
            print("\n✅ Dataset uploaded successfully!")
            
            # Verify the upload
            if verify_upload():
                print("\n🎉 Full dataset upload and verification complete!")
            else:
                print("\n⚠️  Upload complete but verification failed")
        else:
            print("\n❌ Upload failed")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)