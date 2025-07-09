#!/usr/bin/env python3
"""
Member Count Correction - Fix chamber classifications and duplicates

Corrects the remaining discrepancies to achieve constitutional targets:
- Fix territorial delegates (Senate → House)
- Remove senator name duplicates  
- Add Vice President record
- Target: 441 House + 101 Senate = 542 total
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Tuple
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

class MemberCountCorrection:
    """Correct member counts to achieve constitutional accuracy"""
    
    def __init__(self):
        self.db_url = os.getenv('DATABASE_URL')
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'operation': 'Member Count Correction',
            'target': {'house': 441, 'senate': 101, 'total': 542}
        }
    
    def execute_corrections(self, dry_run: bool = True) -> Dict:
        """Execute member count corrections"""
        print("=" * 60)
        print(f"MEMBER COUNT CORRECTION {'(DRY RUN)' if dry_run else '(LIVE RUN)'}")
        print("=" * 60)
        
        # Step 1: Fix territorial delegate chamber assignments
        self._fix_territorial_delegates(dry_run)
        
        # Step 2: Remove senator name duplicates
        self._remove_senator_duplicates(dry_run)
        
        # Step 3: Add Vice President record  
        self._add_vice_president(dry_run)
        
        # Step 4: Verify final counts
        self._verify_final_counts()
        
        return self.results
    
    def _fix_territorial_delegates(self, dry_run: bool):
        """Fix territorial delegates incorrectly classified as Senate"""
        print("\\n🏛️ Step 1: Fix Territorial Delegate Classifications")
        
        try:
            with psycopg2.connect(self.db_url) as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    
                    # Find territorial delegates in Senate
                    cur.execute('''
                        SELECT id, first_name, last_name, state, bioguide_id
                        FROM members 
                        WHERE chamber = 'Senate' AND is_current = true
                        AND state IN ('AS', 'DC', 'GU', 'MP', 'PR', 'VI')
                        ORDER BY state
                    ''')
                    territorial_senators = cur.fetchall()
                    
                    print(f"Found {len(territorial_senators)} territorial delegates in Senate:")
                    for delegate in territorial_senators:
                        print(f"  {delegate['first_name']} {delegate['last_name']} ({delegate['state']}) - ID {delegate['id']}")
                    
                    if territorial_senators and not dry_run:
                        # Move them to House
                        delegate_ids = [d['id'] for d in territorial_senators]
                        cur.execute('''
                            UPDATE members 
                            SET chamber = 'House', district = '0', updated_at = NOW()
                            WHERE id = ANY(%s)
                        ''', (delegate_ids,))
                        conn.commit()
                        print(f"✅ Moved {len(delegate_ids)} delegates from Senate to House")
                    elif territorial_senators:
                        print(f"🔍 DRY RUN: Would move {len(territorial_senators)} delegates to House")
                    
                    self.results['territorial_delegates_moved'] = len(territorial_senators)
                    
        except Exception as e:
            print(f"❌ Territorial delegate fix failed: {e}")
    
    def _remove_senator_duplicates(self, dry_run: bool):
        """Remove senator name duplicates (e.g., Bernie vs Bernard Sanders)"""
        print("\\n🔧 Step 2: Remove Senator Name Duplicates")
        
        try:
            with psycopg2.connect(self.db_url) as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    
                    # Find potential senator name duplicates by state
                    cur.execute('''
                        WITH similar_senators AS (
                            SELECT 
                                state,
                                ARRAY_AGG(id ORDER BY 
                                    CASE WHEN bioguide_id LIKE 'TMP%' THEN 1 ELSE 0 END,
                                    LENGTH(first_name) DESC,  -- Prefer full names over nicknames
                                    id
                                ) as ids,
                                ARRAY_AGG(first_name || ' ' || last_name ORDER BY 
                                    CASE WHEN bioguide_id LIKE 'TMP%' THEN 1 ELSE 0 END,
                                    LENGTH(first_name) DESC,
                                    id
                                ) as names,
                                ARRAY_AGG(bioguide_id ORDER BY 
                                    CASE WHEN bioguide_id LIKE 'TMP%' THEN 1 ELSE 0 END,
                                    LENGTH(first_name) DESC,
                                    id
                                ) as bioguides,
                                COUNT(*) as count
                            FROM members 
                            WHERE chamber = 'Senate' AND is_current = true
                                AND state NOT IN ('AS', 'DC', 'GU', 'MP', 'PR', 'VI')  -- Exclude territories
                            GROUP BY state, 
                                LOWER(REGEXP_REPLACE(last_name, '[^a-zA-Z]', '', 'g'))  -- Group by normalized last name
                            HAVING COUNT(*) > 2  -- More than 2 senators per state per last name
                        )
                        SELECT * FROM similar_senators
                        ORDER BY state
                    ''')
                    duplicate_states = cur.fetchall()
                    
                    print(f"Found potential duplicates in {len(duplicate_states)} states:")
                    
                    ids_to_deactivate = []
                    for state_group in duplicate_states:
                        state = state_group['state']
                        names = state_group['names']
                        ids = state_group['ids']
                        bioguides = state_group['bioguides']
                        
                        print(f"\\n  {state} ({state_group['count']} records):")
                        for i, (name, bioguide, id_val) in enumerate(zip(names, bioguides, ids)):
                            action = "KEEP" if i < 2 else "REMOVE"
                            print(f"    {action}: {name} ({bioguide}) - ID {id_val}")
                            if i >= 2:  # Keep first 2, remove rest
                                ids_to_deactivate.append(id_val)
                    
                    if ids_to_deactivate and not dry_run:
                        cur.execute('''
                            UPDATE members 
                            SET is_current = false, updated_at = NOW()
                            WHERE id = ANY(%s)
                        ''', (ids_to_deactivate,))
                        conn.commit()
                        print(f"\\n✅ Deactivated {len(ids_to_deactivate)} duplicate senator records")
                    elif ids_to_deactivate:
                        print(f"\\n🔍 DRY RUN: Would deactivate {len(ids_to_deactivate)} duplicate senators")
                    
                    self.results['senator_duplicates_removed'] = len(ids_to_deactivate)
                    
        except Exception as e:
            print(f"❌ Senator duplicate removal failed: {e}")
    
    def _add_vice_president(self, dry_run: bool):
        """Add Vice President as President of the Senate"""
        print("\\n👥 Step 3: Add Vice President Record")
        
        try:
            with psycopg2.connect(self.db_url) as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    
                    # Check if VP already exists
                    cur.execute('''
                        SELECT id, first_name, last_name, bioguide_id
                        FROM members 
                        WHERE is_current = true
                        AND (LOWER(first_name || ' ' || last_name) LIKE '%kamala%harris%'
                             OR bioguide_id = 'H001075'
                             OR (chamber = 'Senate' AND LOWER(first_name) = 'kamala'))
                    ''')
                    existing_vp = cur.fetchone()
                    
                    if existing_vp:
                        print(f"✅ Vice President already exists: {existing_vp['first_name']} {existing_vp['last_name']} (ID {existing_vp['id']})")
                        self.results['vp_added'] = False
                    else:
                        if not dry_run:
                            # Add Kamala Harris as VP/President of Senate
                            cur.execute('''
                                INSERT INTO members (
                                    bioguide_id, first_name, last_name, chamber, 
                                    state, party, district, is_current, 
                                    congress_session, created_at, updated_at
                                ) VALUES (
                                    'H001075', 'Kamala', 'Harris', 'Senate',
                                    'CA', 'Democratic', NULL, true,
                                    119, NOW(), NOW()
                                )
                            ''')
                            conn.commit()
                            print("✅ Added Vice President Kamala Harris as President of the Senate")
                        else:
                            print("🔍 DRY RUN: Would add VP Kamala Harris as President of Senate")
                        
                        self.results['vp_added'] = True
                    
        except Exception as e:
            print(f"❌ VP addition failed: {e}")
    
    def _verify_final_counts(self):
        """Verify final member counts"""
        print("\\n✅ Step 4: Final Count Verification")
        
        try:
            with psycopg2.connect(self.db_url) as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    
                    # Final counts
                    cur.execute('''
                        SELECT 
                            chamber, 
                            COUNT(*) as count,
                            COUNT(DISTINCT state) as states_represented
                        FROM members 
                        WHERE is_current = true
                        GROUP BY chamber
                        ORDER BY chamber
                    ''')
                    final_counts = cur.fetchall()
                    
                    # Detailed breakdown
                    cur.execute('''
                        SELECT 
                            'House Voting' as category,
                            COUNT(*) as count
                        FROM members 
                        WHERE is_current = true AND chamber = 'House'
                            AND state NOT IN ('AS', 'DC', 'GU', 'MP', 'PR', 'VI')
                        
                        UNION ALL
                        
                        SELECT 
                            'House Non-Voting' as category,
                            COUNT(*) as count
                        FROM members 
                        WHERE is_current = true AND chamber = 'House'
                            AND state IN ('AS', 'DC', 'GU', 'MP', 'PR', 'VI')
                        
                        UNION ALL
                        
                        SELECT 
                            'Senate Regular' as category,
                            COUNT(*) as count
                        FROM members 
                        WHERE is_current = true AND chamber = 'Senate'
                            AND NOT (first_name = 'Kamala' AND last_name = 'Harris')
                        
                        UNION ALL
                        
                        SELECT 
                            'Senate VP' as category,
                            COUNT(*) as count
                        FROM members 
                        WHERE is_current = true AND chamber = 'Senate'
                            AND first_name = 'Kamala' AND last_name = 'Harris'
                    ''')
                    breakdown = cur.fetchall()
                    
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
                    
                    print("\\nDetailed breakdown:")
                    for row in breakdown:
                        print(f"  {row['category']}: {row['count']}")
                    
                    self.results['final_counts'] = {row['chamber']: row['count'] for row in final_counts}
                    self.results['breakdown'] = {row['category']: row['count'] for row in breakdown}
                    self.results['success'] = total_members == 542
                    
        except Exception as e:
            print(f"❌ Final verification failed: {e}")

def main():
    """Execute member count corrections"""
    corrector = MemberCountCorrection()
    
    # Run dry run first
    print("🔍 RUNNING DRY RUN ANALYSIS...")
    dry_results = corrector.execute_corrections(dry_run=True)
    
    print("\\n" + "="*60)
    print("DRY RUN COMPLETE - READY FOR LIVE EXECUTION")
    print("="*60)
    
    changes = []
    if dry_results.get('territorial_delegates_moved', 0) > 0:
        changes.append(f"Move {dry_results['territorial_delegates_moved']} territorial delegates to House")
    if dry_results.get('senator_duplicates_removed', 0) > 0:
        changes.append(f"Remove {dry_results['senator_duplicates_removed']} senator duplicates")
    if dry_results.get('vp_added', False):
        changes.append("Add Vice President Kamala Harris")
    
    print("Planned changes:")
    for i, change in enumerate(changes, 1):
        print(f"  {i}. {change}")
    
    # Save dry run results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dry_run_file = f"member_correction_dry_run_{timestamp}.json"
    with open(dry_run_file, 'w') as f:
        json.dump(dry_results, f, indent=2, default=str)
    
    print(f"\\n📄 Dry run results saved to: {dry_run_file}")
    return dry_results

if __name__ == "__main__":
    main()