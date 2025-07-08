#!/usr/bin/env python3
"""
Phase 1.2: API Schema Updates
Update API models to support Congressional session tracking and 119th Congress data.
"""

import sqlite3
import os
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
import re

class CongressionalDataMigrator:
    """Handles migration of 119th Congress data to API schema format."""
    
    def __init__(self, source_db: str = "congress_119th.db"):
        self.source_db = source_db
        self.migration_log = []
        
    def log_action(self, action: str, details: str, status: str = "INFO"):
        """Log migration actions."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "details": details,
            "status": status
        }
        self.migration_log.append(entry)
        print(f"[{status}] {action}: {details}")
    
    def parse_full_name(self, full_name: str) -> Dict[str, Optional[str]]:
        """Parse full name into components for API schema."""
        if not full_name:
            return {"first_name": None, "last_name": None, "middle_name": None, "suffix": None, "nickname": None}
        
        # Handle common suffixes
        suffixes = ["Jr.", "Sr.", "II", "III", "IV", "V"]
        suffix = None
        name_parts = full_name.strip().split()
        
        # Check for suffix
        if name_parts and name_parts[-1] in suffixes:
            suffix = name_parts.pop()
        
        # Handle different name patterns
        if len(name_parts) >= 2:
            first_name = name_parts[0]
            last_name = name_parts[-1]
            middle_name = " ".join(name_parts[1:-1]) if len(name_parts) > 2 else None
        elif len(name_parts) == 1:
            first_name = name_parts[0]
            last_name = None
            middle_name = None
        else:
            first_name = full_name
            last_name = None
            middle_name = None
        
        return {
            "first_name": first_name,
            "last_name": last_name,
            "middle_name": middle_name if middle_name else None,
            "suffix": suffix,
            "nickname": None  # Cannot determine from full name
        }
    
    def migrate_members_data(self) -> List[Dict[str, Any]]:
        """Migrate members from 119th Congress format to API format."""
        
        self.log_action("migrate_members_data", "Starting members migration")
        
        conn = sqlite3.connect(self.source_db)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM members_119th")
        columns = [description[0] for description in cursor.description]
        members_119th = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        migrated_members = []
        
        for member in members_119th:
            # Parse name components
            name_parts = self.parse_full_name(member.get("name", ""))
            
            # Generate bioguide_id if missing (use existing logic or create placeholder)
            bioguide_id = member.get("bioguide_id") or f"119TH_{member['id']:04d}"
            
            migrated_member = {
                # IDs - keep original ID, generate bioguide if missing
                "id": member.get("id"),
                "bioguide_id": bioguide_id,
                "congress_gov_id": None,  # Not available in 119th data
                
                # Name components
                "first_name": name_parts["first_name"],
                "last_name": name_parts["last_name"],
                "middle_name": name_parts["middle_name"],
                "suffix": name_parts["suffix"],
                "nickname": name_parts["nickname"],
                
                # Political information
                "party": member.get("party"),
                "chamber": member.get("chamber"),
                "state": member.get("state"),
                "district": member.get("district"),
                
                # Service information
                "term_start": member.get("term_start"),
                "term_end": member.get("term_end"),
                "is_current": member.get("is_current", True),
                
                # Congressional session tracking (NEW)
                "congress_session": member.get("congress_session", 119),
                
                # Contact information (not available in 119th data)
                "phone": None,
                "email": None,
                "website": None,
                
                # Additional information (not available in 119th data)
                "birth_date": None,
                "birth_state": None,
                "birth_city": None,
                "official_photo_url": None,
                
                # Metadata
                "created_at": member.get("created_at"),
                "updated_at": datetime.now().isoformat(),
                "last_scraped_at": None
            }
            
            migrated_members.append(migrated_member)
        
        conn.close()
        
        self.log_action("migrate_members_data", f"Migrated {len(migrated_members)} members")
        return migrated_members
    
    def migrate_committees_data(self) -> List[Dict[str, Any]]:
        """Migrate committees from 119th Congress format to API format."""
        
        self.log_action("migrate_committees_data", "Starting committees migration")
        
        conn = sqlite3.connect(self.source_db)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM committees_119th")
        columns = [description[0] for description in cursor.description]
        committees_119th = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        # Get members for chair/ranking member lookup
        cursor.execute("SELECT * FROM members_119th")
        members_columns = [description[0] for description in cursor.description]
        members_119th = [dict(zip(members_columns, row)) for row in cursor.fetchall()]
        
        # Create name to ID mapping for leadership
        name_to_id = {}
        for member in members_119th:
            name = member.get("name", "").strip()
            if name:
                name_to_id[name] = member.get("id")
        
        migrated_committees = []
        
        for committee in committees_119th:
            # Look up chair and ranking member IDs
            chair_member_id = None
            ranking_member_id = None
            
            chair_name = committee.get("chair_name", "")
            ranking_name = committee.get("ranking_member_name", "")
            
            if chair_name and chair_name in name_to_id:
                chair_member_id = name_to_id[chair_name]
            
            if ranking_name and ranking_name in name_to_id:
                ranking_member_id = name_to_id[ranking_name]
            
            migrated_committee = {
                # IDs
                "id": committee.get("id"),
                "congress_gov_id": None,  # Not available in 119th data
                "committee_code": None,   # Not available in 119th data
                
                # Basic information
                "name": committee.get("name"),
                "chamber": committee.get("chamber"),
                "committee_type": committee.get("committee_type", "Standing"),
                
                # Congressional session tracking (NEW)
                "congress_session": committee.get("congress_session", 119),
                
                # Hierarchy (assume all are main committees for now)
                "parent_committee_id": None,
                "is_subcommittee": False,
                
                # Details (not available in 119th data)
                "description": None,
                "jurisdiction": None,
                
                # Leadership (converted from names to IDs)
                "chair_member_id": chair_member_id,
                "ranking_member_id": ranking_member_id,
                
                # Contact information (not available in 119th data)
                "phone": None,
                "email": None,
                "website": None,
                "office_location": None,
                
                # Official URLs (not available in 119th data)
                "hearings_url": None,
                "members_url": None,
                "official_website_url": None,
                "last_url_update": None,
                
                # Activity status
                "is_active": True,
                
                # Metadata
                "created_at": committee.get("created_at"),
                "updated_at": datetime.now().isoformat(),
                "last_scraped_at": None,
                
                # Legacy 119th fields for reference
                "_119th_chair_name": committee.get("chair_name"),
                "_119th_chair_party": committee.get("chair_party"),
                "_119th_chair_state": committee.get("chair_state"),
                "_119th_ranking_name": committee.get("ranking_member_name"),
                "_119th_ranking_party": committee.get("ranking_member_party"),
                "_119th_ranking_state": committee.get("ranking_member_state")
            }
            
            migrated_committees.append(migrated_committee)
        
        conn.close()
        
        self.log_action("migrate_committees_data", f"Migrated {len(migrated_committees)} committees")
        return migrated_committees
    
    def migrate_memberships_data(self) -> List[Dict[str, Any]]:
        """Migrate committee memberships from 119th Congress format to API format."""
        
        self.log_action("migrate_memberships_data", "Starting memberships migration")
        
        conn = sqlite3.connect(self.source_db)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM committee_memberships_119th")
        columns = [description[0] for description in cursor.description]
        memberships_119th = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        migrated_memberships = []
        
        for membership in memberships_119th:
            migrated_membership = {
                "id": membership.get("id"),
                "member_id": membership.get("member_id"),
                "committee_id": membership.get("committee_id"),
                "position": membership.get("position", "Member"),
                "start_date": membership.get("start_date"),
                "end_date": membership.get("end_date"),
                "is_current": membership.get("is_current", True),
                "created_at": membership.get("created_at"),
                "updated_at": datetime.now().isoformat()
            }
            
            migrated_memberships.append(migrated_membership)
        
        conn.close()
        
        self.log_action("migrate_memberships_data", f"Migrated {len(migrated_memberships)} memberships")
        return migrated_memberships
    
    def migrate_congressional_sessions(self) -> List[Dict[str, Any]]:
        """Migrate congressional sessions data."""
        
        self.log_action("migrate_congressional_sessions", "Starting sessions migration")
        
        conn = sqlite3.connect(self.source_db)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM congressional_sessions")
        columns = [description[0] for description in cursor.description]
        sessions = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        conn.close()
        
        self.log_action("migrate_congressional_sessions", f"Migrated {len(sessions)} sessions")
        return sessions
    
    def create_api_schema_update(self) -> Dict[str, Any]:
        """Create the complete API schema update with 119th Congress data."""
        
        self.log_action("create_api_schema_update", "Starting full migration")
        
        migration_data = {
            "migration_info": {
                "timestamp": datetime.now().isoformat(),
                "source_database": self.source_db,
                "target_schema": "API Schema with Congressional Session Support",
                "congress_session": 119,
                "migration_type": "119th Congress Integration"
            },
            "members": self.migrate_members_data(),
            "committees": self.migrate_committees_data(),
            "committee_memberships": self.migrate_memberships_data(),
            "congressional_sessions": self.migrate_congressional_sessions(),
            "schema_changes": {
                "new_fields": [
                    "congress_session field added to Member model",
                    "congress_session field added to Committee model",
                    "CongressionalSession model added"
                ],
                "field_mappings": {
                    "members": {
                        "name": "first_name + last_name + middle_name + suffix",
                        "chair_name": "chair_member_id (lookup)",
                        "ranking_member_name": "ranking_member_id (lookup)"
                    }
                }
            },
            "validation_summary": {
                "members_migrated": len(self.migrate_members_data()),
                "committees_migrated": len(self.migrate_committees_data()),
                "memberships_migrated": len(self.migrate_memberships_data()),
                "leadership_mapped": 0,  # Will be calculated
                "data_quality_issues": []
            },
            "migration_log": self.migration_log
        }
        
        # Calculate leadership mapping success
        committees = migration_data["committees"]
        mapped_chairs = sum(1 for c in committees if c["chair_member_id"] is not None)
        mapped_ranking = sum(1 for c in committees if c["ranking_member_id"] is not None)
        migration_data["validation_summary"]["leadership_mapped"] = mapped_chairs + mapped_ranking
        
        # Identify data quality issues
        issues = []
        for member in migration_data["members"]:
            if not member["last_name"]:
                issues.append(f"Member {member['id']}: No last name parsed from '{member['first_name']}'")
        
        for committee in migration_data["committees"]:
            if committee["_119th_chair_name"] and not committee["chair_member_id"]:
                issues.append(f"Committee {committee['name']}: Chair '{committee['_119th_chair_name']}' not found in members")
            if committee["_119th_ranking_name"] and not committee["ranking_member_id"]:
                issues.append(f"Committee {committee['name']}: Ranking member '{committee['_119th_ranking_name']}' not found in members")
        
        migration_data["validation_summary"]["data_quality_issues"] = issues
        
        self.log_action("create_api_schema_update", "Migration complete")
        return migration_data

def main():
    """Run the API schema migration."""
    
    print("🔄 Phase 1.2: API Schema Updates")
    print("=" * 50)
    
    # Check if source database exists
    if not os.path.exists("congress_119th.db"):
        print("❌ Error: congress_119th.db not found")
        return
    
    # Initialize migrator
    migrator = CongressionalDataMigrator()
    
    # Run migration
    print("🚀 Starting 119th Congress data migration...")
    migration_data = migrator.create_api_schema_update()
    
    # Save migration results
    output_file = f"phase1_migration_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump(migration_data, f, indent=2)
    
    # Display summary
    print(f"\n📊 Migration Summary:")
    print(f"   Source: {migration_data['migration_info']['source_database']}")
    print(f"   Target: API Schema with Congressional Session Support")
    print(f"   Congress Session: {migration_data['migration_info']['congress_session']}")
    
    validation = migration_data["validation_summary"]
    print(f"\n📈 Data Migrated:")
    print(f"   Members: {validation['members_migrated']}")
    print(f"   Committees: {validation['committees_migrated']}")
    print(f"   Memberships: {validation['memberships_migrated']}")
    print(f"   Leadership positions mapped: {validation['leadership_mapped']}")
    
    # Show sample migrated data
    print(f"\n👥 Sample Members (API Schema):")
    for member in migration_data["members"][:3]:
        name = f"{member['first_name']} {member['last_name']}"
        party_state = f"({member['party']}-{member['state']})"
        print(f"   - {name} {party_state} - {member['chamber']}")
    
    print(f"\n🏛️ Sample Committees (API Schema):")
    for committee in migration_data["committees"][:3]:
        chair_info = ""
        if committee["chair_member_id"]:
            chair_info = f" (Chair ID: {committee['chair_member_id']})"
        print(f"   - {committee['name']} ({committee['chamber']}){chair_info}")
    
    # Show data quality issues
    if validation["data_quality_issues"]:
        print(f"\n⚠️  Data Quality Issues ({len(validation['data_quality_issues'])}):")
        for issue in validation["data_quality_issues"][:5]:
            print(f"   - {issue}")
        if len(validation["data_quality_issues"]) > 5:
            print(f"   ... and {len(validation['data_quality_issues']) - 5} more")
    else:
        print(f"\n✅ No data quality issues found")
    
    print(f"\n📄 Migration data saved to: {output_file}")
    print(f"\n✅ Phase 1.2 Schema Migration Complete")
    
    # Recommendations for next steps
    print(f"\n🎯 Next Steps (Phase 1.3):")
    print(f"   1. Update SQLAlchemy models with congress_session fields")
    print(f"   2. Create CongressionalSession model")
    print(f"   3. Add session-aware API endpoints")
    print(f"   4. Test API compatibility with migrated data")
    print(f"   5. Deploy to production database")
    
    return migration_data

if __name__ == "__main__":
    main()