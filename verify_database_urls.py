#!/usr/bin/env python3

"""
Verify Database URLs
Check if the committee URLs are actually in the database
"""

import psycopg2
from psycopg2.extras import RealDictCursor
import json

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

def verify_database_urls():
    """Verify that URLs are actually in the database"""
    conn = connect_to_database()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Check if URL columns exist
        cursor.execute("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'committees'
            AND column_name IN ('hearings_url', 'members_url', 'official_website_url', 'last_url_update')
            ORDER BY column_name;
        """)
        
        url_columns = cursor.fetchall()
        print("🔍 CHECKING URL COLUMNS IN DATABASE")
        print("=" * 60)
        print(f"URL columns found: {len(url_columns)}")
        for col in url_columns:
            print(f"  ✅ {col['column_name']}")
        
        # Check if committees have URLs
        cursor.execute("""
            SELECT id, name, chamber, hearings_url, members_url, official_website_url, last_url_update
            FROM committees
            WHERE (hearings_url IS NOT NULL OR members_url IS NOT NULL OR official_website_url IS NOT NULL)
            AND (is_subcommittee = FALSE OR is_subcommittee IS NULL)
            LIMIT 10;
        """)
        
        committees_with_urls = cursor.fetchall()
        print(f"\n📋 COMMITTEES WITH URLS: {len(committees_with_urls)}")
        print("=" * 60)
        
        if len(committees_with_urls) > 0:
            for committee in committees_with_urls:
                print(f"  {committee['chamber']:<6} {committee['name'][:50]:<50}")
                if committee['hearings_url']:
                    print(f"         Hearings: {committee['hearings_url']}")
                if committee['members_url']:
                    print(f"         Members:  {committee['members_url']}")
                if committee['official_website_url']:
                    print(f"         Website:  {committee['official_website_url']}")
                if committee['last_url_update']:
                    print(f"         Updated:  {committee['last_url_update']}")
                print()
        
        # Get total counts
        cursor.execute("""
            SELECT 
                COUNT(*) as total_committees,
                COUNT(CASE WHEN hearings_url IS NOT NULL THEN 1 END) as with_hearings,
                COUNT(CASE WHEN members_url IS NOT NULL THEN 1 END) as with_members,
                COUNT(CASE WHEN official_website_url IS NOT NULL THEN 1 END) as with_website
            FROM committees
            WHERE is_subcommittee = FALSE OR is_subcommittee IS NULL;
        """)
        
        stats = cursor.fetchone()
        print(f"📊 DATABASE STATISTICS:")
        print("=" * 60)
        print(f"  Total Main Committees: {stats['total_committees']}")
        print(f"  With Hearings URL: {stats['with_hearings']}")
        print(f"  With Members URL: {stats['with_members']}")
        print(f"  With Website URL: {stats['with_website']}")
        
        return len(committees_with_urls) > 0
        
    except Exception as e:
        print(f"Database verification error: {e}")
        return False
    
    finally:
        conn.close()

def main():
    """Main verification function"""
    print("🔍 VERIFYING DATABASE URLS")
    print("=" * 60)
    
    has_urls = verify_database_urls()
    
    if has_urls:
        print("\n✅ DATABASE VERIFICATION SUCCESSFUL")
        print("=" * 60)
        print("✅ URL columns exist in database")
        print("✅ Committees have URL data")
        print("❓ Issue may be with API serialization")
    else:
        print("\n❌ DATABASE VERIFICATION FAILED")
        print("=" * 60)
        print("❌ URL columns may not exist")
        print("❌ No committees have URL data")
        print("❓ Database update may have failed")

if __name__ == "__main__":
    main()