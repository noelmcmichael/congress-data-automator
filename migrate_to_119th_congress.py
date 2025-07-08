#!/usr/bin/env python3
"""
119th Congress Database Migration Script
Migrates database from 118th to 119th Congress data with proper session tracking.
"""

import json
import sqlite3
import os
from datetime import datetime, date
from typing import Dict, List, Optional
from congressional_session_tracker import CongressionalSessionTracker

class Congress119Migration:
    """Database migration to 119th Congress"""
    
    def __init__(self, db_path: str = "congress_119th.db"):
        self.db_path = db_path
        self.session_tracker = CongressionalSessionTracker()
        self.migration_log = []
        
    def create_119th_schema(self):
        """Create enhanced database schema with Congressional session tracking"""
        print("🏗️ Creating 119th Congress database schema...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Congressional sessions metadata table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS congressional_sessions (
                session_id INTEGER PRIMARY KEY,
                congress_number INTEGER UNIQUE NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                is_current BOOLEAN NOT NULL DEFAULT FALSE,
                party_control_house TEXT,
                party_control_senate TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Enhanced committees table with session tracking
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS committees_119th (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                congress_session INTEGER NOT NULL,
                name TEXT NOT NULL,
                chamber TEXT NOT NULL CHECK (chamber IN ('House', 'Senate', 'Joint')),
                committee_type TEXT DEFAULT 'Standing',
                chair_name TEXT,
                chair_party TEXT,
                chair_state TEXT,
                ranking_member_name TEXT,
                ranking_member_party TEXT,
                ranking_member_state TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (congress_session) REFERENCES congressional_sessions(congress_number),
                UNIQUE(congress_session, name, chamber)
            )
        """)
        
        # Enhanced members table with session tracking
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS members_119th (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                congress_session INTEGER NOT NULL,
                bioguide_id TEXT,
                name TEXT NOT NULL,
                party TEXT NOT NULL,
                state TEXT NOT NULL,
                chamber TEXT NOT NULL CHECK (chamber IN ('House', 'Senate')),
                district TEXT,
                term_start TEXT,
                term_end TEXT,
                is_current BOOLEAN DEFAULT TRUE,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (congress_session) REFERENCES congressional_sessions(congress_number),
                UNIQUE(congress_session, name, state, chamber)
            )
        """)
        
        # Enhanced committee memberships with session tracking
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS committee_memberships_119th (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                congress_session INTEGER NOT NULL,
                member_id INTEGER NOT NULL,
                committee_id INTEGER NOT NULL,
                position TEXT DEFAULT 'Member',
                subcommittee TEXT,
                is_current BOOLEAN DEFAULT TRUE,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (congress_session) REFERENCES congressional_sessions(congress_number),
                FOREIGN KEY (member_id) REFERENCES members_119th(id),
                FOREIGN KEY (committee_id) REFERENCES committees_119th(id),
                UNIQUE(congress_session, member_id, committee_id)
            )
        """)
        
        # Data migration log
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS migration_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                migration_type TEXT NOT NULL,
                from_congress INTEGER,
                to_congress INTEGER,
                records_migrated INTEGER,
                migration_timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                notes TEXT
            )
        """)
        
        conn.commit()
        conn.close()
        
        print("✅ 119th Congress schema created successfully")
        
    def insert_congressional_sessions(self):
        """Insert Congressional session metadata"""
        print("📅 Inserting Congressional session metadata...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get session information
        sessions = self.session_tracker.get_historical_sessions()
        
        for session in sessions:
            cursor.execute("""
                INSERT OR REPLACE INTO congressional_sessions 
                (congress_number, start_date, end_date, is_current, party_control_house, party_control_senate)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                session.congress_number,
                session.start_date.isoformat(),
                session.end_date.isoformat(),
                session.is_current,
                'Republican' if session.congress_number == 119 else None,  # Known for 119th
                'Republican' if session.congress_number == 119 else None   # Known for 119th
            ))
        
        conn.commit()
        conn.close()
        
        print(f"✅ Inserted {len(sessions)} Congressional sessions")
        
    def load_119th_congress_data(self, data_file: str) -> Dict:
        """Load 119th Congress data from JSON file"""
        print(f"📥 Loading 119th Congress data from {data_file}...")
        
        if not os.path.exists(data_file):
            raise FileNotFoundError(f"Data file not found: {data_file}")
        
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        committees = data.get('committees', {})
        print(f"✅ Loaded {len(committees)} committees from data file")
        
        return data
    
    def migrate_committees(self, congress_data: Dict):
        """Migrate committee data to 119th Congress"""
        print("🏛️ Migrating committee data to 119th Congress...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        committees = congress_data.get('committees', {})
        congress_session = 119
        
        committees_migrated = 0
        
        for committee_key, committee_info in committees.items():
            try:
                # Extract committee information
                committee_name = committee_info.get('name', committee_key.replace('Senate ', '').replace('House ', ''))
                chamber = committee_info.get('chamber', 'Unknown')
                committee_type = committee_info.get('type', 'Standing')
                
                # Chair information
                chair = committee_info.get('chair')
                chair_name = chair.get('name') if chair else None
                chair_party = chair.get('party') if chair else None
                chair_state = chair.get('state') if chair else None
                
                # Ranking member information
                ranking = committee_info.get('ranking_member')
                ranking_name = ranking.get('name') if ranking else None
                ranking_party = ranking.get('party') if ranking else None
                ranking_state = ranking.get('state') if ranking else None
                
                # Insert committee
                cursor.execute("""
                    INSERT OR REPLACE INTO committees_119th 
                    (congress_session, name, chamber, committee_type, chair_name, chair_party, chair_state,
                     ranking_member_name, ranking_member_party, ranking_member_state)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    congress_session, committee_name, chamber, committee_type,
                    chair_name, chair_party, chair_state,
                    ranking_name, ranking_party, ranking_state
                ))
                
                committees_migrated += 1
                
            except Exception as e:
                print(f"  ⚠️ Error migrating committee {committee_key}: {e}")
                continue
        
        conn.commit()
        conn.close()
        
        print(f"✅ Migrated {committees_migrated} committees to 119th Congress")
        self.migration_log.append(f"Committees migrated: {committees_migrated}")
        
        return committees_migrated
    
    def create_sample_members(self):
        """Create sample member data based on committee leadership"""
        print("👥 Creating sample member data from committee leadership...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get all committee chairs and ranking members
        cursor.execute("""
            SELECT chair_name, chair_party, chair_state, 'Chair' as position, chamber
            FROM committees_119th 
            WHERE chair_name IS NOT NULL
            UNION
            SELECT ranking_member_name, ranking_member_party, ranking_member_state, 'Ranking Member' as position, chamber
            FROM committees_119th 
            WHERE ranking_member_name IS NOT NULL
        """)
        
        leadership_members = cursor.fetchall()
        congress_session = 119
        members_created = 0
        
        for member_data in leadership_members:
            name, party, state, position, chamber = member_data
            
            try:
                # Determine chamber from committee
                member_chamber = 'Senate' if chamber == 'Senate' else 'House'
                
                # Insert member
                cursor.execute("""
                    INSERT OR IGNORE INTO members_119th 
                    (congress_session, name, party, state, chamber, term_start, term_end, is_current)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    congress_session, name, party, state, member_chamber,
                    '2025-01-03', '2027-01-03', True
                ))
                
                if cursor.rowcount > 0:
                    members_created += 1
                
            except Exception as e:
                print(f"  ⚠️ Error creating member {name}: {e}")
                continue
        
        conn.commit()
        conn.close()
        
        print(f"✅ Created {members_created} member records from committee leadership")
        self.migration_log.append(f"Members created: {members_created}")
        
        return members_created
    
    def create_committee_memberships(self):
        """Create committee membership relationships for leadership"""
        print("🔗 Creating committee membership relationships...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        congress_session = 119
        memberships_created = 0
        
        # Create chair memberships
        cursor.execute("""
            INSERT OR IGNORE INTO committee_memberships_119th 
            (congress_session, member_id, committee_id, position)
            SELECT ?, m.id, c.id, 'Chair'
            FROM members_119th m
            JOIN committees_119th c ON m.name = c.chair_name AND m.state = c.chair_state
            WHERE m.congress_session = ? AND c.congress_session = ?
        """, (congress_session, congress_session, congress_session))
        
        memberships_created += cursor.rowcount
        
        # Create ranking member memberships
        cursor.execute("""
            INSERT OR IGNORE INTO committee_memberships_119th 
            (congress_session, member_id, committee_id, position)
            SELECT ?, m.id, c.id, 'Ranking Member'
            FROM members_119th m
            JOIN committees_119th c ON m.name = c.ranking_member_name AND m.state = c.ranking_member_state
            WHERE m.congress_session = ? AND c.congress_session = ?
        """, (congress_session, congress_session, congress_session))
        
        memberships_created += cursor.rowcount
        
        conn.commit()
        conn.close()
        
        print(f"✅ Created {memberships_created} committee membership relationships")
        self.migration_log.append(f"Memberships created: {memberships_created}")
        
        return memberships_created
    
    def log_migration(self):
        """Log the migration to database"""
        print("📝 Logging migration details...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO migration_log 
            (migration_type, from_congress, to_congress, records_migrated, notes)
            VALUES (?, ?, ?, ?, ?)
        """, (
            '118th_to_119th_migration',
            118,
            119,
            len(self.migration_log),
            '; '.join(self.migration_log)
        ))
        
        conn.commit()
        conn.close()
        
        print("✅ Migration logged successfully")
    
    def validate_migration(self) -> Dict:
        """Validate the 119th Congress migration"""
        print("🔍 Validating 119th Congress migration...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Count records
        cursor.execute("SELECT COUNT(*) FROM committees_119th WHERE congress_session = 119")
        committee_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM members_119th WHERE congress_session = 119")
        member_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM committee_memberships_119th WHERE congress_session = 119")
        membership_count = cursor.fetchone()[0]
        
        # Check for key committees
        cursor.execute("""
            SELECT name, chair_name, ranking_member_name 
            FROM committees_119th 
            WHERE congress_session = 119 AND name IN ('Judiciary', 'Commerce, Science, and Transportation', 'Finance', 'Armed Services')
        """)
        key_committees = cursor.fetchall()
        
        conn.close()
        
        validation = {
            'migration_timestamp': datetime.now().isoformat(),
            'congress_session': '119th Congress (2025-2027)',
            'record_counts': {
                'committees': committee_count,
                'members': member_count,
                'memberships': membership_count
            },
            'key_committees_verified': len(key_committees),
            'leadership_sample': [
                {'committee': row[0], 'chair': row[1], 'ranking': row[2]} 
                for row in key_committees
            ],
            'migration_success': committee_count > 0 and member_count > 0,
            'data_quality': 'HIGH' if committee_count >= 12 else 'MEDIUM'
        }
        
        print(f"✅ Migration validation complete:")
        print(f"   - Committees: {committee_count}")
        print(f"   - Members: {member_count}")
        print(f"   - Memberships: {membership_count}")
        print(f"   - Key committees verified: {len(key_committees)}")
        
        return validation
    
    def execute_full_migration(self, data_file: str) -> Dict:
        """Execute complete 119th Congress migration"""
        print("🇺🇸 Executing Full 119th Congress Database Migration")
        print("=" * 60)
        
        start_time = datetime.now()
        
        try:
            # Load data
            congress_data = self.load_119th_congress_data(data_file)
            
            # Create schema
            self.create_119th_schema()
            
            # Insert session metadata
            self.insert_congressional_sessions()
            
            # Migrate committees
            committees_migrated = self.migrate_committees(congress_data)
            
            # Create members from leadership
            members_created = self.create_sample_members()
            
            # Create memberships
            memberships_created = self.create_committee_memberships()
            
            # Log migration
            self.log_migration()
            
            # Validate
            validation = self.validate_migration()
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            migration_summary = {
                'migration_status': 'SUCCESS',
                'duration_seconds': duration,
                'committees_migrated': committees_migrated,
                'members_created': members_created,
                'memberships_created': memberships_created,
                'database_file': self.db_path,
                'validation': validation,
                'completion_timestamp': end_time.isoformat()
            }
            
            print(f"\n🎉 Migration completed successfully in {duration:.1f} seconds!")
            print(f"📁 Database: {self.db_path}")
            
            return migration_summary
            
        except Exception as e:
            print(f"❌ Migration failed: {e}")
            return {
                'migration_status': 'FAILED',
                'error': str(e),
                'completion_timestamp': datetime.now().isoformat()
            }

def main():
    """Main migration execution"""
    print("🇺🇸 119th Congress Database Migration")
    print("=" * 50)
    
    # Find the most recent 119th Congress data file
    data_file = None
    for filename in os.listdir('.'):
        if filename.startswith('comprehensive_119th_congress_') and filename.endswith('.json'):
            data_file = filename
            break
    
    if not data_file:
        print("❌ No 119th Congress data file found!")
        print("   Please run improved_119th_scraper.py first")
        return
    
    print(f"📁 Using data file: {data_file}")
    
    # Execute migration
    migrator = Congress119Migration()
    result = migrator.execute_full_migration(data_file)
    
    # Export results
    with open('migration_result_119th.json', 'w') as f:
        json.dump(result, f, indent=2, default=str)
    
    print(f"📋 Migration results saved to: migration_result_119th.json")

if __name__ == "__main__":
    main()