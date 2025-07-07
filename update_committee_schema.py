#!/usr/bin/env python3

"""
Step 2: Database Schema Updates
Add required URL columns to committees table
"""

import psycopg2
from psycopg2.extras import RealDictCursor
import os
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

def backup_table_structure():
    """Create backup of current table structure"""
    conn = connect_to_database()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Get current table structure
        cursor.execute("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_name = 'committees'
            ORDER BY ordinal_position;
        """)
        
        columns = cursor.fetchall()
        
        # Save backup
        backup_info = {
            "timestamp": datetime.now().isoformat(),
            "table_name": "committees",
            "action": "pre_schema_update_backup",
            "columns": [dict(col) for col in columns]
        }
        
        with open(f'committee_schema_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json', 'w') as f:
            import json
            json.dump(backup_info, f, indent=2, default=str)
        
        print("✅ Schema backup created successfully")
        return True
        
    except Exception as e:
        print(f"Backup error: {e}")
        return False
    
    finally:
        conn.close()

def update_schema():
    """Add new URL columns to committees table"""
    conn = connect_to_database()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        # Add new columns
        new_columns = [
            ("hearings_url", "VARCHAR(255)", "Official hearings page URL"),
            ("members_url", "VARCHAR(255)", "Official members page URL"),
            ("official_website_url", "VARCHAR(255)", "Main committee website URL"),
            ("last_url_update", "TIMESTAMP", "Last time URLs were updated")
        ]
        
        print("🔧 ADDING NEW COLUMNS TO COMMITTEES TABLE:")
        print("=" * 60)
        
        for col_name, col_type, description in new_columns:
            try:
                # Check if column already exists
                cursor.execute("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = 'committees' AND column_name = %s;
                """, (col_name,))
                
                if cursor.fetchone():
                    print(f"  {col_name:<20} ALREADY EXISTS")
                else:
                    # Add the column
                    cursor.execute(f"""
                        ALTER TABLE committees 
                        ADD COLUMN {col_name} {col_type};
                    """)
                    
                    # Add comment for documentation
                    cursor.execute(f"""
                        COMMENT ON COLUMN committees.{col_name} IS %s;
                    """, (description,))
                    
                    print(f"  {col_name:<20} ADDED SUCCESSFULLY")
                    
            except Exception as e:
                print(f"  {col_name:<20} ERROR: {e}")
                return False
        
        # Commit the changes
        conn.commit()
        print("\n✅ SCHEMA UPDATE COMPLETED SUCCESSFULLY")
        
        # Verify the changes
        cursor.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = 'committees'
            AND column_name IN ('hearings_url', 'members_url', 'official_website_url', 'last_url_update')
            ORDER BY column_name;
        """)
        
        new_cols = cursor.fetchall()
        print("\n📋 VERIFICATION - NEW COLUMNS ADDED:")
        print("=" * 60)
        for col in new_cols:
            print(f"  {col[0]:<25} {col[1]:<15} {'NULL' if col[2] == 'YES' else 'NOT NULL'}")
        
        return True
        
    except Exception as e:
        print(f"Schema update error: {e}")
        conn.rollback()
        return False
    
    finally:
        conn.close()

def main():
    """Main execution function"""
    print("🚀 STARTING COMMITTEE SCHEMA UPDATE")
    print("=" * 60)
    
    # Step 1: Create backup
    print("\n1. Creating schema backup...")
    if not backup_table_structure():
        print("❌ Backup failed. Aborting.")
        return
    
    # Step 2: Update schema
    print("\n2. Updating schema...")
    if not update_schema():
        print("❌ Schema update failed.")
        return
    
    print("\n🎉 COMMITTEE SCHEMA UPDATE COMPLETED")
    print("=" * 60)
    print("✅ New columns added:")
    print("  - hearings_url: Official hearings page URL")
    print("  - members_url: Official members page URL") 
    print("  - official_website_url: Main committee website URL")
    print("  - last_url_update: Last time URLs were updated")
    print("\n📋 Ready for Step 3: URL Mapping System")

if __name__ == "__main__":
    main()