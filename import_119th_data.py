#!/usr/bin/env python3
"""
Import 119th Congress data from SQLite to PostgreSQL for reconciliation testing
"""
import os
import sys
import sqlite3
sys.path.append('backend')

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.models.member import Member
from backend.app.models.committee import Committee, CommitteeMembership

def import_119th_data():
    """Import data from congress_119th.db to PostgreSQL"""
    
    # Connect to SQLite
    sqlite_conn = sqlite3.connect('congress_119th.db')
    sqlite_cursor = sqlite_conn.cursor()
    
    # Connect to PostgreSQL
    db_url = os.getenv('DATABASE_URL', 'postgresql://noelmcmichael@127.0.0.1:5432/congress_data')
    engine = create_engine(db_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    pg_session = SessionLocal()
    
    try:
        print("🔄 Importing 119th Congress data...")
        
        # Import committees first
        sqlite_cursor.execute("""
            SELECT id, name, chamber, committee_type, chair_name, chair_party, chair_state,
                   ranking_member_name, ranking_member_party, ranking_member_state
            FROM committees_119th
        """)
        
        committees = sqlite_cursor.fetchall()
        committee_mapping = {}  # sqlite_id -> pg_id
        
        print(f"📋 Importing {len(committees)} committees...")
        for row in committees:
            sqlite_id, name, chamber, committee_type, chair_name, chair_party, chair_state, ranking_name, ranking_party, ranking_state = row
            
            committee = Committee(
                name=name,
                chamber=chamber,
                committee_type=committee_type,
                congress_session=119,
                is_active=True
            )
            
            pg_session.add(committee)
            pg_session.flush()  # Get the ID
            
            committee_mapping[sqlite_id] = committee.id
            print(f"  ✅ {name} ({chamber}) -> ID: {committee.id}")
        
        # Import members
        sqlite_cursor.execute("""
            SELECT id, name, party, state, chamber, district, bioguide_id
            FROM members_119th
        """)
        
        members = sqlite_cursor.fetchall()
        member_mapping = {}  # sqlite_id -> pg_id
        
        print(f"👥 Importing {len(members)} members...")
        for row in members:
            sqlite_id, name, party, state, chamber, district, bioguide_id = row
            
            # Parse name into first/last
            name_parts = name.split(", ")
            if len(name_parts) >= 2:
                last_name = name_parts[0]
                first_name = name_parts[1]
            else:
                name_parts = name.split()
                if len(name_parts) >= 2:
                    first_name = name_parts[0]
                    last_name = " ".join(name_parts[1:])
                else:
                    first_name = name
                    last_name = ""
            
            member = Member(
                first_name=first_name,
                last_name=last_name,
                party=party,
                state=state,
                chamber=chamber,
                district=str(district) if district else None,
                bioguide_id=bioguide_id or f"TMP{sqlite_id}",  # Temporary ID if none
                congress_session=119,
                is_current=True
            )
            
            pg_session.add(member)
            pg_session.flush()  # Get the ID
            
            member_mapping[sqlite_id] = member.id
            print(f"  ✅ {first_name} {last_name} ({party}-{state}) -> ID: {member.id}")
        
        # Import committee memberships
        sqlite_cursor.execute("""
            SELECT member_id, committee_id, position
            FROM committee_memberships_119th
        """)
        
        memberships = sqlite_cursor.fetchall()
        
        print(f"🔗 Importing {len(memberships)} committee memberships...")
        for row in memberships:
            sqlite_member_id, sqlite_committee_id, position = row
            
            pg_member_id = member_mapping.get(sqlite_member_id)
            pg_committee_id = committee_mapping.get(sqlite_committee_id)
            
            if pg_member_id and pg_committee_id:
                membership = CommitteeMembership(
                    member_id=pg_member_id,
                    committee_id=pg_committee_id,
                    position=position,
                    is_current=True
                )
                
                pg_session.add(membership)
                print(f"  ✅ Member {pg_member_id} -> Committee {pg_committee_id} ({position})")
        
        # Commit all changes
        pg_session.commit()
        
        # Verify import
        member_count = pg_session.query(Member).count()
        committee_count = pg_session.query(Committee).count()
        membership_count = pg_session.query(CommitteeMembership).count()
        
        print(f"\n✅ Import complete!")
        print(f"   Members: {member_count}")
        print(f"   Committees: {committee_count}")
        print(f"   Memberships: {membership_count}")
        
        # Show some sample data
        print(f"\n📊 Sample data:")
        sample_members = pg_session.query(Member).limit(3).all()
        for member in sample_members:
            print(f"   Member: {member.first_name} {member.last_name} ({member.party}-{member.state})")
        
        sample_committees = pg_session.query(Committee).limit(3).all()
        for committee in sample_committees:
            print(f"   Committee: {committee.name} ({committee.chamber})")
            
        return True
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        pg_session.rollback()
        return False
        
    finally:
        sqlite_conn.close()
        pg_session.close()

if __name__ == "__main__":
    success = import_119th_data()
    sys.exit(0 if success else 1)