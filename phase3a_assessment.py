#!/usr/bin/env python3
"""
Phase 3A: Committee Structure Assessment
Analyze current committee database state and plan expansion strategy
"""

import os
import sys
import json
import time
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_db_connection():
    """Get database connection"""
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            port=os.getenv('DB_PORT', '5432')
        )
        return conn
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None

def analyze_current_committees():
    """Analyze current committee database state"""
    print("🔍 Analyzing Current Committee Database State")
    print("=" * 50)
    
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Basic committee count
        cursor.execute("SELECT COUNT(*) as total_committees FROM committees")
        total_committees = cursor.fetchone()['total_committees']
        print(f"📊 Total Committees: {total_committees}")
        
        # Committee by chamber
        cursor.execute("""
            SELECT chamber, COUNT(*) as count 
            FROM committees 
            GROUP BY chamber 
            ORDER BY chamber
        """)
        chamber_stats = cursor.fetchall()
        print("\n📋 Committees by Chamber:")
        for stat in chamber_stats:
            print(f"   {stat['chamber']}: {stat['count']}")
        
        # Subcommittee analysis
        cursor.execute("""
            SELECT 
                is_subcommittee,
                COUNT(*) as count
            FROM committees 
            GROUP BY is_subcommittee 
            ORDER BY is_subcommittee
        """)
        subcommittee_stats = cursor.fetchall()
        print("\n📋 Committee Types:")
        for stat in subcommittee_stats:
            committee_type = "Subcommittees" if stat['is_subcommittee'] else "Main Committees"
            print(f"   {committee_type}: {stat['count']}")
        
        # Active vs inactive
        cursor.execute("""
            SELECT 
                is_active,
                COUNT(*) as count
            FROM committees 
            GROUP BY is_active 
            ORDER BY is_active DESC
        """)
        active_stats = cursor.fetchall()
        print("\n📋 Committee Status:")
        for stat in active_stats:
            status = "Active" if stat['is_active'] else "Inactive"
            print(f"   {status}: {stat['count']}")
        
        # Committee membership analysis
        cursor.execute("""
            SELECT COUNT(*) as total_memberships 
            FROM committee_memberships
        """)
        total_memberships = cursor.fetchone()['total_memberships']
        print(f"\n👥 Total Committee Memberships: {total_memberships}")
        
        # Sample committees for structure analysis
        cursor.execute("""
            SELECT 
                name, chamber, committee_code, is_subcommittee, 
                parent_committee_id, is_active
            FROM committees 
            ORDER BY chamber, name 
            LIMIT 10
        """)
        sample_committees = cursor.fetchall()
        print("\n📋 Sample Committees:")
        for committee in sample_committees:
            subcommittee_mark = " (Sub)" if committee['is_subcommittee'] else ""
            active_mark = " ✅" if committee['is_active'] else " ❌"
            print(f"   {committee['chamber']}: {committee['name']}{subcommittee_mark}{active_mark}")
        
        cursor.close()
        conn.close()
        
        return {
            'total_committees': total_committees,
            'chamber_stats': chamber_stats,
            'subcommittee_stats': subcommittee_stats,
            'active_stats': active_stats,
            'total_memberships': total_memberships,
            'sample_committees': sample_committees
        }
        
    except Exception as e:
        print(f"❌ Database analysis failed: {e}")
        return None

