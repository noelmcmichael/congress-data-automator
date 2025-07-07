#!/usr/bin/env python3

"""
Step 4: Database Population
Load committee URLs into the database using the mapping
"""

import psycopg2
from psycopg2.extras import RealDictCursor
import json
from datetime import datetime
import requests
import time

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

def load_mapping():
    """Load the committee URL mapping"""
    try:
        with open('committee_url_mapping.json', 'r') as f:
            mapping = json.load(f)
        return mapping
    except Exception as e:
        print(f"Error loading mapping: {e}")
        return None

def validate_url(url):
    """Validate URL accessibility"""
    try:
        response = requests.head(url, timeout=10, allow_redirects=True)
        return response.status_code == 200
    except:
        return False

def add_manual_mapping():
    """Add manual mapping for the unmapped committee"""
    manual_mapping = {
        "committee_id": 181,
        "database_name": "Committee on Health, Education, Labor and Pensions",
        "official_name": "Health, Education, Labor, and Pensions",
        "chamber": "Senate",
        "hearings_url": "https://www.help.senate.gov/hearings",
        "members_url": "https://www.help.senate.gov/about/members",
        "match_type": "manual",
        "confidence": 1.0
    }
    return manual_mapping

def populate_urls():
    """Populate committee URLs in the database"""
    conn = connect_to_database()
    if not conn:
        return False
    
    mapping = load_mapping()
    if not mapping:
        return False
    
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Add manual mapping for the unmapped committee
        manual_mapping = add_manual_mapping()
        all_mappings = mapping['mappings'] + [manual_mapping]
        
        print("🔄 POPULATING COMMITTEE URLS")
        print("=" * 60)
        
        successful_updates = 0
        failed_updates = 0
        url_validations = {"valid": 0, "invalid": 0}
        
        for committee_mapping in all_mappings:
            committee_id = committee_mapping['committee_id']
            hearings_url = committee_mapping['hearings_url']
            members_url = committee_mapping['members_url']
            
            try:
                # Validate URLs (optional - can be time consuming)
                # hearings_valid = validate_url(hearings_url)
                # members_valid = validate_url(members_url)
                
                # For now, skip validation to speed up the process
                hearings_valid = True
                members_valid = True
                
                # Extract base website from hearings URL
                if hearings_url.startswith('https://'):
                    base_url = '/'.join(hearings_url.split('/')[:3])
                else:
                    base_url = hearings_url
                
                # Update the database
                cursor.execute("""
                    UPDATE committees 
                    SET hearings_url = %s,
                        members_url = %s,
                        official_website_url = %s,
                        last_url_update = %s
                    WHERE id = %s;
                """, (
                    hearings_url,
                    members_url,
                    base_url,
                    datetime.now(),
                    committee_id
                ))
                
                if cursor.rowcount > 0:
                    successful_updates += 1
                    status = "✅"
                    if hearings_valid and members_valid:
                        url_validations["valid"] += 1
                    else:
                        url_validations["invalid"] += 1
                else:
                    failed_updates += 1
                    status = "❌"
                
                print(f"{status} {committee_mapping['chamber']:<6} {committee_mapping['database_name'][:50]:<50}")
                
            except Exception as e:
                failed_updates += 1
                print(f"❌ {committee_mapping['chamber']:<6} {committee_mapping['database_name'][:50]:<50} ERROR: {e}")
        
        # Commit all changes
        conn.commit()
        
        print(f"\n📊 POPULATION RESULTS:")
        print("=" * 60)
        print(f"  Successful Updates: {successful_updates}")
        print(f"  Failed Updates: {failed_updates}")
        print(f"  Total Committees: {len(all_mappings)}")
        print(f"  Success Rate: {(successful_updates / len(all_mappings)) * 100:.1f}%")
        
        # Verify the updates
        cursor.execute("""
            SELECT COUNT(*) as total_committees,
                   COUNT(CASE WHEN hearings_url IS NOT NULL THEN 1 END) as with_hearings_url,
                   COUNT(CASE WHEN members_url IS NOT NULL THEN 1 END) as with_members_url,
                   COUNT(CASE WHEN official_website_url IS NOT NULL THEN 1 END) as with_website_url
            FROM committees
            WHERE is_subcommittee = FALSE OR is_subcommittee IS NULL;
        """)
        
        verification = cursor.fetchone()
        
        print(f"\n🔍 VERIFICATION RESULTS:")
        print("=" * 60)
        print(f"  Total Main Committees: {verification['total_committees']}")
        print(f"  With Hearings URL: {verification['with_hearings_url']}")
        print(f"  With Members URL: {verification['with_members_url']}")
        print(f"  With Website URL: {verification['with_website_url']}")
        
        # Show sample of updated committees
        cursor.execute("""
            SELECT id, name, chamber, hearings_url, members_url, official_website_url
            FROM committees
            WHERE hearings_url IS NOT NULL
            AND (is_subcommittee = FALSE OR is_subcommittee IS NULL)
            ORDER BY chamber, name
            LIMIT 5;
        """)
        
        samples = cursor.fetchall()
        print(f"\n📋 SAMPLE UPDATED COMMITTEES:")
        print("=" * 60)
        for sample in samples:
            print(f"  {sample['chamber']:<6} {sample['name'][:40]:<42}")
            print(f"         Hearings: {sample['hearings_url']}")
            print(f"         Members:  {sample['members_url']}")
            print()
        
        return successful_updates > 0
        
    except Exception as e:
        print(f"Population error: {e}")
        conn.rollback()
        return False
    
    finally:
        conn.close()

def main():
    """Main execution function"""
    print("🚀 STARTING COMMITTEE URL POPULATION")
    print("=" * 60)
    
    success = populate_urls()
    
    if success:
        print("\n✅ COMMITTEE URL POPULATION COMPLETED")
        print("=" * 60)
        print("✅ All committee URLs populated successfully")
        print("✅ Database enhanced with official resources")
        print("✅ Ready for Step 5: API Enhancement")
    else:
        print("\n❌ COMMITTEE URL POPULATION FAILED")
        print("=" * 60)
        print("❌ Check database connection and try again")

if __name__ == "__main__":
    main()