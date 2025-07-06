#!/usr/bin/env python3
"""
Export real congressional data from production database to static JSON files.
This bypasses deployment issues and provides real data to frontend immediately.
"""
import os
import json
import sys
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Database connection (same as production)
DATABASE_URL = "postgresql+psycopg2://postgres:Noel19922024@localhost:5433/congress_data"

def export_real_data():
    """Export real data from production database."""
    
    print("🔄 Connecting to production database via Cloud SQL Proxy...")
    
    # Create engine with production database URL
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Test connection
        result = session.execute(text("SELECT COUNT(*) FROM members"))
        member_count = result.scalar()
        print(f"✅ Connected! Found {member_count} members in database")
        
        # Export members
        print("📥 Exporting members...")
        members_result = session.execute(text("""
            SELECT id, bioguide_id, first_name, last_name, middle_name, nickname, 
                   party, chamber, state, district, is_current, official_photo_url,
                   created_at, updated_at, last_scraped_at
            FROM members 
            ORDER BY last_name, first_name
            LIMIT 100
        """))
        
        members = []
        for row in members_result:
            members.append({
                "id": row.id,
                "bioguide_id": row.bioguide_id,
                "first_name": row.first_name,
                "last_name": row.last_name,
                "middle_name": row.middle_name,
                "nickname": row.nickname,
                "party": row.party,
                "chamber": row.chamber,
                "state": row.state,
                "district": row.district,
                "is_current": row.is_current,
                "official_photo_url": row.official_photo_url,
                "created_at": row.created_at.isoformat() if row.created_at else None,
                "updated_at": row.updated_at.isoformat() if row.updated_at else None,
                "last_scraped_at": row.last_scraped_at.isoformat() if row.last_scraped_at else None,
            })
        
        # Export committees  
        print("📥 Exporting committees...")
        committees_result = session.execute(text("""
            SELECT id, name, chamber, committee_code, congress_gov_id, is_active, 
                   is_subcommittee, parent_committee_id, website_url,
                   created_at, updated_at
            FROM committees 
            WHERE is_active = true
            ORDER BY name
            LIMIT 100
        """))
        
        committees = []
        for row in committees_result:
            committees.append({
                "id": row.id,
                "name": row.name,
                "chamber": row.chamber,
                "committee_code": row.committee_code,
                "congress_gov_id": row.congress_gov_id,
                "is_active": row.is_active,
                "is_subcommittee": row.is_subcommittee,
                "parent_committee_id": row.parent_committee_id,
                "website_url": row.website_url,
                "created_at": row.created_at.isoformat() if row.created_at else None,
                "updated_at": row.updated_at.isoformat() if row.updated_at else None,
            })
        
        # Export hearings
        print("📥 Exporting hearings...")
        hearings_result = session.execute(text("""
            SELECT id, congress_gov_id, title, description, committee_id,
                   scheduled_date, start_time, end_time, location, room,
                   hearing_type, status, transcript_url, video_url, webcast_url,
                   congress_session, congress_number, scraped_video_urls,
                   created_at, updated_at, last_scraped_at
            FROM hearings 
            ORDER BY created_at DESC
            LIMIT 100
        """))
        
        hearings = []
        for row in hearings_result:
            hearings.append({
                "id": row.id,
                "congress_gov_id": row.congress_gov_id,
                "title": row.title,
                "description": row.description,
                "committee_id": row.committee_id,
                "scheduled_date": row.scheduled_date.isoformat() if row.scheduled_date else None,
                "start_time": row.start_time.isoformat() if row.start_time else None,
                "end_time": row.end_time.isoformat() if row.end_time else None,
                "location": row.location,
                "room": row.room,
                "hearing_type": row.hearing_type,
                "status": row.status,
                "transcript_url": row.transcript_url,
                "video_url": row.video_url,
                "webcast_url": row.webcast_url,
                "congress_session": row.congress_session,
                "congress_number": row.congress_number,
                "scraped_video_urls": row.scraped_video_urls,
                "created_at": row.created_at.isoformat() if row.created_at else None,
                "updated_at": row.updated_at.isoformat() if row.updated_at else None,
                "last_scraped_at": row.last_scraped_at.isoformat() if row.last_scraped_at else None,
            })
        
        # Save to files
        os.makedirs("frontend/src/data", exist_ok=True)
        
        with open("frontend/src/data/realMembers.json", "w") as f:
            json.dump(members, f, indent=2)
        
        with open("frontend/src/data/realCommittees.json", "w") as f:
            json.dump(committees, f, indent=2)
            
        with open("frontend/src/data/realHearings.json", "w") as f:
            json.dump(hearings, f, indent=2)
        
        print(f"✅ Successfully exported:")
        print(f"   📊 {len(members)} members")
        print(f"   📊 {len(committees)} committees") 
        print(f"   📊 {len(hearings)} hearings")
        print(f"📁 Files saved to frontend/src/data/")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
        
    finally:
        session.close()

if __name__ == "__main__":
    if not export_real_data():
        sys.exit(1)