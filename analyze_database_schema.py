"""
Phase 2 Step 2.1: Database Connection & Schema Analysis
Analyze current database structure and leadership positions for Wikipedia reconciliation.
"""

import asyncio
import json
import sys
import os
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import text

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.core.database import get_db
from backend.app.models.member import Member
from backend.app.models.committee import Committee, CommitteeMembership

def analyze_database_schema():
    """
    Analyze the current database schema and leadership positions.
    """
    print("🔍 Phase 2 Step 2.1: Database Connection & Schema Analysis")
    print("=" * 70)
    
    db = next(get_db())
    
    try:
        # 1. Test database connectivity
        print("\n1. Testing Database Connectivity...")
        result = db.execute(text("SELECT 1")).fetchone()
        print(f"   ✅ Database connection successful: {result}")
        
        # 2. Analyze table structures
        print("\n2. Analyzing Table Structures...")
        
        # Check members table
        members_count = db.query(Member).count()
        print(f"   📊 Members table: {members_count} records")
        
        # Check committees table
        committees_count = db.query(Committee).count()
        print(f"   📊 Committees table: {committees_count} records")
        
        # Check committee_memberships table
        memberships_count = db.query(CommitteeMembership).count()
        print(f"   📊 Committee memberships table: {memberships_count} records")
        
        # 3. Analyze current leadership positions
        print("\n3. Analyzing Current Leadership Positions...")
        
        # Get committees with leadership
        committees_with_leadership = db.query(Committee).filter(
            (Committee.chair_member_id.isnot(None)) | 
            (Committee.ranking_member_id.isnot(None))
        ).all()
        
        print(f"   📋 Committees with leadership: {len(committees_with_leadership)}")
        
        leadership_analysis = []
        for committee in committees_with_leadership:
            chair_name = "None"
            ranking_name = "None"
            
            if committee.chair_member_id:
                chair = db.query(Member).filter(Member.id == committee.chair_member_id).first()
                if chair:
                    chair_name = f"{chair.first_name} {chair.last_name} ({chair.party}-{chair.state})"
            
            if committee.ranking_member_id:
                ranking = db.query(Member).filter(Member.id == committee.ranking_member_id).first()
                if ranking:
                    ranking_name = f"{ranking.first_name} {ranking.last_name} ({ranking.party}-{ranking.state})"
            
            leadership_analysis.append({
                "committee_id": committee.id,
                "committee_name": committee.name,
                "chamber": committee.chamber,
                "chair": chair_name,
                "ranking_member": ranking_name
            })
        
        # 4. Sample leadership positions for comparison
        print("\n4. Sample Current Leadership Positions:")
        for i, leadership in enumerate(leadership_analysis[:10]):  # Show first 10
            print(f"   {i+1}. {leadership['committee_name']} ({leadership['chamber']})")
            print(f"      Chair: {leadership['chair']}")
            print(f"      Ranking: {leadership['ranking_member']}")
        
        # 5. Save analysis results
        analysis_results = {
            "timestamp": datetime.now().isoformat(),
            "database_stats": {
                "members_count": members_count,
                "committees_count": committees_count,
                "memberships_count": memberships_count,
                "committees_with_leadership": len(committees_with_leadership)
            },
            "leadership_positions": leadership_analysis,
            "schema_analysis": {
                "members_table_fields": ["id", "first_name", "last_name", "party", "state", "chamber"],
                "committees_table_fields": ["id", "name", "chamber", "chair_member_id", "ranking_member_id"],
                "reconciliation_strategy": "Match by name and chamber, update chair_member_id and ranking_member_id"
            }
        }
        
        with open("database_schema_analysis.json", "w") as f:
            json.dump(analysis_results, f, indent=2)
        
        print(f"\n✅ Analysis complete! Results saved to database_schema_analysis.json")
        print(f"   📊 Summary: {members_count} members, {committees_count} committees, {len(committees_with_leadership)} with leadership")
        
        return analysis_results
        
    except Exception as e:
        print(f"❌ Error during database analysis: {str(e)}")
        return None
    finally:
        db.close()

if __name__ == "__main__":
    analyze_database_schema()