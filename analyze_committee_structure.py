#!/usr/bin/env python3

"""
Step 1: Database Schema Analysis
Analyze current committee table structure and identify required URL columns
"""

import psycopg2
from psycopg2.extras import RealDictCursor
import os
import json
from datetime import datetime

def connect_to_database():
    """Connect to Cloud SQL database via proxy"""
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5433,
            database="congress_data",
            user="postgres",
            password="mDf3S9ZnBpQqJvGsY1"
        )
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

def analyze_committee_structure():
    """Analyze current committee table structure"""
    conn = connect_to_database()
    if not conn:
        return
    
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Get table structure
        cursor.execute("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_name = 'committees'
            ORDER BY ordinal_position;
        """)
        
        columns = cursor.fetchall()
        print("📊 CURRENT COMMITTEE TABLE STRUCTURE:")
        print("=" * 60)
        for col in columns:
            print(f"  {col['column_name']:<20} {col['data_type']:<15} {'NULL' if col['is_nullable'] == 'YES' else 'NOT NULL'}")
        
        # Get sample committee data
        cursor.execute("""
            SELECT id, name, chamber, committee_type, description, website, is_subcommittee
            FROM committees
            WHERE is_subcommittee = FALSE OR is_subcommittee IS NULL
            ORDER BY chamber, name
            LIMIT 10;
        """)
        
        sample_committees = cursor.fetchall()
        print("\n🏛️ SAMPLE STANDING COMMITTEES:")
        print("=" * 60)
        for committee in sample_committees:
            print(f"  {committee['id']:<3} {committee['chamber']:<6} {committee['name'][:40]:<42}")
            if committee['website']:
                print(f"      Website: {committee['website']}")
        
        # Get committee counts by chamber and type
        cursor.execute("""
            SELECT chamber, committee_type, 
                   COUNT(*) as count,
                   COUNT(CASE WHEN is_subcommittee = TRUE THEN 1 END) as subcommittees
            FROM committees
            GROUP BY chamber, committee_type
            ORDER BY chamber, committee_type;
        """)
        
        counts = cursor.fetchall()
        print("\n📈 COMMITTEE COUNTS BY CHAMBER AND TYPE:")
        print("=" * 60)
        for count in counts:
            print(f"  {count['chamber']:<10} {count['committee_type']:<15} {count['count']:<5} ({count['subcommittees']} subcommittees)")
        
        # Identify committees that need URLs
        cursor.execute("""
            SELECT COUNT(*) as total_committees,
                   COUNT(CASE WHEN website IS NOT NULL THEN 1 END) as with_website,
                   COUNT(CASE WHEN website IS NULL THEN 1 END) as without_website
            FROM committees
            WHERE is_subcommittee = FALSE OR is_subcommittee IS NULL;
        """)
        
        url_status = cursor.fetchone()
        print(f"\n🔗 URL STATUS FOR MAIN COMMITTEES:")
        print("=" * 60)
        print(f"  Total Main Committees: {url_status['total_committees']}")
        print(f"  With Website: {url_status['with_website']}")
        print(f"  Without Website: {url_status['without_website']}")
        
        # Create analysis report
        analysis_report = {
            "timestamp": datetime.now().isoformat(),
            "table_structure": [dict(col) for col in columns],
            "sample_committees": [dict(committee) for committee in sample_committees],
            "counts_by_chamber": [dict(count) for count in counts],
            "url_status": dict(url_status),
            "required_columns": [
                {"name": "hearings_url", "type": "VARCHAR(255)", "description": "Official hearings page URL"},
                {"name": "members_url", "type": "VARCHAR(255)", "description": "Official members page URL"},
                {"name": "official_website", "type": "VARCHAR(255)", "description": "Main committee website URL"},
                {"name": "last_url_update", "type": "TIMESTAMP", "description": "Last time URLs were updated"}
            ]
        }
        
        with open('committee_structure_analysis.json', 'w') as f:
            json.dump(analysis_report, f, indent=2, default=str)
        
        print(f"\n✅ ANALYSIS COMPLETE")
        print(f"📁 Report saved to: committee_structure_analysis.json")
        
    except Exception as e:
        print(f"Analysis error: {e}")
    
    finally:
        conn.close()

if __name__ == "__main__":
    analyze_committee_structure()