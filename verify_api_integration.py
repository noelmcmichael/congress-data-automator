#!/usr/bin/env python3
"""
Verify API integration after leadership updates
"""
import os
import sys
sys.path.append('backend')

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.models.member import Member
from backend.app.models.committee import Committee

def verify_api_integration():
    """Verify that updated leadership data is accessible via database queries"""
    
    # Connect to PostgreSQL
    db_url = os.getenv('DATABASE_URL', 'postgresql://noelmcmichael@127.0.0.1:5432/congress_data')
    engine = create_engine(db_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    
    try:
        print("🔍 Verifying API integration after leadership updates...")
        
        # Test key leadership positions that should match Wikipedia
        test_cases = [
            ("Judiciary", "Senate", "Chuck Grassley", "Dick Durbin"),
            ("Armed Services", "Senate", "Roger Wicker", "Jack Reed"),
            ("Appropriations", "Senate", "Susan Collins", "Patty Murray"),
            ("Commerce, Science, and Transportation", "Senate", "Ted Cruz", "Maria Cantwell"),
            ("Finance", "Senate", "Mike Crapo", "Ron Wyden"),
        ]
        
        success_count = 0
        total_tests = len(test_cases)
        
        for committee_name, chamber, expected_chair, expected_ranking in test_cases:
            print(f"\n📋 Testing {committee_name} ({chamber}):")
            
            # Find committee
            committee = session.query(Committee).filter(
                Committee.name.ilike(f"%{committee_name}%"),
                Committee.chamber == chamber
            ).first()
            
            if not committee:
                print(f"   ❌ Committee not found")
                continue
            
            # Get chair
            chair = session.query(Member).filter(Member.id == committee.chair_member_id).first() if committee.chair_member_id else None
            ranking = session.query(Member).filter(Member.id == committee.ranking_member_id).first() if committee.ranking_member_id else None
            
            chair_name = f"{chair.first_name} {chair.last_name}" if chair else "None"
            ranking_name = f"{ranking.first_name} {ranking.last_name}" if ranking else "None"
            
            print(f"   👤 Chair: {chair_name} (Expected: {expected_chair})")
            print(f"   👤 Ranking: {ranking_name} (Expected: {expected_ranking})")
            
            # Check if matches
            chair_match = expected_chair in chair_name if chair else False
            ranking_match = expected_ranking in ranking_name if ranking else False
            
            if chair_match and ranking_match:
                print(f"   ✅ Perfect match!")
                success_count += 1
            elif chair_match:
                print(f"   ⚠️ Chair matches, ranking member different")
            elif ranking_match:
                print(f"   ⚠️ Ranking member matches, chair different")
            else:
                print(f"   ❌ No matches")
        
        print(f"\n📊 Verification Results:")
        print(f"   ✅ Perfect matches: {success_count}/{total_tests}")
        print(f"   📈 Success rate: {(success_count/total_tests)*100:.1f}%")
        
        # Test API-style queries
        print(f"\n🔌 Testing API-style queries:")
        
        # Query all committees with leadership
        committees_with_leadership = session.query(Committee).filter(
            Committee.chair_member_id.isnot(None),
            Committee.ranking_member_id.isnot(None)
        ).all()
        
        print(f"   📋 Committees with complete leadership: {len(committees_with_leadership)}")
        
        # Query members with chair positions
        chairs = session.query(Member).join(Committee, Member.id == Committee.chair_member_id).all()
        print(f"   👑 Members serving as chairs: {len(chairs)}")
        
        # Query members with ranking positions
        ranking_members = session.query(Member).join(Committee, Member.id == Committee.ranking_member_id).all()
        print(f"   🥈 Members serving as ranking members: {len(ranking_members)}")
        
        # Sample API response for Chuck Grassley
        grassley = session.query(Member).filter(
            Member.first_name.ilike("%Chuck%"),
            Member.last_name.ilike("%Grassley%")
        ).first()
        
        if grassley:
            chair_committees = session.query(Committee).filter(Committee.chair_member_id == grassley.id).all()
            ranking_committees = session.query(Committee).filter(Committee.ranking_member_id == grassley.id).all()
            
            print(f"\n👤 Chuck Grassley (ID: {grassley.id}):")
            print(f"   Chair of: {[c.name for c in chair_committees]}")
            print(f"   Ranking member of: {[c.name for c in ranking_committees]}")
        
        return success_count >= total_tests * 0.6  # 60% success threshold
        
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        session.close()

if __name__ == "__main__":
    success = verify_api_integration()
    sys.exit(0 if success else 1)