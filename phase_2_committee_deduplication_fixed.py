#!/usr/bin/env python3
"""
Phase 2: Committee Deduplication & Consolidation (Fixed)
========================================================

Systematically remove duplicate committees while preserving member assignments
and maintaining data integrity. Handles foreign key constraints properly.
"""

import psycopg2
import json
from datetime import datetime
from collections import defaultdict

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
        """Identify duplicate committees and create comprehensive mapping"""
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
        
        # Create mapping for deduplication
        id_mapping = {}  # old_id -> new_id
        committees_to_remove = []
        committees_to_keep = []
        
        for key, group in duplicate_groups.items():
            if len(group) > 1:
                # Select best committee to keep
                best_committee = None
                for committee in group:
                    if committee['congress_gov_id']:
                        best_committee = committee
                        break
                
                if not best_committee:
                    best_committee = max(group, key=lambda x: x['created_at'])
                
                # Create mapping
                keep_id = best_committee['id']
                committees_to_keep.append(keep_id)
                
                for committee in group:
                    if committee['id'] != keep_id:
                        id_mapping[committee['id']] = keep_id
                        committees_to_remove.append(committee['id'])
        
        print(f"   📊 Duplicate groups found: {len([g for g in duplicate_groups.values() if len(g) > 1])}")
        print(f"   📊 Committees to remove: {len(committees_to_remove)}")
        print(f"   📊 ID mappings created: {len(id_mapping)}")
        
        self.deduplication_results['id_mapping'] = id_mapping
        self.deduplication_results['remove_ids'] = committees_to_remove
        self.deduplication_results['keep_ids'] = committees_to_keep
        
        return id_mapping
    
    def update_all_references(self):
        """Update all foreign key references before removing duplicates"""
        print("\n🔗 UPDATING ALL FOREIGN KEY REFERENCES...")
        
        id_mapping = self.deduplication_results['id_mapping']
        
        if not id_mapping:
            print("   ℹ️ No references to update")
            return 0
        
        cur = self.conn.cursor()
        total_updates = 0
        
        for old_id, new_id in id_mapping.items():
            # Update parent committee references
            cur.execute("""
                UPDATE committees 
                SET parent_committee_id = %s 
                WHERE parent_committee_id = %s
            """, (new_id, old_id))
            parent_updates = cur.rowcount
            
            # Update hearing committee references
            cur.execute("""
                UPDATE hearings 
                SET committee_id = %s 
                WHERE committee_id = %s
            """, (new_id, old_id))
            hearing_updates = cur.rowcount
            
            total_updates += parent_updates + hearing_updates
            
            if parent_updates > 0 or hearing_updates > 0:
                print(f"      Committee {old_id} -> {new_id}: {parent_updates} parent refs, {hearing_updates} hearing refs")
        
        self.conn.commit()
        print(f"   ✅ Updated {total_updates} total references")
        
        return total_updates
    
    def migrate_member_assignments(self):
        """Migrate member assignments from duplicate committees to kept committees"""
        print("\n🔄 MIGRATING MEMBER ASSIGNMENTS...")
        
        id_mapping = self.deduplication_results['id_mapping']
        migration_count = 0
        
        cur = self.conn.cursor()
        
        for old_id, new_id in id_mapping.items():
            # Get memberships to migrate
            cur.execute("""
                SELECT member_id, position, start_date, end_date, is_current
                FROM committee_memberships 
                WHERE committee_id = %s
            """, (old_id,))
            
            memberships = cur.fetchall()
            
            for membership in memberships:
                member_id, position, start_date, end_date, is_current = membership
                
                # Check if member already assigned to target committee
                cur.execute("""
                    SELECT id, position FROM committee_memberships 
                    WHERE committee_id = %s AND member_id = %s
                """, (new_id, member_id))
                
                existing = cur.fetchone()
                
                if not existing:
                    # Migrate assignment
                    cur.execute("""
                        INSERT INTO committee_memberships 
                        (committee_id, member_id, position, start_date, end_date, is_current)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (new_id, member_id, position, start_date, end_date, is_current))
                    migration_count += 1
                else:
                    # Update position if the migrated one is more senior
                    existing_id, existing_position = existing
                    if position in ['Chair', 'Ranking Member'] and existing_position not in ['Chair', 'Ranking Member']:
                        cur.execute("""
                            UPDATE committee_memberships 
                            SET position = %s 
                            WHERE id = %s
                        """, (position, existing_id))
                        migration_count += 1
            
            # Remove old memberships
            cur.execute("""
                DELETE FROM committee_memberships 
                WHERE committee_id = %s
            """, (old_id,))
        
        self.conn.commit()
        print(f"   ✅ Migrated {migration_count} member assignments")
        
        return migration_count
    
    def remove_duplicate_committees(self):
        """Remove duplicate committees after updating references"""
        print("\n🗑️ REMOVING DUPLICATE COMMITTEES...")
        
        remove_ids = self.deduplication_results['remove_ids']
        
        if not remove_ids:
            print("   ℹ️ No committees to remove")
            return 0
        
        cur = self.conn.cursor()
        
        # Remove committees (foreign keys should be handled now)
        cur.execute("""
            DELETE FROM committees 
            WHERE id = ANY(%s)
        """, (remove_ids,))
        
        removed_count = cur.rowcount
        self.conn.commit()
        
        print(f"   ✅ Removed {removed_count} duplicate committees")
        
        return removed_count
    
    def identify_and_remove_empty_committees(self):
        """Identify and remove committees with no member assignments (safe removal)"""
        print("\n📋 IDENTIFYING AND REMOVING EMPTY COMMITTEES...")
        
        cur = self.conn.cursor()
        
        # Get committees with no members, no hearings, AND no children
        cur.execute("""
            SELECT c.id, c.name, c.chamber, c.committee_type
            FROM committees c
            LEFT JOIN committee_memberships cm ON c.id = cm.committee_id
            LEFT JOIN hearings h ON c.id = h.committee_id
            LEFT JOIN committees child ON c.id = child.parent_committee_id
            WHERE cm.committee_id IS NULL 
              AND h.committee_id IS NULL
              AND child.parent_committee_id IS NULL
        """)
        
        safe_empty_committees = cur.fetchall()
        
        # Get committees with issues (members, hearings, or children)
        cur.execute("""
            SELECT 
                c.id, c.name, c.chamber, c.committee_type,
                COUNT(DISTINCT cm.id) as member_count,
                COUNT(DISTINCT h.id) as hearing_count,
                COUNT(DISTINCT child.id) as child_count
            FROM committees c
            LEFT JOIN committee_memberships cm ON c.id = cm.committee_id
            LEFT JOIN hearings h ON c.id = h.committee_id
            LEFT JOIN committees child ON c.id = child.parent_committee_id
            GROUP BY c.id, c.name, c.chamber, c.committee_type
            HAVING COUNT(DISTINCT cm.id) > 0 
                OR COUNT(DISTINCT h.id) > 0 
                OR COUNT(DISTINCT child.id) > 0
        """)
        
        committees_with_data = cur.fetchall()
        
        print(f"   📊 Empty committees (safe to remove): {len(safe_empty_committees)}")
        print(f"   📊 Committees with data: {len(committees_with_data)}")
        
        # Remove only completely safe empty committees
        if safe_empty_committees:
            safe_empty_ids = [c[0] for c in safe_empty_committees]
            
            cur.execute("""
                DELETE FROM committees 
                WHERE id = ANY(%s)
            """, (safe_empty_ids,))
            
            removed_count = cur.rowcount
            self.conn.commit()
            
            print(f"   ✅ Removed {removed_count} completely empty committees")
            
            self.deduplication_results['empty_removed'] = removed_count
            self.deduplication_results['committees_with_data'] = len(committees_with_data)
            return removed_count
        else:
            print("   ℹ️ No safe empty committees to remove")
            return 0
    
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
        
        # Count by chamber and type
        cur.execute("""
            SELECT chamber, committee_type, COUNT(*)
            FROM committees
            GROUP BY chamber, committee_type
            ORDER BY chamber, committee_type
        """)
        structure = cur.fetchall()
        
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
            'empty_committees': total_committees - committees_with_members,
            'committee_structure': structure,
            'remaining_duplicates': len(remaining_duplicates),
            'duplicate_details': remaining_duplicates
        }
        
        print(f"   📊 Total committees: {total_committees}")
        print(f"   📊 Committees with members: {committees_with_members}")
        print(f"   📊 Empty committees: {total_committees - committees_with_members}")
        print(f"   📊 Remaining duplicates: {len(remaining_duplicates)}")
        
        print("\n   📊 Committee structure:")
        for chamber, comm_type, count in structure:
            print(f"      {chamber} {comm_type}: {count}")
        
        self.deduplication_results['validation'] = validation_results
        
        return validation_results
    
    def generate_report(self):
        """Generate comprehensive deduplication report"""
        print("\n📋 GENERATING DEDUPLICATION REPORT...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        report = {
            'timestamp': timestamp,
            'operation': 'committee_deduplication',
            'results': self.deduplication_results
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
            
            # Phase 2: Identify duplicates and create mapping
            self.identify_duplicates()
            
            # Phase 3: Update all foreign key references
            self.update_all_references()
            
            # Phase 4: Migrate member assignments
            self.migrate_member_assignments()
            
            # Phase 5: Remove duplicate committees
            self.remove_duplicate_committees()
            
            # Phase 6: Remove empty committees
            self.identify_and_remove_empty_committees()
            
            # Phase 7: Validate results
            self.validate_deduplication()
            
            # Phase 8: Generate report
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