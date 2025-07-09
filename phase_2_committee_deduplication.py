#!/usr/bin/env python3
"""
Phase 2: Committee Deduplication & Consolidation
=================================================

Systematically remove duplicate committees while preserving member assignments
and maintaining data integrity.
"""

import psycopg2
import json
from datetime import datetime
from collections import defaultdict
import pandas as pd

class CommitteeDeduplicationProcessor:
    def __init__(self):
        self.db_config = {
            'host': 'localhost',
            'port': 5433,
            'database': 'congress_data',
            'user': 'postgres',
            'password': 'mDf3S9ZnBpQqJvGsY1'
        }
        self.conn = None
        self.deduplication_results = {}
        
    def connect(self):
        """Establish database connection"""
        try:
            self.conn = psycopg2.connect(**self.db_config)
            print("✅ Connected to Congressional database")
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def backup_current_state(self):
        """Create backup before any modifications"""
        print("\n💾 CREATING BACKUP...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        try:
            cur = self.conn.cursor()
            
            # Backup committees
            cur.execute(f"""
                CREATE TABLE committees_backup_{timestamp} AS 
                SELECT * FROM committees;
            """)
            
            # Backup memberships
            cur.execute(f"""
                CREATE TABLE committee_memberships_backup_{timestamp} AS 
                SELECT * FROM committee_memberships;
            """)
            
            self.conn.commit()
            print(f"   ✅ Backup created: committees_backup_{timestamp}")
            print(f"   ✅ Backup created: committee_memberships_backup_{timestamp}")
            
            return timestamp
            
        except Exception as e:
            print(f"   ❌ Backup failed: {e}")
            return None
    
    def identify_duplicates(self):
        """Identify duplicate committees and select best ones to keep"""
        print("\n🔍 IDENTIFYING DUPLICATES FOR DEDUPLICATION...")
        
        # Get all committees with details
        query = """
        SELECT 
            id,
            name,
            chamber,
            committee_type,
            congress_gov_id,
            parent_committee_id,
            created_at
        FROM committees 
        ORDER BY name, chamber, committee_type, created_at;
        """
        
        cur = self.conn.cursor()
        cur.execute(query)
        committees = cur.fetchall()
        
        # Group by normalized key
        duplicate_groups = defaultdict(list)
        
        for committee in committees:
            id_, name, chamber, comm_type, congress_gov_id, parent_id, created_at = committee
            
            # Normalize name for grouping
            name_normalized = name.lower().strip()
            key = (name_normalized, chamber, comm_type)
            
            duplicate_groups[key].append({
                'id': id_,
                'name': name,
                'chamber': chamber,
                'committee_type': comm_type,
                'congress_gov_id': congress_gov_id,
                'parent_committee_id': parent_id,
                'created_at': created_at
            })
        
        # Identify duplicates and select keepers
        deduplication_plan = []
        committees_to_remove = []
        committees_to_keep = []
        
        for key, group in duplicate_groups.items():
            if len(group) > 1:
                # Select best committee to keep (prioritize: congress_gov_id > newer > first)
                best_committee = None
                for committee in group:
                    if committee['congress_gov_id']:
                        best_committee = committee
                        break
                
                if not best_committee:
                    # If no congress_gov_id, take the newest
                    best_committee = max(group, key=lambda x: x['created_at'])
                
                # Plan the deduplication
                others = [c for c in group if c['id'] != best_committee['id']]
                
                deduplication_plan.append({
                    'key': key,
                    'keep': best_committee,
                    'remove': others,
                    'count': len(group)
                })
                
                committees_to_keep.append(best_committee['id'])
                committees_to_remove.extend([c['id'] for c in others])
        
        print(f"   📊 Duplicate groups found: {len(deduplication_plan)}")
        print(f"   📊 Committees to remove: {len(committees_to_remove)}")
        print(f"   📊 Committees to keep: {len(committees_to_keep)}")
        
        self.deduplication_results['plan'] = deduplication_plan
        self.deduplication_results['remove_ids'] = committees_to_remove
        self.deduplication_results['keep_ids'] = committees_to_keep
        
        return deduplication_plan
    
    def migrate_member_assignments(self):
        """Migrate member assignments from duplicate committees to kept committees"""
        print("\n🔄 MIGRATING MEMBER ASSIGNMENTS...")
        
        plan = self.deduplication_results['plan']
        migration_count = 0
        
        cur = self.conn.cursor()
        
        for group in plan:
            keep_id = group['keep']['id']
            remove_committees = group['remove']
            
            for remove_committee in remove_committees:
                remove_id = remove_committee['id']
                
                # Get memberships to migrate
                cur.execute("""
                    SELECT member_id, position, start_date, end_date, is_current
                    FROM committee_memberships 
                    WHERE committee_id = %s
                """, (remove_id,))
                
                memberships = cur.fetchall()
                
                for membership in memberships:
                    member_id, position, start_date, end_date, is_current = membership
                    
                    # Check if member already assigned to keeper committee
                    cur.execute("""
                        SELECT id FROM committee_memberships 
                        WHERE committee_id = %s AND member_id = %s
                    """, (keep_id, member_id))
                    
                    existing = cur.fetchone()
                    
                    if not existing:
                        # Migrate assignment
                        cur.execute("""
                            INSERT INTO committee_memberships 
                            (committee_id, member_id, position, start_date, end_date, is_current)
                            VALUES (%s, %s, %s, %s, %s, %s)
                        """, (keep_id, member_id, position, start_date, end_date, is_current))
                        migration_count += 1
                    else:
                        # Update position if the migrated one is more senior
                        if position in ['Chair', 'Ranking Member']:
                            cur.execute("""
                                UPDATE committee_memberships 
                                SET position = %s 
                                WHERE id = %s
                            """, (position, existing[0]))
                
                # Remove old memberships
                cur.execute("""
                    DELETE FROM committee_memberships 
                    WHERE committee_id = %s
                """, (remove_id,))
        
        self.conn.commit()
        print(f"   ✅ Migrated {migration_count} member assignments")
        
        return migration_count
    
    def remove_duplicate_committees(self):
        """Remove duplicate committees after migration"""
        print("\n🗑️ REMOVING DUPLICATE COMMITTEES...")
        
        remove_ids = self.deduplication_results['remove_ids']
        
        if not remove_ids:
            print("   ℹ️ No committees to remove")
            return 0
        
        cur = self.conn.cursor()
        
        # Remove committees
        cur.execute("""
            DELETE FROM committees 
            WHERE id = ANY(%s)
        """, (remove_ids,))
        
        removed_count = cur.rowcount
        self.conn.commit()
        
        print(f"   ✅ Removed {removed_count} duplicate committees")
        
        return removed_count
    
    def identify_empty_committees(self):
        """Identify committees with no member assignments"""
        print("\n📋 IDENTIFYING EMPTY COMMITTEES...")
        
        cur = self.conn.cursor()
        
        # Find committees with no members
        cur.execute("""
            SELECT c.id, c.name, c.chamber, c.committee_type
            FROM committees c
            LEFT JOIN committee_memberships cm ON c.id = cm.committee_id
            WHERE cm.committee_id IS NULL
            ORDER BY c.chamber, c.name
        """)
        
        empty_committees = cur.fetchall()
        
        print(f"   📊 Empty committees found: {len(empty_committees)}")
        
        # Analyze by type
        by_type = defaultdict(int)
        for committee in empty_committees:
            _, _, chamber, comm_type = committee
            by_type[f"{chamber} {comm_type}"] += 1
        
        for key, count in by_type.items():
            print(f"      {key}: {count}")
        
        self.deduplication_results['empty_committees'] = empty_committees
        
        return empty_committees
    
    def remove_empty_committees(self):
        """Remove committees with no member assignments"""
        print("\n🗑️ REMOVING EMPTY COMMITTEES...")
        
        empty_committees = self.deduplication_results.get('empty_committees', [])
        
        if not empty_committees:
            print("   ℹ️ No empty committees to remove")
            return 0
        
        empty_ids = [c[0] for c in empty_committees]
        
        cur = self.conn.cursor()
        
        # Remove empty committees
        cur.execute("""
            DELETE FROM committees 
            WHERE id = ANY(%s)
        """, (empty_ids,))
        
        removed_count = cur.rowcount
        self.conn.commit()
        
        print(f"   ✅ Removed {removed_count} empty committees")
        
        return removed_count
    
    def validate_deduplication(self):
        """Validate deduplication results"""
        print("\n✅ VALIDATING DEDUPLICATION RESULTS...")
        
        cur = self.conn.cursor()
        
        # Count remaining committees
        cur.execute("SELECT COUNT(*) FROM committees")
        total_committees = cur.fetchone()[0]
        
        # Count committees with members
        cur.execute("""
            SELECT COUNT(DISTINCT c.id) 
            FROM committees c
            JOIN committee_memberships cm ON c.id = cm.committee_id
        """)
        committees_with_members = cur.fetchone()[0]
        
        # Count empty committees
        empty_committees = total_committees - committees_with_members
        
        # Check for remaining duplicates
        cur.execute("""
            SELECT LOWER(TRIM(name)), chamber, committee_type, COUNT(*)
            FROM committees
            GROUP BY LOWER(TRIM(name)), chamber, committee_type
            HAVING COUNT(*) > 1
        """)
        remaining_duplicates = cur.fetchall()
        
        validation_results = {
            'total_committees': total_committees,
            'committees_with_members': committees_with_members,
            'empty_committees': empty_committees,
            'remaining_duplicates': len(remaining_duplicates)
        }
        
        print(f"   📊 Total committees: {total_committees}")
        print(f"   📊 Committees with members: {committees_with_members}")
        print(f"   📊 Empty committees: {empty_committees}")
        print(f"   📊 Remaining duplicates: {len(remaining_duplicates)}")
        
        self.deduplication_results['validation'] = validation_results
        
        return validation_results
    
    def generate_report(self):
        """Generate comprehensive deduplication report"""
        print("\n📋 GENERATING DEDUPLICATION REPORT...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        report = {
            'timestamp': timestamp,
            'deduplication_results': self.deduplication_results
        }
        
        report_file = f"committee_deduplication_report_{timestamp}.json"
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"   ✅ Report saved: {report_file}")
        
        return report
    
    def run_deduplication(self):
        """Execute complete deduplication process"""
        print("🔄 COMMITTEE DEDUPLICATION & CONSOLIDATION")
        print("=" * 50)
        
        if not self.connect():
            return False
        
        try:
            # Phase 1: Backup
            backup_timestamp = self.backup_current_state()
            if not backup_timestamp:
                return False
            
            # Phase 2: Identify duplicates
            self.identify_duplicates()
            
            # Phase 3: Migrate member assignments
            self.migrate_member_assignments()
            
            # Phase 4: Remove duplicate committees
            self.remove_duplicate_committees()
            
            # Phase 5: Identify and remove empty committees
            self.identify_empty_committees()
            self.remove_empty_committees()
            
            # Phase 6: Validate results
            self.validate_deduplication()
            
            # Phase 7: Generate report
            report = self.generate_report()
            
            print("\n✅ DEDUPLICATION COMPLETE")
            print("Committee structure has been cleaned and consolidated.")
            
            return report
            
        except Exception as e:
            print(f"❌ Deduplication failed: {e}")
            self.conn.rollback()
            return False
        finally:
            if self.conn:
                self.conn.close()

def main():
    """Execute Phase 2 Committee Deduplication"""
    processor = CommitteeDeduplicationProcessor()
    return processor.run_deduplication()

if __name__ == "__main__":
    main()