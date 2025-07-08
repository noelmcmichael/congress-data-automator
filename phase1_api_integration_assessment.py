#!/usr/bin/env python3
"""
Phase 1.1: API Integration Assessment
Examine current API connection to 119th Congress database and identify compatibility issues.
"""

import sqlite3
import os
from datetime import datetime
import json

def assess_119th_congress_database():
    """Assess the 119th Congress database structure and content."""
    
    db_path = "congress_119th.db"
    if not os.path.exists(db_path):
        return {"error": "119th Congress database not found"}
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    assessment = {
        "timestamp": datetime.now().isoformat(),
        "database_path": db_path,
        "tables": {},
        "data_summary": {},
        "schema_compatibility": {},
        "recommendations": []
    }
    
    # Get table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    assessment["tables"]["found"] = tables
    
    # Analyze each table
    for table in tables:
        # Get schema
        cursor.execute(f"PRAGMA table_info({table})")
        columns = cursor.fetchall()
        assessment["tables"][table] = {
            "columns": [{"name": col[1], "type": col[2], "nullable": not col[3], "primary_key": col[5]} for col in columns]
        }
        
        # Get row count
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        assessment["data_summary"][table] = {"row_count": count}
        
        # Get sample data for non-empty tables
        if count > 0:
            cursor.execute(f"SELECT * FROM {table} LIMIT 3")
            sample_data = cursor.fetchall()
            assessment["data_summary"][table]["sample_data"] = sample_data
    
    # Analyze 119th Congress specific data
    if "members_119th" in tables:
        cursor.execute("SELECT party, COUNT(*) FROM members_119th GROUP BY party")
        party_breakdown = dict(cursor.fetchall())
        assessment["data_summary"]["members_119th"]["party_breakdown"] = party_breakdown
        
        cursor.execute("SELECT chamber, COUNT(*) FROM members_119th GROUP BY chamber")
        chamber_breakdown = dict(cursor.fetchall())
        assessment["data_summary"]["members_119th"]["chamber_breakdown"] = chamber_breakdown
    
    if "committees_119th" in tables:
        cursor.execute("SELECT chamber, COUNT(*) FROM committees_119th GROUP BY chamber")
        committee_chamber_breakdown = dict(cursor.fetchall())
        assessment["data_summary"]["committees_119th"]["chamber_breakdown"] = committee_chamber_breakdown
        
        # Check for current leadership
        cursor.execute("SELECT name, chair_name, ranking_member_name FROM committees_119th WHERE chair_name IS NOT NULL LIMIT 5")
        leadership_sample = cursor.fetchall()
        assessment["data_summary"]["committees_119th"]["leadership_sample"] = leadership_sample
    
    # Congressional session analysis
    if "congressional_sessions" in tables:
        cursor.execute("SELECT * FROM congressional_sessions")
        sessions = cursor.fetchall()
        assessment["data_summary"]["congressional_sessions"] = {"sessions": sessions}
    
    conn.close()
    
    # Schema compatibility analysis
    assessment["schema_compatibility"] = analyze_schema_compatibility()
    
    # Generate recommendations
    assessment["recommendations"] = generate_integration_recommendations(assessment)
    
    return assessment

def analyze_schema_compatibility():
    """Compare 119th Congress schema with current API schema."""
    
    compatibility = {
        "members": {
            "119th_fields": ["id", "congress_session", "bioguide_id", "name", "party", "state", "chamber", "district", "term_start", "term_end", "is_current"],
            "api_fields": ["id", "bioguide_id", "congress_gov_id", "first_name", "last_name", "middle_name", "suffix", "nickname", "party", "chamber", "state", "district", "term_start", "term_end", "is_current"],
            "missing_in_119th": ["congress_gov_id", "first_name", "last_name", "middle_name", "suffix", "nickname", "phone", "email", "website", "birth_date", "birth_state", "birth_city", "official_photo_url"],
            "extra_in_119th": ["congress_session"],
            "name_differences": {
                "119th_name_field": "Single 'name' field",
                "api_name_fields": "Separate first_name, last_name, middle_name, suffix, nickname fields"
            }
        },
        "committees": {
            "119th_fields": ["id", "congress_session", "name", "chamber", "committee_type", "chair_name", "chair_party", "chair_state", "ranking_member_name", "ranking_member_party", "ranking_member_state"],
            "api_fields": ["id", "congress_gov_id", "committee_code", "name", "chamber", "committee_type", "parent_committee_id", "is_subcommittee", "description", "jurisdiction", "chair_member_id", "ranking_member_id"],
            "missing_in_119th": ["congress_gov_id", "committee_code", "parent_committee_id", "is_subcommittee", "description", "jurisdiction", "chair_member_id", "ranking_member_id"],
            "extra_in_119th": ["congress_session", "chair_name", "chair_party", "chair_state", "ranking_member_name", "ranking_member_party", "ranking_member_state"],
            "leadership_differences": {
                "119th_leadership": "Text fields with names, parties, states",
                "api_leadership": "Foreign key references to member IDs"
            }
        }
    }
    
    return compatibility

