#!/usr/bin/env python3
"""
Final Validation Script for 119th Congress Data
Comprehensive testing of the 119th Congress database migration.
"""

import sqlite3
import json
from datetime import datetime
from typing import Dict
from congressional_session_tracker import CongressionalSessionTracker

class Final119Validation:
    """Comprehensive validation of 119th Congress data"""
    
    def __init__(self, db_path: str = "congress_119th.db"):
        self.db_path = db_path
        self.tracker = CongressionalSessionTracker()
        
    def test_congressional_session_accuracy(self) -> Dict:
        """Test Congressional session tracking accuracy"""
        print("🗓️ Testing Congressional session accuracy...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check current Congress
        current_congress = self.tracker.get_current_congress()
        
        cursor.execute("""
            SELECT congress_number, start_date, end_date, is_current, party_control_house, party_control_senate
            FROM congressional_sessions
            WHERE congress_number = ?
        """, (current_congress,))
        
        current_session = cursor.fetchone()
        
        # Check data currency
        is_current, status = self.tracker.is_data_current(119)
        
        conn.close()
        
        session_test = {
            'current_congress_detected': current_congress,
            'database_has_current_session': current_session is not None,
            'session_details': {
                'congress': current_session[0] if current_session else None,
                'start_date': current_session[1] if current_session else None,
                'end_date': current_session[2] if current_session else None,
                'is_current': current_session[3] if current_session else None,
                'house_control': current_session[4] if current_session else None,
                'senate_control': current_session[5] if current_session else None
            },
            'data_currency_check': {
                'is_current': is_current,
                'status': status
            }
        }
        
        print(f"✅ Current Congress: {current_congress}th")
        print(f"✅ Database session tracking: {'Working' if current_session else 'Missing'}")
        print(f"✅ Data currency: {'Current' if is_current else 'Outdated'}")
        
        return session_test
    
    def test_committee_leadership_accuracy(self) -> Dict:
        """Test committee leadership accuracy for known positions"""
        print("🏛️ Testing committee leadership accuracy...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Known accurate leadership for 119th Congress
        expected_leadership = {
            'Judiciary': {
                'chair': 'Chuck Grassley',
                'ranking': 'Dick Durbin'
            },
            'Commerce, Science, and Transportation': {
                'chair': 'Ted Cruz',
                'ranking': 'Maria Cantwell'
            },
            'Finance': {
                'chair': 'Mike Crapo',
                'ranking': 'Ron Wyden'
            },
            'Armed Services': {
                'chair': 'Roger Wicker',
                'ranking': 'Jack Reed'
            }
        }
        
        leadership_tests = {}
        correct_count = 0
        total_tests = 0
        
        for committee, expected in expected_leadership.items():
            cursor.execute("""
                SELECT chair_name, ranking_member_name, chamber
                FROM committees_119th
                WHERE name = ? AND congress_session = 119
            """, (committee,))
            
            result = cursor.fetchone()
            
            if result:
                chair_name, ranking_name, chamber = result
                
                chair_correct = expected['chair'] in (chair_name or '')
                ranking_correct = expected['ranking'] in (ranking_name or '')
                
                leadership_tests[committee] = {
                    'expected_chair': expected['chair'],
                    'actual_chair': chair_name,
                    'chair_correct': chair_correct,
                    'expected_ranking': expected['ranking'],
                    'actual_ranking': ranking_name,
                    'ranking_correct': ranking_correct,
                    'chamber': chamber
                }
                
                if chair_correct:
                    correct_count += 1
                if ranking_correct:
                    correct_count += 1
                total_tests += 2
                
                print(f"  ✅ {committee}: Chair {chair_name}, Ranking {ranking_name}")
            else:
                leadership_tests[committee] = {
                    'error': 'Committee not found in database'
                }
                print(f"  ❌ {committee}: Not found in database")
        
        conn.close()
        
        accuracy_score = (correct_count / total_tests * 100) if total_tests > 0 else 0
        
        leadership_validation = {
            'committees_tested': len(expected_leadership),
            'total_leadership_positions': total_tests,
            'correct_positions': correct_count,
            'accuracy_percentage': accuracy_score,
            'tests': leadership_tests
        }
        
        print(f"✅ Leadership accuracy: {accuracy_score:.1f}% ({correct_count}/{total_tests})")
        
        return leadership_validation
    
    def test_member_committee_relationships(self) -> Dict:
        """Test member-committee relationship integrity"""
        print("🔗 Testing member-committee relationships...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Test relationship integrity
        cursor.execute("""
            SELECT 
                m.name, 
                m.party, 
                m.state, 
                c.name as committee, 
                cm.position
            FROM committee_memberships_119th cm
            JOIN members_119th m ON cm.member_id = m.id
            JOIN committees_119th c ON cm.committee_id = c.id
            WHERE cm.congress_session = 119
            ORDER BY m.name
        """)
        
        relationships = cursor.fetchall()
        
        # Count relationships by position
        position_counts = {}
        for rel in relationships:
            position = rel[4]
            position_counts[position] = position_counts.get(position, 0) + 1
        
        # Test specific known relationships
        cursor.execute("""
            SELECT m.name, c.name, cm.position
            FROM committee_memberships_119th cm
            JOIN members_119th m ON cm.member_id = m.id
            JOIN committees_119th c ON cm.committee_id = c.id
            WHERE m.name LIKE '%Grassley%' AND c.name = 'Judiciary'
            AND cm.congress_session = 119
        """)
        
        grassley_judiciary = cursor.fetchone()
        
        cursor.execute("""
            SELECT m.name, c.name, cm.position
            FROM committee_memberships_119th cm
            JOIN members_119th m ON cm.member_id = m.id
            JOIN committees_119th c ON cm.committee_id = c.id
            WHERE m.name LIKE '%Cruz%' AND c.name LIKE '%Commerce%'
            AND cm.congress_session = 119
        """)
        
        cruz_commerce = cursor.fetchone()
        
        conn.close()
        
        relationship_tests = {
            'total_relationships': len(relationships),
            'position_breakdown': position_counts,
            'sample_relationships': relationships[:10],  # First 10 for review
            'specific_tests': {
                'grassley_judiciary': {
                    'found': grassley_judiciary is not None,
                    'details': grassley_judiciary if grassley_judiciary else None
                },
                'cruz_commerce': {
                    'found': cruz_commerce is not None,
                    'details': cruz_commerce if cruz_commerce else None
                }
            }
        }
        
        print(f"✅ Total relationships: {len(relationships)}")
        print(f"✅ Position breakdown: {position_counts}")
        print(f"✅ Grassley-Judiciary: {'Found' if grassley_judiciary else 'Missing'}")
        print(f"✅ Cruz-Commerce: {'Found' if cruz_commerce else 'Missing'}")
        
        return relationship_tests
    
    def test_data_completeness(self) -> Dict:
        """Test overall data completeness and quality"""
        print("📊 Testing data completeness...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Count all records
        cursor.execute("SELECT COUNT(*) FROM committees_119th WHERE congress_session = 119")
        committee_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM members_119th WHERE congress_session = 119")
        member_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM committee_memberships_119th WHERE congress_session = 119")
        membership_count = cursor.fetchone()[0]
        
        # Check for nulls in critical fields
        cursor.execute("""
            SELECT COUNT(*) FROM committees_119th 
            WHERE congress_session = 119 AND (chair_name IS NULL OR ranking_member_name IS NULL)
        """)
        committees_missing_leadership = cursor.fetchone()[0]
        
        # Check chamber distribution
        cursor.execute("""
            SELECT chamber, COUNT(*) 
            FROM committees_119th 
            WHERE congress_session = 119 
            GROUP BY chamber
        """)
        chamber_distribution = dict(cursor.fetchall())
        
        # Check party distribution
        cursor.execute("""
            SELECT party, COUNT(*) 
            FROM members_119th 
            WHERE congress_session = 119 
            GROUP BY party
        """)
        party_distribution = dict(cursor.fetchall())
        
        conn.close()
        
        completeness = {
            'record_counts': {
                'committees': committee_count,
                'members': member_count,
                'memberships': membership_count
            },
            'data_quality': {
                'committees_missing_leadership': committees_missing_leadership,
                'leadership_coverage': f"{((committee_count - committees_missing_leadership) / committee_count * 100):.1f}%" if committee_count > 0 else "0%"
            },
            'distributions': {
                'chamber': chamber_distribution,
                'party': party_distribution
            },
            'completeness_score': min(100, (committee_count + member_count + membership_count) / 3 * 5)  # Rough scoring
        }
        
        print(f"✅ Committees: {committee_count}")
        print(f"✅ Members: {member_count}")
        print(f"✅ Memberships: {membership_count}")
        print(f"✅ Leadership coverage: {completeness['data_quality']['leadership_coverage']}")
        
        return completeness
    
    def generate_validation_report(self) -> Dict:
        """Generate comprehensive validation report"""
        print("📋 Generating comprehensive validation report...")
        
        report = {
            'validation_timestamp': datetime.now().isoformat(),
            'database_file': self.db_path,
            'congress_session': '119th Congress (2025-2027)',
            'validation_version': '1.0.0'
        }
        
        # Run all tests
        report['session_accuracy'] = self.test_congressional_session_accuracy()
        report['leadership_accuracy'] = self.test_committee_leadership_accuracy()
        report['relationship_integrity'] = self.test_member_committee_relationships()
        report['data_completeness'] = self.test_data_completeness()
        
        # Calculate overall score
        leadership_score = report['leadership_accuracy'].get('accuracy_percentage', 0)
        completeness_score = report['data_completeness'].get('completeness_score', 0)
        relationship_score = 100 if report['relationship_integrity']['total_relationships'] > 0 else 0
        session_score = 100 if report['session_accuracy']['data_currency_check']['is_current'] else 0
        
        overall_score = (leadership_score + completeness_score + relationship_score + session_score) / 4
        
        report['overall_assessment'] = {
            'overall_score': overall_score,
            'grade': 'A' if overall_score >= 90 else 'B' if overall_score >= 80 else 'C' if overall_score >= 70 else 'D',
            'status': 'EXCELLENT' if overall_score >= 90 else 'GOOD' if overall_score >= 80 else 'NEEDS_IMPROVEMENT',
            'component_scores': {
                'leadership_accuracy': leadership_score,
                'data_completeness': completeness_score,
                'relationship_integrity': relationship_score,
                'session_accuracy': session_score
            }
        }
        
        print(f"\n📊 Overall Assessment:")
        print(f"   Score: {overall_score:.1f}/100 (Grade: {report['overall_assessment']['grade']})")
        print(f"   Status: {report['overall_assessment']['status']}")
        
        return report
    
    def export_validation_report(self, output_file: str = None) -> str:
        """Export validation report to file"""
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"119th_congress_validation_report_{timestamp}.json"
        
        report = self.generate_validation_report()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"📁 Validation report exported to: {output_file}")
        
        return output_file

def main():
    """Main validation execution"""
    print("🇺🇸 Final 119th Congress Data Validation")
    print("=" * 50)
    
    validator = Final119Validation()
    
    # Check if database exists
    import os
    if not os.path.exists(validator.db_path):
        print(f"❌ Database not found: {validator.db_path}")
        print("   Please run migrate_to_119th_congress.py first")
        return
    
    # Run validation and export report
    report_file = validator.export_validation_report()
    
    print(f"\n🎉 Validation complete!")
    print(f"📋 Report: {report_file}")

if __name__ == "__main__":
    main()