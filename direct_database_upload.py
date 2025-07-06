#!/usr/bin/env python3
"""
Direct database upload using SQLAlchemy and the same connection as the API.
"""
import json
import glob
import os
import sys
from datetime import datetime
from typing import List, Dict, Any
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

def get_database_url() -> str:
    """Get the database URL for direct connection."""
    return "postgresql://postgres:mDf3S9ZnBpQqJvGsY1@127.0.0.1:5432/congress_data"

def load_collected_data() -> List[Dict[str, Any]]:
    """Load the most recent collected members data."""
    member_files = glob.glob("collected_members_full_*.json")
    if not member_files:
        raise FileNotFoundError("No collected members file found")
    
    latest_file = max(member_files, key=os.path.getctime)
    print(f"📄 Using dataset: {latest_file}")
    
    with open(latest_file, 'r') as f:
        members = json.load(f)
    
    print(f"📊 Total members to upload: {len(members)}")
    return members

def start_cloud_sql_proxy():
    """Start the Cloud SQL Proxy."""
    import subprocess
    import time
    
    proxy_cmd = [
        "./cloud-sql-proxy", 
        "chefgavin:us-central1:congressional-db",
        "--port=5432"
    ]
    
    print("🔌 Starting Cloud SQL Proxy...")
    proxy_process = subprocess.Popen(proxy_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Wait for proxy to start
    time.sleep(5)
    
    # Test connection
    try:
        engine = create_engine(get_database_url())
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Database connection established")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        proxy_process.terminate()
        return None
    
    return proxy_process

def upload_members_to_database(members: List[Dict[str, Any]]) -> bool:
    """Upload members to the database."""
    
    # Start proxy
    proxy_process = start_cloud_sql_proxy()
    if not proxy_process:
        return False
    
    try:
        # Create database connection
        engine = create_engine(get_database_url())
        Session = sessionmaker(bind=engine)
        session = Session()
        
        print("🗑️  Clearing existing members...")
        # Clear existing data
        session.execute(text("DELETE FROM committee_memberships"))
        session.execute(text("DELETE FROM members"))
        session.commit()
        
        print("📥 Uploading new members...")
        # Upload new members
        uploaded_count = 0
        
        for member in members:
            try:
                # Extract member data
                bioguide_id = member.get('bioguideId', '')
                name = member.get('name', '')
                first_name = member.get('firstName', '')
                last_name = member.get('lastName', '')
                party = member.get('partyName', '')
                state = member.get('state', '')
                
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
                district = member.get('district')
                if district is None:
                    district = 0
                
                # Get image URL
                image_url = member.get('depiction', {}).get('imageUrl', '')
                
                # Insert member
                insert_sql = text("""
                    INSERT INTO members (bioguide_id, name, first_name, last_name, party, state, chamber, district, image_url, is_current)
                    VALUES (:bioguide_id, :name, :first_name, :last_name, :party, :state, :chamber, :district, :image_url, :is_current)
                """)
                
                session.execute(insert_sql, {
                    'bioguide_id': bioguide_id,
                    'name': name,
                    'first_name': first_name,
                    'last_name': last_name,
                    'party': party,
                    'state': state,
                    'chamber': chamber,
                    'district': district,
                    'image_url': image_url,
                    'is_current': True
                })
                
                uploaded_count += 1
                
                if uploaded_count % 50 == 0:
                    print(f"  📊 Uploaded {uploaded_count} members...")
                
            except Exception as e:
                print(f"❌ Error uploading member {member.get('name', 'Unknown')}: {e}")
                continue
        
        # Commit all changes
        session.commit()
        print(f"✅ Successfully uploaded {uploaded_count} members")
        
        session.close()
        
        # Stop proxy
        proxy_process.terminate()
        proxy_process.wait()
        
        return True
        
    except Exception as e:
        print(f"❌ Error during upload: {e}")
        proxy_process.terminate()
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
    print("🚀 DIRECT DATABASE UPLOAD OF CONGRESSIONAL DATASET")
    print("=" * 60)
    
    try:
        # Load collected data
        members = load_collected_data()
        
        # Upload to database
        if upload_members_to_database(members):
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