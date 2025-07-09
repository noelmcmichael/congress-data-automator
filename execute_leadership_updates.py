#!/usr/bin/env python3
"""
Execute leadership updates from reconciliation
"""
import os
import sys
sys.path.append('backend')

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from backend.app.models.member import Member
from backend.app.models.committee import Committee

def execute_leadership_updates():
    """Execute the generated SQL leadership updates"""
    
    # Connect to PostgreSQL
    db_url = os.getenv('DATABASE_URL', 'postgresql://noelmcmichael@127.0.0.1:5432/congress_data')
    engine = create_engine(db_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    
    try:
        print("🔄 Executing leadership updates...")
        
        # Read SQL statements
        with open('leadership_updates.sql', 'r') as f:
            sql_statements = [line.strip() for line in f if line.strip()]
        
        print(f"📜 Found {len(sql_statements)} SQL statements to execute")
        
        # Execute each statement
        executed_count = 0
        for i, sql in enumerate(sql_statements, 1):
            try:
                result = session.execute(text(sql))
                executed_count += 1
                print(f"   ✅ {i}. {sql}")
            except Exception as e:
                print(f"   ❌ {i}. Failed: {sql} - Error: {e}")
        
        # Commit changes
        session.commit()
        print(f"\n✅ Executed {executed_count}/{len(sql_statements)} updates successfully")
        
        # Verify changes by checking some leadership positions
        print(f"\n🔍 Verification - Sample Leadership Positions:")
        
        # Check some key committees
        committees_to_check = [
            ('Judiciary', 'Senate'),
            ('Agriculture, Nutrition, and Forestry', 'Senate'),
            ('Appropriations', 'Senate'),
            ('Armed Services', 'Senate')
        ]
        
        for committee_name, chamber in committees_to_check:
            committee = session.query(Committee).filter(
                Committee.name.ilike(f"%{committee_name}%"),
                Committee.chamber == chamber
            ).first()
            
            if committee:
                chair = session.query(Member).filter(Member.id == committee.chair_member_id).first() if committee.chair_member_id else None
                ranking = session.query(Member).filter(Member.id == committee.ranking_member_id).first() if committee.ranking_member_id else None
                
                chair_name = f"{chair.first_name} {chair.last_name}" if chair else "None"
                ranking_name = f"{ranking.first_name} {ranking.last_name}" if ranking else "None"
                
                print(f"   📋 {committee.name} ({chamber}):")
                print(f"      Chair: {chair_name}")
                print(f"      Ranking Member: {ranking_name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Leadership updates failed: {e}")
        session.rollback()
        return False
        
    finally:
        session.close()

if __name__ == "__main__":
    success = execute_leadership_updates()
    sys.exit(0 if success else 1)