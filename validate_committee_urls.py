#!/usr/bin/env python3

"""
Validate Committee URLs
Check and fix broken committee URLs identified during scraping
"""

import requests
import psycopg2
from psycopg2.extras import RealDictCursor
import json
import time
from datetime import datetime

def connect_to_database():
    """Connect to Cloud SQL database via proxy"""
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5433,
            database="congress_data",
            user="postgres",
            password="mDf3S9ZnBpQqJvGsY1"
        )
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

def validate_url(url, timeout=10):
    """Validate a single URL"""
    try:
        response = requests.head(url, timeout=timeout, allow_redirects=True)
        return {
            'status_code': response.status_code,
            'final_url': response.url,
            'valid': response.status_code == 200,
            'error': None
        }
    except requests.exceptions.RequestException as e:
        return {
            'status_code': None,
            'final_url': None,
            'valid': False,
            'error': str(e)
        }

def get_committee_urls():
    """Get all committee URLs from database"""
    conn = connect_to_database()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT id, name, chamber, hearings_url, members_url, official_website_url
            FROM committees
            WHERE (hearings_url IS NOT NULL OR members_url IS NOT NULL OR official_website_url IS NOT NULL)
            AND (is_subcommittee = FALSE OR is_subcommittee IS NULL)
            ORDER BY chamber, name;
        """)
        
        committees = cursor.fetchall()
        conn.close()
        return committees
        
    except Exception as e:
        print(f"Error fetching committee URLs: {e}")
        conn.close()
        return []

def validate_all_urls():
    """Validate all committee URLs"""
    print("🔍 VALIDATING COMMITTEE URLS")
    print("=" * 60)
    
    committees = get_committee_urls()
    if not committees:
        print("❌ No committees with URLs found")
        return []
    
    print(f"📋 Found {len(committees)} committees with URLs")
    
    validation_results = []
    
    for i, committee in enumerate(committees, 1):
        print(f"\n[{i}/{len(committees)}] {committee['chamber']} - {committee['name']}")
        
        committee_result = {
            'id': committee['id'],
            'name': committee['name'],
            'chamber': committee['chamber'],
            'urls': {}
        }
        
        # Test each URL type
        url_types = [
            ('hearings_url', committee['hearings_url']),
            ('members_url', committee['members_url']),
            ('official_website_url', committee['official_website_url'])
        ]
        
        for url_type, url in url_types:
            if url:
                print(f"   Testing {url_type}...")
                result = validate_url(url)
                committee_result['urls'][url_type] = {
                    'url': url,
                    'result': result
                }
                
                if result['valid']:
                    print(f"     ✅ {result['status_code']} - OK")
                else:
                    print(f"     ❌ {result['status_code']} - {result['error']}")
                
                # Be respectful with rate limiting
                time.sleep(1)
        
        validation_results.append(committee_result)
    
    return validation_results

def analyze_validation_results(results):
    """Analyze validation results and identify issues"""
    print("\n📊 VALIDATION ANALYSIS")
    print("=" * 60)
    
    total_urls = 0
    valid_urls = 0
    broken_urls = []
    
    for committee in results:
        for url_type, url_data in committee['urls'].items():
            total_urls += 1
            if url_data['result']['valid']:
                valid_urls += 1
            else:
                broken_urls.append({
                    'committee': committee['name'],
                    'chamber': committee['chamber'],
                    'url_type': url_type,
                    'url': url_data['url'],
                    'error': url_data['result']['error'],
                    'status_code': url_data['result']['status_code']
                })
    
    print(f"Total URLs tested: {total_urls}")
    print(f"Valid URLs: {valid_urls}")
    print(f"Broken URLs: {len(broken_urls)}")
    print(f"Success rate: {(valid_urls/total_urls)*100:.1f}%")
    
    if broken_urls:
        print(f"\n❌ BROKEN URLS ({len(broken_urls)}):")
        print("-" * 60)
        
        for broken in broken_urls:
            print(f"• {broken['chamber']} - {broken['committee']}")
            print(f"  Type: {broken['url_type']}")
            print(f"  URL: {broken['url']}")
            print(f"  Error: {broken['status_code']} - {broken['error']}")
            print()
    
    return broken_urls

def suggest_url_fixes(broken_urls):
    """Suggest fixes for broken URLs"""
    print("🔧 SUGGESTED URL FIXES")
    print("=" * 60)
    
    fixes = []
    
    for broken in broken_urls:
        committee_name = broken['committee']
        chamber = broken['chamber']
        url_type = broken['url_type']
        current_url = broken['url']
        
        # Common fix patterns for House committees
        if chamber == 'House' and '404' in str(broken['status_code']) or 'Not Found' in str(broken['error']):
            committee_slug = committee_name.lower().replace(' ', '').replace('committee on ', '').replace('committee', '')
            
            if url_type == 'hearings_url':
                suggested_url = f"https://{committee_slug}.house.gov/calendar"
            elif url_type == 'members_url':
                suggested_url = f"https://{committee_slug}.house.gov/about/members"
            elif url_type == 'official_website_url':
                suggested_url = f"https://{committee_slug}.house.gov"
            else:
                suggested_url = None
            
            if suggested_url:
                fixes.append({
                    'committee_id': broken.get('committee_id'),
                    'committee': committee_name,
                    'chamber': chamber,
                    'url_type': url_type,
                    'current_url': current_url,
                    'suggested_url': suggested_url,
                    'reason': 'Standard House committee URL pattern'
                })
        
        # Common fix patterns for Senate committees
        elif chamber == 'Senate' and '404' in str(broken['status_code']):
            committee_slug = committee_name.lower().replace('committee on ', '').replace(' ', '')
            
            if url_type == 'hearings_url':
                suggested_url = f"https://www.{committee_slug}.senate.gov/hearings"
            elif url_type == 'members_url':
                suggested_url = f"https://www.{committee_slug}.senate.gov/about/members"
            elif url_type == 'official_website_url':
                suggested_url = f"https://www.{committee_slug}.senate.gov"
            else:
                suggested_url = None
            
            if suggested_url:
                fixes.append({
                    'committee_id': broken.get('committee_id'),
                    'committee': committee_name,
                    'chamber': chamber,
                    'url_type': url_type,
                    'current_url': current_url,
                    'suggested_url': suggested_url,
                    'reason': 'Standard Senate committee URL pattern'
                })
    
    if fixes:
        print(f"📋 Found {len(fixes)} potential fixes:")
        print("-" * 60)
        
        for fix in fixes:
            print(f"• {fix['chamber']} - {fix['committee']}")
            print(f"  Type: {fix['url_type']}")
            print(f"  Current: {fix['current_url']}")
            print(f"  Suggested: {fix['suggested_url']}")
            print(f"  Reason: {fix['reason']}")
            print()
    else:
        print("No automatic fixes available")
    
    return fixes

def save_validation_report(results, broken_urls, fixes):
    """Save validation report to file"""
    report = {
        'timestamp': datetime.now().isoformat(),
        'summary': {
            'total_committees': len(results),
            'total_urls': sum(len(c['urls']) for c in results),
            'valid_urls': sum(sum(1 for u in c['urls'].values() if u['result']['valid']) for c in results),
            'broken_urls': len(broken_urls),
            'suggested_fixes': len(fixes)
        },
        'results': results,
        'broken_urls': broken_urls,
        'suggested_fixes': fixes
    }
    
    filename = f"url_validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(filename, 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    print(f"📄 Validation report saved: {filename}")
    return filename

def main():
    """Main validation function"""
    print("🔍 COMMITTEE URL VALIDATION")
    print("=" * 60)
    
    # Step 1: Validate all URLs
    results = validate_all_urls()
    
    if not results:
        print("❌ No validation results")
        return False
    
    # Step 2: Analyze results
    broken_urls = analyze_validation_results(results)
    
    # Step 3: Suggest fixes
    fixes = suggest_url_fixes(broken_urls)
    
    # Step 4: Save report
    report_file = save_validation_report(results, broken_urls, fixes)
    
    # Step 5: Summary
    total_urls = sum(len(c['urls']) for c in results)
    valid_urls = total_urls - len(broken_urls)
    success_rate = (valid_urls / total_urls) * 100 if total_urls > 0 else 0
    
    print(f"\n📊 VALIDATION SUMMARY")
    print("=" * 60)
    print(f"✅ Committees validated: {len(results)}")
    print(f"✅ URLs tested: {total_urls}")
    print(f"✅ Success rate: {success_rate:.1f}%")
    print(f"📄 Report saved: {report_file}")
    
    if len(broken_urls) == 0:
        print("\n🎉 ALL URLS WORKING!")
        print("✅ No broken URLs found")
        print("✅ Committee resources fully operational")
        return True
    else:
        print(f"\n⚠️ ISSUES FOUND: {len(broken_urls)} broken URLs")
        print("📋 Suggested fixes available in report")
        print("🔧 Manual review and fixes recommended")
        return False

if __name__ == "__main__":
    success = main()