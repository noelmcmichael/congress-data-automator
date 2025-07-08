#!/usr/bin/env python3
"""
Fix datetime format in database - remove 'Z' suffix and standardize format.
"""

import sqlite3
from datetime import datetime
import os

def fix_datetime_format():
    """Fix datetime format in all tables."""
    db_path = "test.db"
    
    if not os.path.exists(db_path):
        print(f"Database not found: {db_path}")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    for (table_name,) in tables:
        print(f"Processing table: {table_name}")
        
        # Get table schema
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        # Find datetime columns
        datetime_columns = []
        for column in columns:
            column_name = column[1]
            if column_name.endswith('_at') or column_name in ['created_at', 'updated_at', 'date_time']:
                datetime_columns.append(column_name)
        
        if datetime_columns:
            print(f"  Found datetime columns: {datetime_columns}")
            
            # Fix datetime format in each column
            for column_name in datetime_columns:
                # Update values that end with 'Z' to remove the 'Z'
                update_query = f"""
                UPDATE {table_name} 
                SET {column_name} = REPLACE({column_name}, 'Z', '')
                WHERE {column_name} LIKE '%Z'
                """
                cursor.execute(update_query)
                affected_rows = cursor.rowcount
                print(f"  Updated {affected_rows} rows in {table_name}.{column_name}")
    
    conn.commit()
    conn.close()
    
    print("✅ DateTime format fix completed!")

if __name__ == "__main__":
    fix_datetime_format()