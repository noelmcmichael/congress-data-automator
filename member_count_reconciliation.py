#!/usr/bin/env python3
"""
Member Count Reconciliation Analysis

Investigates and resolves Congressional member count discrepancies.
Target: 441 House + 101 Senate = 542 total members
Current: 570 members (28 over target)
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import requests
from collections import defaultdict, Counter

load_dotenv()

class MemberReconciliationAnalyzer:
    """Comprehensive member count analysis and reconciliation"""
    
    def __init__(self):
        self.db_url = os.getenv('DATABASE_URL')
        self.api_key = os.getenv('CONGRESS_API_KEY')
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'analysis': 'Member Count Reconciliation',
            'target_counts': {
                'house_total': 441,
                'house_voting': 435,
                'house_nonvoting': 6,
                'senate_total': 101,
                'senate_members': 100,
                'senate_vp': 1,
                'grand_total': 542
            }
        }
    
    def execute_full_analysis(self) -> Dict:
        """Execute comprehensive member count reconciliation"""
        print("=" * 60)
        print("CONGRESSIONAL MEMBER COUNT RECONCILIATION")
        print("=" * 60)
        
        # Phase A: Current Database Analysis
        self._analyze_current_database()
        
        # Phase B: Duplicate Detection
        self._detect_duplicates()
        
        # Phase C: Historical Member Analysis
        self._analyze_historical_members()
        
        # Phase D: Chamber-Specific Analysis
        self._analyze_chamber_specifics()
        
        # Phase E: Official Source Cross-Reference
        self._cross_reference_official_sources()
        
        # Phase F: Generate Recommendations
        self._generate_recommendations()
        
        return self.results
    
    def _analyze_current_database(self):
        """Phase A: Analyze current database state"""
        print("\n📊 Phase A: Current Database Analysis")
        
        try:
            with psycopg2.connect(self.db_url) as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    
                    # Basic count analysis
                    cur.execute("""
                        SELECT 
                            chamber,
                            COUNT(*) as total_count,
                            COUNT(*) FILTER (WHERE is_current = true) as current_count,
                            COUNT(*) FILTER (WHERE is_current = false OR is_current IS NULL) as inactive_count
                        FROM members 
                        GROUP BY chamber
                        ORDER BY chamber
                    """)
                    chamber_analysis = cur.fetchall()
                    
                    # Recent additions analysis
                    cur.execute("""
                        SELECT 
                            DATE(created_at) as creation_date,
                            chamber,
                            COUNT(*) as count
                        FROM members 
                        WHERE created_at >= '2025-01-08'
                        GROUP BY DATE(created_at), chamber
                        ORDER BY creation_date, chamber
                    """)
                    recent_additions = cur.fetchall()
                    
                    # State distribution analysis
                    cur.execute("""
                        SELECT 
                            state,
                            chamber,
                            COUNT(*) as count
                        FROM members 
                        WHERE is_current = true
                        GROUP BY state, chamber
                        HAVING COUNT(*) > 2  -- Flag unusual state counts
                        ORDER BY count DESC, state
                    """)
                    unusual_state_counts = cur.fetchall()
                    
                    # Store results
                    self.results['current_database'] = {
                        'chamber_analysis': [dict(row) for row in chamber_analysis],
                        'recent_additions': [dict(row) for row in recent_additions],
                        'unusual_state_counts': [dict(row) for row in unusual_state_counts]
                    }
                    
                    # Print summary
                    print("Chamber Analysis:")
                    total_current = 0
                    for row in chamber_analysis:
                        print(f"  {row['chamber']}: {row['current_count']} current, {row['inactive_count']} inactive")
                        total_current += row['current_count']
                    print(f"  TOTAL CURRENT: {total_current}")
                    print(f"  TARGET: 542")
                    print(f"  DISCREPANCY: {total_current - 542:+d}")
                    
        except Exception as e:
            print(f"❌ Database analysis failed: {e}")
            self.results['current_database'] = {'error': str(e)}
    
    def _detect_duplicates(self):
        """Phase B: Detect potential duplicate members"""
        print("\n🔍 Phase B: Duplicate Detection")
        
        try:
            with psycopg2.connect(self.db_url) as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    
                    # Name-based duplicates
                    cur.execute("""
                        SELECT 
                            first_name, last_name, state, chamber,
                            COUNT(*) as count,
                            STRING_AGG(bioguide_id, ', ') as bioguide_ids,
                            STRING_AGG(CAST(id AS TEXT), ', ') as db_ids
                        FROM members 
                        WHERE is_current = true
                        GROUP BY first_name, last_name, state, chamber
                        HAVING COUNT(*) > 1
                        ORDER BY count DESC
                    """)
                    name_duplicates = cur.fetchall()
                    
                    # Bioguide duplicates (shouldn't exist)
                    cur.execute("""
                        SELECT 
                            bioguide_id,
                            COUNT(*) as count,
                            STRING_AGG(first_name || ' ' || last_name, ', ') as names
                        FROM members 
                        WHERE is_current = true
                        GROUP BY bioguide_id
                        HAVING COUNT(*) > 1
                        ORDER BY count DESC
                    """)
                    bioguide_duplicates = cur.fetchall()
                    
                    # State-district duplicates (House only)
                    cur.execute("""
                        SELECT 
                            state, district,
                            COUNT(*) as count,
                            STRING_AGG(first_name || ' ' || last_name, ', ') as names,
                            STRING_AGG(bioguide_id, ', ') as bioguide_ids
                        FROM members 
                        WHERE is_current = true AND chamber = 'House' AND district IS NOT NULL
                        GROUP BY state, district
                        HAVING COUNT(*) > 1
                        ORDER BY count DESC
                    """)
                    district_duplicates = cur.fetchall()
                    
                    self.results['duplicates'] = {
                        'name_duplicates': [dict(row) for row in name_duplicates],
                        'bioguide_duplicates': [dict(row) for row in bioguide_duplicates],
                        'district_duplicates': [dict(row) for row in district_duplicates]
                    }
                    
                    # Print findings
                    print(f"Name-based duplicates: {len(name_duplicates)}")
                    print(f"Bioguide duplicates: {len(bioguide_duplicates)}")
                    print(f"District duplicates: {len(district_duplicates)}")
                    
                    if name_duplicates:
                        print("\nName duplicates found:")
                        for dup in name_duplicates[:5]:  # Show first 5
                            print(f"  {dup['first_name']} {dup['last_name']} ({dup['state']}-{dup['chamber']}): {dup['count']} records")
                    
        except Exception as e:
            print(f"❌ Duplicate detection failed: {e}")
            self.results['duplicates'] = {'error': str(e)}
    
    def _analyze_historical_members(self):
        """Phase C: Analyze historical vs current member status"""
        print("\n📅 Phase C: Historical Member Analysis")
        
        try:
            with psycopg2.connect(self.db_url) as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    
                    # Members with no current flag or false
                    cur.execute("""
                        SELECT 
                            chamber,
                            COUNT(*) FILTER (WHERE is_current IS NULL) as null_current,
                            COUNT(*) FILTER (WHERE is_current = false) as false_current,
                            COUNT(*) FILTER (WHERE term_end < CURRENT_DATE) as past_term,
                            COUNT(*) FILTER (WHERE created_at < '2025-01-08') as pre_phase2
                        FROM members 
                        GROUP BY chamber
                    """)
                    current_status_analysis = cur.fetchall()
                    
                    # Sample of potentially historical members
                    cur.execute("""
                        SELECT 
                            first_name, last_name, chamber, state,
                            is_current, term_start, term_end, created_at,
                            bioguide_id
                        FROM members 
                        WHERE is_current = false OR is_current IS NULL
                        ORDER BY created_at DESC
                        LIMIT 10
                    """)
                    sample_historical = cur.fetchall()
                    
                    self.results['historical_analysis'] = {
                        'current_status_analysis': [dict(row) for row in current_status_analysis],
                        'sample_historical': [dict(row) for row in sample_historical]
                    }
                    
                    print("Current status analysis:")
                    for row in current_status_analysis:
                        print(f"  {row['chamber']}: {row['null_current']} null, {row['false_current']} false, {row['past_term']} past term")
                    
        except Exception as e:
            print(f"❌ Historical analysis failed: {e}")
            self.results['historical_analysis'] = {'error': str(e)}
    
    def _analyze_chamber_specifics(self):
        """Phase D: Chamber-specific constitutional requirements"""
        print("\n🏛️ Phase D: Chamber-Specific Analysis")
        
        try:
            with psycopg2.connect(self.db_url) as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    
                    # House analysis
                    cur.execute("""
                        SELECT 
                            state,
                            COUNT(*) as rep_count,
                            STRING_AGG(DISTINCT district ORDER BY district::int) as districts
                        FROM members 
                        WHERE chamber = 'House' AND is_current = true
                        GROUP BY state
                        ORDER BY rep_count DESC
                    """)
                    house_by_state = cur.fetchall()
                    
                    # Senate analysis
                    cur.execute("""
                        SELECT 
                            state,
                            COUNT(*) as senator_count,
                            STRING_AGG(first_name || ' ' || last_name, ', ') as senators
                        FROM members 
                        WHERE chamber = 'Senate' AND is_current = true
                        GROUP BY state
                        HAVING COUNT(*) != 2  -- Should be exactly 2 per state
                        ORDER BY senator_count DESC
                    """)
                    unusual_senate_counts = cur.fetchall()
                    
                    # Non-voting delegates/territories
                    cur.execute("""
                        SELECT 
                            state, district,
                            first_name || ' ' || last_name as name,
                            bioguide_id
                        FROM members 
                        WHERE chamber = 'House' AND is_current = true
                        AND state IN ('DC', 'PR', 'VI', 'GU', 'AS', 'MP')
                        ORDER BY state
                    """)
                    non_voting_delegates = cur.fetchall()
                    
                    # Vice President check
                    cur.execute("""
                        SELECT 
                            first_name || ' ' || last_name as name,
                            bioguide_id, party
                        FROM members 
                        WHERE chamber = 'Senate' AND is_current = true
                        AND (LOWER(first_name || ' ' || last_name) LIKE '%harris%'
                             OR LOWER(first_name || ' ' || last_name) LIKE '%vice president%')
                    """)
                    vp_search = cur.fetchall()
                    
                    self.results['chamber_specifics'] = {
                        'house_by_state': [dict(row) for row in house_by_state],
                        'unusual_senate_counts': [dict(row) for row in unusual_senate_counts],
                        'non_voting_delegates': [dict(row) for row in non_voting_delegates],
                        'vp_search': [dict(row) for row in vp_search]
                    }
                    
                    print(f"House members by state: {len(house_by_state)} states")
                    print(f"States with unusual Senate counts: {len(unusual_senate_counts)}")
                    print(f"Non-voting delegates found: {len(non_voting_delegates)}")
                    print(f"VP search results: {len(vp_search)}")
                    
                    if unusual_senate_counts:
                        print("\nStates with unusual Senate counts:")
                        for state in unusual_senate_counts[:10]:
                            print(f"  {state['state']}: {state['senator_count']} senators")
                    
        except Exception as e:
            print(f"❌ Chamber analysis failed: {e}")
            self.results['chamber_specifics'] = {'error': str(e)}
    
    def _cross_reference_official_sources(self):
        """Phase E: Cross-reference with official sources"""
        print("\n🌐 Phase E: Official Source Cross-Reference")
        
        # Test Congress.gov API parameters
        if self.api_key:
            try:
                # Test different API parameters
                test_urls = [
                    ('current_members', 'https://api.congress.gov/v3/member?currentMember=true&limit=250'),
                    ('house_current', 'https://api.congress.gov/v3/member?currentMember=true&chamber=house&limit=250'),
                    ('senate_current', 'https://api.congress.gov/v3/member?currentMember=true&chamber=senate&limit=250'),
                ]
                
                api_results = {}
                for test_name, url in test_urls:
                    try:
                        response = requests.get(url, params={'api_key': self.api_key}, timeout=10)
                        if response.status_code == 200:
                            data = response.json()
                            count = len(data.get('members', []))
                            api_results[test_name] = {
                                'count': count,
                                'status': 'success'
                            }
                            print(f"  {test_name}: {count} members")
                        else:
                            api_results[test_name] = {
                                'count': 0,
                                'status': f'error_{response.status_code}'
                            }
                    except Exception as e:
                        api_results[test_name] = {
                            'count': 0,
                            'status': f'exception_{str(e)[:50]}'
                        }
                
                self.results['official_sources'] = {'congress_api': api_results}
                
            except Exception as e:
                print(f"❌ API cross-reference failed: {e}")
                self.results['official_sources'] = {'error': str(e)}
        else:
            print("⚠️ No API key available for cross-reference")
            self.results['official_sources'] = {'error': 'No API key'}
    
    def _generate_recommendations(self):
        """Phase F: Generate specific recommendations for reconciliation"""
        print("\n💡 Phase F: Generating Recommendations")
        
        recommendations = []
        
        # Analyze current vs target counts
        chamber_analysis = self.results.get('current_database', {}).get('chamber_analysis', [])
        current_totals = {row['chamber']: row['current_count'] for row in chamber_analysis}
        
        house_current = current_totals.get('House', 0)
        senate_current = current_totals.get('Senate', 0)
        total_current = house_current + senate_current
        
        # House recommendations
        if house_current != 441:
            diff = house_current - 441
            if diff > 0:
                recommendations.append({
                    'priority': 'HIGH',
                    'chamber': 'House',
                    'issue': f'{diff} excess members',
                    'action': f'Remove {diff} duplicate or inactive House members',
                    'sql_investigation': """
                        SELECT * FROM members 
                        WHERE chamber = 'House' AND is_current = true
                        ORDER BY created_at DESC, bioguide_id
                    """
                })
            else:
                recommendations.append({
                    'priority': 'HIGH',
                    'chamber': 'House', 
                    'issue': f'{abs(diff)} missing members',
                    'action': f'Add {abs(diff)} missing House members',
                    'sql_investigation': "Check for representatives missing from database"
                })
        
        # Senate recommendations
        if senate_current != 101:
            diff = senate_current - 101
            if diff > 0:
                recommendations.append({
                    'priority': 'HIGH',
                    'chamber': 'Senate',
                    'issue': f'{diff} excess members',
                    'action': f'Remove {diff} duplicate or inactive Senate members', 
                    'sql_investigation': """
                        SELECT * FROM members 
                        WHERE chamber = 'Senate' AND is_current = true
                        ORDER BY created_at DESC, bioguide_id
                    """
                })
            else:
                recommendations.append({
                    'priority': 'HIGH',
                    'chamber': 'Senate',
                    'issue': f'{abs(diff)} missing members',
                    'action': f'Add {abs(diff)} missing Senate members (including VP)',
                    'sql_investigation': "Check for missing senators or VP"
                })
        
        # Duplicate-based recommendations
        duplicates = self.results.get('duplicates', {})
        if duplicates.get('name_duplicates'):
            recommendations.append({
                'priority': 'MEDIUM',
                'chamber': 'Both',
                'issue': f"{len(duplicates['name_duplicates'])} name-based duplicates",
                'action': 'Review and merge duplicate member records',
                'sql_investigation': "Manual review of name duplicates required"
            })
        
        self.results['recommendations'] = recommendations
        
        # Print recommendations
        print(f"Generated {len(recommendations)} recommendations:")
        for i, rec in enumerate(recommendations, 1):
            print(f"  {i}. [{rec['priority']}] {rec['chamber']}: {rec['action']}")
        
        return recommendations

def main():
    """Execute member count reconciliation analysis"""
    analyzer = MemberReconciliationAnalyzer()
    results = analyzer.execute_full_analysis()
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = f"member_reconciliation_analysis_{timestamp}.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n📊 RECONCILIATION SUMMARY")
    print("=" * 40)
    
    # Current state
    chamber_analysis = results.get('current_database', {}).get('chamber_analysis', [])
    for row in chamber_analysis:
        chamber = row['chamber']
        current = row['current_count']
        target = 441 if chamber == 'House' else 101
        status = "✅" if current == target else "❌"
        print(f"{chamber}: {current}/{target} {status}")
    
    # Total
    total_current = sum(row['current_count'] for row in chamber_analysis)
    print(f"TOTAL: {total_current}/542 {'✅' if total_current == 542 else '❌'}")
    print(f"DISCREPANCY: {total_current - 542:+d}")
    
    # Recommendations
    recommendations = results.get('recommendations', [])
    high_priority = [r for r in recommendations if r['priority'] == 'HIGH']
    if high_priority:
        print(f"\n🚨 HIGH PRIORITY ACTIONS: {len(high_priority)}")
        for rec in high_priority:
            print(f"  • {rec['chamber']}: {rec['action']}")
    
    print(f"\n📄 Full analysis saved to: {results_file}")
    return results

if __name__ == "__main__":
    main()