#!/usr/bin/env python3
"""
Hearing Committee Matcher - Phase 3 Implementation
Match hearings to committees based on title analysis and keywords
"""

import requests
import json
import re
from datetime import datetime
from typing import List, Dict, Optional, Tuple

class HearingCommitteeMatcher:
    def __init__(self):
        self.production_api_url = "https://congressional-data-api-v3-1066017671167.us-central1.run.app/api/v1"
        self.existing_hearings = []
        self.existing_committees = {}
        self.committee_patterns = {}
        
    def load_existing_data(self) -> bool:
        """Load existing hearings and committees from production API"""
        print("📥 Loading existing data from production API...")
        
        try:
            # Load hearings
            hearings_response = requests.get(f"{self.production_api_url}/hearings?limit=200")
            if hearings_response.status_code == 200:
                hearings_data = hearings_response.json()
                self.existing_hearings = hearings_data if isinstance(hearings_data, list) else hearings_data.get('hearings', [])
                print(f"✅ Loaded {len(self.existing_hearings)} hearings")
            else:
                print(f"❌ Failed to load hearings: {hearings_response.status_code}")
                return False
            
            # Load committees
            committees_response = requests.get(f"{self.production_api_url}/committees?limit=200")
            if committees_response.status_code == 200:
                committees_data = committees_response.json()
                committees_list = committees_data if isinstance(committees_data, list) else committees_data.get('committees', [])
                
                # Create mapping for easy lookup
                self.existing_committees = {}
                for committee in committees_list:
                    name = committee.get('name', '').lower()
                    self.existing_committees[name] = committee
                
                print(f"✅ Loaded {len(committees_list)} committees")
                return True
            else:
                print(f"❌ Failed to load committees: {committees_response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error loading existing data: {e}")
            return False
    
    def create_committee_patterns(self) -> Dict[str, List[str]]:
        """Create pattern matching rules for committees"""
        print("🔄 Creating committee pattern matching rules...")
        
        # Committee name patterns for matching
        patterns = {
            'judiciary': [
                'judiciary', 'judicial', 'justice', 'courts', 'judges', 'supreme court',
                'federal courts', 'constitutional', 'civil rights', 'criminal justice',
                'immigration', 'antitrust', 'intellectual property', 'patents'
            ],
            'armed services': [
                'armed services', 'defense', 'military', 'pentagon', 'army', 'navy',
                'air force', 'marines', 'national security', 'weapons', 'veterans',
                'warfare', 'troops', 'soldiers', 'combat', 'strategic'
            ],
            'finance': [
                'finance', 'financial', 'treasury', 'tax', 'taxes', 'taxation',
                'budget', 'fiscal', 'economic', 'economy', 'banking', 'securities',
                'insurance', 'trade', 'tariff', 'customs', 'revenue'
            ],
            'agriculture': [
                'agriculture', 'farming', 'food', 'rural', 'crop', 'livestock',
                'agricultural', 'farm', 'nutrition', 'forestry', 'conservation',
                'usda', 'department of agriculture'
            ],
            'appropriations': [
                'appropriations', 'spending', 'budget', 'funding', 'allocation',
                'fiscal', 'money', 'dollars', 'expenditure', 'federal budget'
            ],
            'energy': [
                'energy', 'oil', 'gas', 'nuclear', 'renewable', 'electricity',
                'power', 'coal', 'petroleum', 'natural resources', 'environment',
                'climate', 'solar', 'wind', 'hydroelectric'
            ],
            'health': [
                'health', 'healthcare', 'medical', 'medicine', 'hospital',
                'education', 'labor', 'pensions', 'social security', 'medicare',
                'medicaid', 'public health', 'disease', 'pandemic'
            ],
            'homeland security': [
                'homeland security', 'security', 'terrorism', 'border', 'immigration',
                'customs', 'tsa', 'fema', 'emergency', 'disaster', 'cybersecurity'
            ],
            'foreign relations': [
                'foreign relations', 'international', 'diplomatic', 'embassy',
                'ambassador', 'treaty', 'foreign policy', 'state department',
                'foreign aid', 'international trade'
            ],
            'commerce': [
                'commerce', 'business', 'trade', 'industry', 'manufacturing',
                'transportation', 'technology', 'science', 'research',
                'telecommunications', 'internet', 'regulation'
            ],
            'oversight': [
                'oversight', 'government reform', 'accountability', 'investigation',
                'whistleblower', 'ethics', 'corruption', 'transparency'
            ],
            'intelligence': [
                'intelligence', 'cia', 'fbi', 'nsa', 'classified', 'surveillance',
                'counterintelligence', 'national intelligence'
            ],
            'small business': [
                'small business', 'entrepreneurship', 'startup', 'sba',
                'minority business', 'women business'
            ],
            'rules': [
                'rules', 'administration', 'procedure', 'parliamentary',
                'election', 'voting', 'campaign finance'
            ],
            'ethics': [
                'ethics', 'standards', 'conduct', 'investigation',
                'disciplinary', 'complaints'
            ]
        }
        
        # Map pattern keys to actual committee names in database
        self.committee_patterns = {}
        
        for pattern_key, keywords in patterns.items():
            # Find matching committees in database
            matching_committees = []
            
            for db_name, db_committee in self.existing_committees.items():
                for keyword in keywords:
                    if keyword.lower() in db_name.lower():
                        matching_committees.append(db_committee)
                        break
            
            if matching_committees:
                self.committee_patterns[pattern_key] = {
                    'keywords': keywords,
                    'committees': matching_committees
                }
        
        print(f"✅ Created {len(self.committee_patterns)} committee pattern groups")
        
        # Show some examples
        print("📋 Pattern examples:")
        for pattern_key, pattern_data in list(self.committee_patterns.items())[:3]:
            committee_names = [c.get('name', 'Unknown') for c in pattern_data['committees']]
            print(f"  - {pattern_key}: {len(pattern_data['committees'])} committees")
            print(f"    Keywords: {pattern_data['keywords'][:5]}...")
            print(f"    Matches: {committee_names[:2]}...")
        
        return self.committee_patterns
    
    def match_hearing_to_committee(self, hearing: Dict) -> Optional[Dict]:
        """Match a hearing to a committee based on title analysis"""
        title = hearing.get('title', '').lower()
        
        if not title or title.strip() == '':
            return None
        
        # Score each committee pattern
        pattern_scores = {}
        
        for pattern_key, pattern_data in self.committee_patterns.items():
            score = 0
            keywords = pattern_data['keywords']
            
            # Count keyword matches in title
            for keyword in keywords:
                if keyword.lower() in title:
                    # Weight longer keywords more heavily
                    score += len(keyword.split())
            
            if score > 0:
                pattern_scores[pattern_key] = score
        
        # Find the best matching pattern
        if pattern_scores:
            best_pattern = max(pattern_scores, key=pattern_scores.get)
            best_score = pattern_scores[best_pattern]
            
            # Return the first committee from the best pattern
            committees = self.committee_patterns[best_pattern]['committees']
            if committees:
                return {
                    'committee': committees[0],
                    'pattern': best_pattern,
                    'score': best_score,
                    'keywords_found': [kw for kw in self.committee_patterns[best_pattern]['keywords'] if kw.lower() in title]
                }
        
        return None
    
    def create_hearing_committee_matches(self) -> List[Dict]:
        """Create hearing-committee matches for all hearings"""
        print("🔄 Creating hearing-committee matches...")
        
        matches = []
        
        for hearing in self.existing_hearings:
            hearing_id = hearing.get('id')
            title = hearing.get('title', '')
            
            # Skip hearings that already have committee assignments
            if hearing.get('committee_id'):
                continue
            
            # Try to match to committee
            match_result = self.match_hearing_to_committee(hearing)
            
            if match_result:
                committee = match_result['committee']
                
                match_data = {
                    'hearing_id': hearing_id,
                    'hearing_title': title[:100] + "..." if len(title) > 100 else title,
                    'committee_id': committee.get('id'),
                    'committee_name': committee.get('name'),
                    'match_pattern': match_result['pattern'],
                    'match_score': match_result['score'],
                    'keywords_found': match_result['keywords_found'],
                    'confidence': 'high' if match_result['score'] >= 2 else 'medium'
                }
                
                matches.append(match_data)
                print(f"✅ Matched: {match_data['hearing_title'][:50]}... → {match_data['committee_name']}")
            else:
                print(f"❌ No match: {title[:50]}...")
        
        return matches
    
    def validate_matches(self, matches: List[Dict]) -> Dict:
        """Validate the hearing-committee matches"""
        print("🔍 Validating hearing-committee matches...")
        
        # Statistics
        total_hearings = len(self.existing_hearings)
        matched_hearings = len(matches)
        match_rate = (matched_hearings / total_hearings) * 100 if total_hearings > 0 else 0
        
        # Committee distribution
        committee_counts = {}
        for match in matches:
            committee_name = match['committee_name']
            if committee_name not in committee_counts:
                committee_counts[committee_name] = 0
            committee_counts[committee_name] += 1
        
        # Confidence distribution
        confidence_counts = {}
        for match in matches:
            confidence = match['confidence']
            if confidence not in confidence_counts:
                confidence_counts[confidence] = 0
            confidence_counts[confidence] += 1
        
        validation_report = {
            'total_hearings': total_hearings,
            'matched_hearings': matched_hearings,
            'unmatched_hearings': total_hearings - matched_hearings,
            'match_rate': match_rate,
            'committee_distribution': committee_counts,
            'confidence_distribution': confidence_counts,
            'validation_passed': matched_hearings > 0
        }
        
        print(f"📊 Validation Results:")
        print(f"  Total hearings: {validation_report['total_hearings']}")
        print(f"  Matched hearings: {validation_report['matched_hearings']}")
        print(f"  Match rate: {validation_report['match_rate']:.1f}%")
        print(f"  Committee distribution: {committee_counts}")
        print(f"  Confidence distribution: {confidence_counts}")
        
        return validation_report
    
    def create_sql_update_script(self, matches: List[Dict]) -> str:
        """Create SQL script to update hearing committee assignments"""
        print("🔄 Creating SQL update script for hearings...")
        
        sql_statements = []
        
        sql_statements.append("-- Update hearing committee assignments")
        sql_statements.append("-- Generated by hearing_committee_matcher.py")
        sql_statements.append("")
        
        for match in matches:
            hearing_id = match['hearing_id']
            committee_id = match['committee_id']
            title = match['hearing_title'].replace("'", "''")  # Escape quotes
            
            sql_statements.append(f"-- Update hearing: {title}")
            sql_statements.append(f"UPDATE hearings SET committee_id = {committee_id} WHERE id = {hearing_id};")
            sql_statements.append("")
        
        sql_statements.append("-- Create index for committee queries")
        sql_statements.append("CREATE INDEX IF NOT EXISTS idx_hearings_committee_id ON hearings(committee_id);")
        sql_statements.append("")
        
        sql_script = "\n".join(sql_statements)
        
        print(f"✅ Created SQL script with {len(matches)} hearing updates")
        
        return sql_script
    
    def run_hearing_committee_matching(self) -> Dict:
        """Run the complete hearing-committee matching process"""
        print("🚀 Starting Hearing-Committee Matching")
        print("=" * 60)
        
        # Step 1: Load existing data
        if not self.load_existing_data():
            return {'error': 'Failed to load existing data'}
        
        # Step 2: Create committee patterns
        self.create_committee_patterns()
        
        # Step 3: Create matches
        matches = self.create_hearing_committee_matches()
        
        # Step 4: Validate matches
        validation = self.validate_matches(matches)
        
        # Step 5: Create SQL script
        sql_script = self.create_sql_update_script(matches)
        
        # Step 6: Generate report
        report = {
            'timestamp': datetime.now().isoformat(),
            'source': 'Pattern-Based Matching',
            'hearings_in_database': len(self.existing_hearings),
            'committees_in_database': len(self.existing_committees),
            'matches_created': len(matches),
            'validation': validation,
            'sql_script': sql_script,
            'matches': matches
        }
        
        print(f"\n📊 HEARING-COMMITTEE MATCHING RESULTS")
        print(f"Hearings in database: {report['hearings_in_database']}")
        print(f"Committees in database: {report['committees_in_database']}")
        print(f"Matches created: {report['matches_created']}")
        print(f"Match rate: {validation['match_rate']:.1f}%")
        
        return report

def main():
    """Main function to run hearing-committee matching"""
    try:
        matcher = HearingCommitteeMatcher()
        
        # Run matching
        results = matcher.run_hearing_committee_matching()
        
        # Save results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save main results
        results_file = f"hearing_committee_matches_{timestamp}.json"
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        # Save SQL script separately
        if 'sql_script' in results:
            sql_file = f"hearing_committee_updates_{timestamp}.sql"
            with open(sql_file, 'w') as f:
                f.write(results['sql_script'])
            print(f"💾 SQL script saved to: {sql_file}")
        
        print(f"💾 Results saved to: {results_file}")
        
        if 'error' not in results:
            print("\n🎯 NEXT STEPS:")
            print("1. Review hearing-committee matches for accuracy")
            print("2. Test SQL script in staging environment")
            print("3. Execute SQL script in production")
            print("4. Verify hearing committee filters work")
            print("5. Combine all relationship updates")
        else:
            print(f"\n❌ Error: {results['error']}")
            
    except Exception as e:
        print(f"❌ Fatal error: {e}")

if __name__ == "__main__":
    main()