def test_congress_api():
    """Test Congress.gov API committee endpoint"""
    print("\n🔍 Testing Congress.gov API Committee Endpoint")
    print("=" * 50)
    
    api_key = os.getenv('CONGRESS_API_KEY')
    if not api_key:
        print("❌ CONGRESS_API_KEY not found in environment")
        return None
    
    # Test committee endpoint
    url = "https://api.congress.gov/v3/committee"
    headers = {
        'X-API-Key': api_key,
        'Accept': 'application/json'
    }
    
    try:
        print(f"📡 Testing: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            committees = data.get('committees', [])
            
            print(f"✅ API Response: {response.status_code}")
            print(f"📊 Available Committees: {len(committees)}")
            
            # Analyze committee structure
            if committees:
                # Chamber analysis
                chamber_counts = {}
                for committee in committees[:50]:  # Sample first 50
                    chamber = committee.get('chamber', 'Unknown')
                    chamber_counts[chamber] = chamber_counts.get(chamber, 0) + 1
                
                print("\n📋 Chamber Distribution (sample):")
                for chamber, count in chamber_counts.items():
                    print(f"   {chamber}: {count}")
                
                # Show sample committees
                print("\n📋 Sample Committees from API:")
                for i, committee in enumerate(committees[:5]):
                    name = committee.get('name', 'Unknown')
                    chamber = committee.get('chamber', 'Unknown')
                    code = committee.get('systemCode', 'No code')
                    print(f"   {i+1}. {chamber}: {name} ({code})")
            
            return {
                'status': 'success',
                'committee_count': len(committees),
                'api_response': response.status_code,
                'sample_data': committees[:5] if committees else []
            }
            
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return None

def test_current_api_endpoint():
    """Test current /api/v1/committees endpoint"""
    print("\n🔍 Testing Current API Endpoint")
    print("=" * 50)
    
    try:
        # Test local/production endpoint
        url = "https://politicalequity.io/api/v1/committees?limit=10"
        print(f"📡 Testing: {url}")
        
        start_time = time.time()
        response = requests.get(url, timeout=10)
        duration = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Response: {response.status_code}")
            print(f"⏱️ Response Time: {duration:.3f}s")
            print(f"📊 Committees Returned: {len(data)}")
            
            # Show sample committee structure
            if data:
                print("\n📋 Sample Committee Structure:")
                sample = data[0]
                for key, value in sample.items():
                    print(f"   {key}: {value}")
            
            return {
                'status': 'success',
                'response_time': duration,
                'committee_count': len(data),
                'sample_data': data[:3] if data else []
            }
            
        else:
            print(f"❌ API Error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return None

def create_assessment_report():
    """Create comprehensive assessment report"""
    print("\n📊 Creating Assessment Report")
    print("=" * 50)
    
    # Run all assessments
    db_analysis = analyze_current_committees()
    congress_api_test = test_congress_api()
    current_api_test = test_current_api_endpoint()
    
    # Create report
    report = {
        'assessment_date': datetime.now().isoformat(),
        'database_analysis': db_analysis,
        'congress_api_test': congress_api_test,
        'current_api_test': current_api_test,
        'recommendations': []
    }
    
    # Generate recommendations
    if db_analysis:
        total_committees = db_analysis['total_committees']
        
        if total_committees < 50:
            report['recommendations'].append("LOW COMMITTEE COUNT: Need significant expansion")
        elif total_committees < 100:
            report['recommendations'].append("MODERATE COMMITTEE COUNT: Expansion recommended")
        else:
            report['recommendations'].append("ADEQUATE COMMITTEE COUNT: Review quality and completeness")
    
    if congress_api_test and congress_api_test['status'] == 'success':
        api_count = congress_api_test['committee_count']
        if api_count > 100:
            report['recommendations'].append("CONGRESS API VIABLE: Good source for committee expansion")
        else:
            report['recommendations'].append("CONGRESS API LIMITED: May need supplementary sources")
    
    if current_api_test and current_api_test['response_time'] > 1.0:
        report['recommendations'].append("PERFORMANCE CONCERN: API response time > 1s")
    
    # Save report
    report_file = f"phase3a_assessment_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📝 Assessment report saved: {report_file}")
    
    # Print recommendations
    print("\n🎯 Recommendations:")
    for rec in report['recommendations']:
        print(f"   • {rec}")
    
    return report

def main():
    """Main assessment function"""
    print("🚀 Phase 3A: Committee Structure Assessment")
    print("=" * 60)
    
    # Check prerequisites
    if not os.getenv('DATABASE_URL') and not os.getenv('DB_HOST'):
        print("❌ Database configuration not found")
        sys.exit(1)
    
    if not os.getenv('CONGRESS_API_KEY'):
        print("❌ CONGRESS_API_KEY not found")
        sys.exit(1)
    
    # Run assessment
    report = create_assessment_report()
    
    print("\n✅ Phase 3A Assessment Complete!")
    print("Ready to proceed with Phase 3B: Data Collection Framework")

if __name__ == "__main__":
    main()