def generate_integration_recommendations(assessment):
    """Generate recommendations for integrating 119th Congress data."""
    
    recommendations = []
    
    # Data migration recommendations
    recommendations.append({
        "category": "Data Migration",
        "priority": "HIGH",
        "title": "Create Migration Script",
        "description": "Create a migration script to transform 119th Congress data to API schema format",
        "actions": [
            "Parse 'name' field in members_119th into first_name, last_name components",
            "Map chair_name/ranking_member_name to member IDs in committees",
            "Add missing fields with default values or derive from existing data",
            "Handle congress_session field for tracking Congressional sessions"
        ]
    })
    
    # Schema enhancement recommendations
    recommendations.append({
        "category": "Schema Enhancement",
        "priority": "MEDIUM",
        "title": "Add Congressional Session Support",
        "description": "Enhance API models to support Congressional session tracking",
        "actions": [
            "Add congress_session field to Member and Committee models",
            "Create CongressionalSession model for session metadata",
            "Add session-aware filtering to API endpoints",
            "Implement session transition handling"
        ]
    })
    
    # API endpoint recommendations
    recommendations.append({
        "category": "API Enhancement",
        "priority": "MEDIUM",
        "title": "Congressional Session Endpoints",
        "description": "Add new endpoints for Congressional session information",
        "actions": [
            "Add /congress/session endpoint for current session info",
            "Add /congress/history endpoint for session tracking",
            "Add session filters to existing member/committee endpoints",
            "Add 119th Congress context to all responses"
        ]
    })
    
    # Data quality recommendations
    recommendations.append({
        "category": "Data Quality",
        "priority": "HIGH",
        "title": "Validate 119th Congress Data",
        "description": "Ensure data quality and completeness before integration",
        "actions": [
            "Verify all committee chairs are Republicans (119th Congress)",
            "Verify all ranking members are Democrats",
            "Check member counts match expected Congressional size",
            "Validate party affiliations and state representations"
        ]
    })
    
    return recommendations

def main():
    """Run the API integration assessment."""
    
    print("🔍 Phase 1.1: API Integration Assessment")
    print("=" * 50)
    
    # Run assessment
    assessment = assess_119th_congress_database()
    
    # Save assessment results
    output_file = f"phase1_assessment_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump(assessment, f, indent=2)
    
    # Display summary
    print(f"\n📊 Database Assessment Summary:")
    print(f"   Database: {assessment['database_path']}")
    print(f"   Tables found: {len(assessment['tables']['found'])}")
    
    for table in assessment["tables"]["found"]:
        if table in assessment["data_summary"] and "row_count" in assessment["data_summary"][table]:
            count = assessment["data_summary"][table]["row_count"]
            print(f"   - {table}: {count} rows")
    
    print(f"\n🎯 Key Findings:")
    
    # Members analysis
    if "members_119th" in assessment["data_summary"]:
        members_data = assessment["data_summary"]["members_119th"]
        print(f"   Members (119th Congress): {members_data['row_count']} total")
        if "party_breakdown" in members_data:
            for party, count in members_data["party_breakdown"].items():
                print(f"   - {party}: {count}")
        if "chamber_breakdown" in members_data:
            for chamber, count in members_data["chamber_breakdown"].items():
                print(f"   - {chamber}: {count}")
    
    # Committees analysis
    if "committees_119th" in assessment["data_summary"]:
        committees_data = assessment["data_summary"]["committees_119th"]
        print(f"   Committees (119th Congress): {committees_data['row_count']} total")
        if "chamber_breakdown" in committees_data:
            for chamber, count in committees_data["chamber_breakdown"].items():
                print(f"   - {chamber}: {count}")
        
        # Show leadership sample
        if "leadership_sample" in committees_data:
            print(f"   Committee Leadership Sample:")
            for name, chair, ranking in committees_data["leadership_sample"]:
                print(f"   - {name}: Chair {chair}, Ranking {ranking}")
    
    print(f"\n⚠️  Schema Compatibility Issues:")
    compatibility = assessment["schema_compatibility"]
    
    # Members compatibility
    members_compat = compatibility["members"]
    print(f"   Members table:")
    print(f"   - Missing in 119th: {len(members_compat['missing_in_119th'])} fields")
    print(f"   - Extra in 119th: {len(members_compat['extra_in_119th'])} fields")
    print(f"   - Name field structure different")
    
    # Committees compatibility
    committees_compat = compatibility["committees"]
    print(f"   Committees table:")
    print(f"   - Missing in 119th: {len(committees_compat['missing_in_119th'])} fields")
    print(f"   - Extra in 119th: {len(committees_compat['extra_in_119th'])} fields")
    print(f"   - Leadership structure different (names vs member IDs)")
    
    print(f"\n🎯 Recommendations:")
    for i, rec in enumerate(assessment["recommendations"], 1):
        print(f"   {i}. {rec['title']} ({rec['priority']} priority)")
        print(f"      {rec['description']}")
    
    print(f"\n📄 Full assessment saved to: {output_file}")
    print(f"\n✅ Phase 1.1 Assessment Complete")
    
    return assessment

if __name__ == "__main__":
    main()