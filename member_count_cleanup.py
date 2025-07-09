#!/usr/bin/env python3
"""
Member Count Cleanup - Remove duplicates and achieve constitutional targets

Target: 441 House + 101 Senate = 542 total members
Current: 570 members (22 duplicates + 6 other excess)
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Tuple
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

class MemberCountCleanup:
    """Clean up member counts to achieve constitutional targets"""
    
    def __init__(self):
        self.db_url = os.getenv('DATABASE_URL')
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'operation': 'Member Count Cleanup',
            'target': {'house': 441, 'senate': 101, 'total': 542}
        }
        self.dry_run = True  # Safety first
    
    def execute_cleanup(self, dry_run: bool = True) -> Dict:
        """Execute member count cleanup"""
        self.dry_run = dry_run
        
        print("=" * 60)
        print(f"MEMBER COUNT CLEANUP {'(DRY RUN)' if dry_run else '(LIVE RUN)'}")
        print("=" * 60)
        
        # Step 1: Analyze current state
        self._analyze_current_state()
        
        # Step 2: Remove duplicate records
        self._remove_duplicates()
        
        # Step 3: Analyze remaining excess
        self._analyze_remaining_excess()
        
        # Step 4: Verify final counts
        self._verify_final_counts()
        
        return self.results
    
    def _analyze_current_state(self):
        """Analyze current member counts"""
        print("\n📊 Step 1: Current State Analysis")
        
        try:
            with psycopg2.connect(self.db_url) as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    
                    # Current counts
                    cur.execute("""
                        SELECT chamber, COUNT(*) as count
                        FROM members 
                        WHERE is_current = true
                        GROUP BY chamber
                    """)
                    current_counts = dict(cur.fetchall())
                    
                    self.results['before_cleanup'] = current_counts
                    
                    print(f"Current counts:")
                    print(f"  House: {current_counts.get('House', 0)}/441")
                    print(f"  Senate: {current_counts.get('Senate', 0)}/101")
                    print(f"  Total: {sum(current_counts.values())}/542")
                    
        except Exception as e:
            print(f"❌ Current state analysis failed: {e}")
    
    def _remove_duplicates(self):
        """Remove duplicate member records, keeping the ones with real bioguide_ids"""
        print("\n🔧 Step 2: Remove Duplicate Records")
        
        try:
            with psycopg2.connect(self.db_url) as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    
                    # Find duplicates
                    cur.execute("""
                        SELECT 
                            first_name, last_name, state, chamber,
                            COUNT(*) as count,
                            ARRAY_AGG(id ORDER BY 
                                CASE WHEN bioguide_id LIKE 'TMP%' THEN 1 ELSE 0 END,
                                id
                            ) as db_ids,
                            ARRAY_AGG(bioguide_id ORDER BY 
                                CASE WHEN bioguide_id LIKE 'TMP%' THEN 1 ELSE 0 END,
                                id
                            ) as bioguide_ids
                        FROM members 
                        WHERE is_current = true
                        GROUP BY first_name, last_name, state, chamber
                        HAVING COUNT(*) > 1
                        ORDER BY last_name
                    """)
                    duplicates = cur.fetchall()
                    
                    removed_ids = []
                    for dup in duplicates:
                        # Keep the first (real bioguide_id), remove the rest (TMP ones)
                        ids_to_remove = dup['db_ids'][1:]  # All except first
                        bioguides_to_remove = dup['bioguide_ids'][1:]
                        
                        print(f"  {dup['first_name']} {dup['last_name']} ({dup['state']}-{dup['chamber']}):")
                        print(f"    Keeping: ID {dup['db_ids'][0]} ({dup['bioguide_ids'][0]})")
                        print(f"    Removing: {list(zip(ids_to_remove, bioguides_to_remove))}")
                        
                        removed_ids.extend(ids_to_remove)
                    
                    # Execute removal
                    if removed_ids:
                        if self.dry_run:
                            print(f"\n🔍 DRY RUN: Would remove {len(removed_ids)} duplicate records")
                        else:
                            # Create backup before deletion
                            backup_table = f"members_backup_cleanup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                            cur.execute(f"CREATE TABLE {backup_table} AS SELECT * FROM members")
                            
                            # Remove duplicates
                            cur.execute(
                                "DELETE FROM members WHERE id = ANY(%s)",
                                (removed_ids,)
                            )
                            conn.commit()
                            
                            print(f"✅ Removed {len(removed_ids)} duplicate records")
                            print(f"   Backup created: {backup_table}")
                    
                    self.results['duplicates_removed'] = len(removed_ids)
                    
        except Exception as e:
            print(f"❌ Duplicate removal failed: {e}")
            self.results['duplicates_removed'] = 0
    
    def _analyze_remaining_excess(self):
        """Analyze remaining excess members after duplicate removal"""
        print("\n🔍 Step 3: Analyze Remaining Excess")
        
        try:
            with psycopg2.connect(self.db_url) as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    
                    # Post-duplicate removal counts
                    cur.execute("""
                        SELECT chamber, COUNT(*) as count
                        FROM members 
                        WHERE is_current = true
                        GROUP BY chamber
                    """)
                    post_duplicate_counts = dict(cur.fetchall())
                    
                    house_count = post_duplicate_counts.get('House', 0)
                    senate_count = post_duplicate_counts.get('Senate', 0)
                    
                    house_excess = house_count - 441
                    senate_excess = senate_count - 101
                    
                    print(f"After duplicate removal:")
                    print(f"  House: {house_count}/441 ({house_excess:+d})")
                    print(f"  Senate: {senate_count}/101 ({senate_excess:+d})")
                    
                    # If still excess in Senate, find candidates for removal
                    if senate_excess > 0:
                        print(f"\n🔍 Senate excess investigation ({senate_excess} over):")
                        
                        # Look for potential non-current senators
                        cur.execute("""
                            SELECT 
                                first_name, last_name, state, bioguide_id, id,
                                created_at, congress_session
                            FROM members 
                            WHERE chamber = 'Senate' AND is_current = true
                            ORDER BY 
                                CASE WHEN congress_session != 119 THEN 0 ELSE 1 END,
                                created_at DESC
                            LIMIT %s
                        """, (senate_excess * 2,))  # Get more for investigation
                        
                        potential_removals = cur.fetchall()
                        print(f"   Potential candidates for removal:")
                        for member in potential_removals[:senate_excess]:
                            print(f"     {member['first_name']} {member['last_name']} ({member['state']}) - {member['bioguide_id']}")
                    
                    # Similar for House if under target
                    if house_excess < 0:
                        print(f"\n🔍 House shortage investigation ({abs(house_excess)} under):")
                        print("   Need to investigate missing House members")
                    
                    self.results['post_duplicate_counts'] = post_duplicate_counts
                    
        except Exception as e:
            print(f"❌ Remaining excess analysis failed: {e}")
    
    def _verify_final_counts(self):
        """Verify final member counts"""
        print("\n✅ Step 4: Final Count Verification")
        
        try:
            with psycopg2.connect(self.db_url) as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    
                    # Final counts
                    cur.execute("""
                        SELECT 
                            chamber, 
                            COUNT(*) as count,
                            COUNT(DISTINCT state) as states_represented
                        FROM members 
                        WHERE is_current = true
                        GROUP BY chamber
                    """)
                    final_counts = cur.fetchall()
                    
                    print("Final verification:")
                    total_members = 0
                    for row in final_counts:
                        chamber = row['chamber']
                        count = row['count']
                        target = 441 if chamber == 'House' else 101
                        status = "✅" if count == target else "❌"
                        total_members += count
                        
                        print(f"  {chamber}: {count}/{target} {status} ({row['states_represented']} states)")
                    
                    total_status = "✅" if total_members == 542 else "❌"
                    print(f"  TOTAL: {total_members}/542 {total_status}")
                    
                    self.results['final_counts'] = {row['chamber']: row['count'] for row in final_counts}
                    self.results['success'] = total_members == 542
                    
        except Exception as e:
            print(f"❌ Final verification failed: {e}")

def main():
    """Execute member count cleanup"""
    cleanup = MemberCountCleanup()
    
    # First run as dry run to see what would happen
    print("🔍 RUNNING DRY RUN ANALYSIS...")
    dry_results = cleanup.execute_cleanup(dry_run=True)
    
    # Ask for confirmation if this is an interactive session
    print("\n" + "="*60)
    print("DRY RUN COMPLETE")
    print("="*60)
    
    duplicates_to_remove = dry_results.get('duplicates_removed', 0)
    print(f"Would remove {duplicates_to_remove} duplicate records")
    
    # Show what the final state would be
    before = dry_results.get('before_cleanup', {})
    house_before = before.get('House', 0)
    senate_before = before.get('Senate', 0)
    
    house_after = house_before - (duplicates_to_remove if house_before > 441 else 0)
    senate_after = senate_before - (duplicates_to_remove if senate_before > 101 else 0)
    
    print(f"Projected after cleanup:")
    print(f"  House: {house_before} → {house_after} (target: 441)")
    print(f"  Senate: {senate_before} → {senate_after} (target: 101)")
    
    # Save dry run results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dry_run_file = f"member_cleanup_dry_run_{timestamp}.json"
    with open(dry_run_file, 'w') as f:
        json.dump(dry_results, f, indent=2, default=str)
    
    print(f"\n📄 Dry run results saved to: {dry_run_file}")
    return dry_results

if __name__ == "__main__":
    main()