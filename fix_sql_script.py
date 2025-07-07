#!/usr/bin/env python3
"""
Fix the SQL script to include the committee_type field.
"""

import re

def fix_sql_script():
    """Fix the SQL script to include committee_type field."""
    
    # Read the original SQL file
    with open('fix_congressional_database_20250706_180216.sql', 'r') as f:
        sql_content = f.read()
    
    # Pattern to match INSERT statements
    pattern = r"INSERT INTO committees \(id, name, chamber, jurisdiction, is_active, is_subcommittee\)"
    replacement = "INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type)"
    
    # Replace the INSERT statement structure
    updated_sql = re.sub(pattern, replacement, sql_content)
    
    # Pattern to match VALUES clauses and add 'Standing' for committee_type
    values_pattern = r"VALUES \((\d+), '([^']+)', '([^']+)', '([^']*)', (true|false), (true|false)\)"
    
    def replace_values(match):
        id_val = match.group(1)
        name = match.group(2)
        chamber = match.group(3)
        jurisdiction = match.group(4)
        is_active = match.group(5)
        is_subcommittee = match.group(6)
        
        # Determine committee type based on is_subcommittee
        if is_subcommittee == "true":
            committee_type = "Subcommittee"
        else:
            committee_type = "Standing"
        
        return f"VALUES ({id_val}, '{name}', '{chamber}', '{jurisdiction}', {is_active}, {is_subcommittee}, '{committee_type}')"
    
    # Replace all VALUES clauses
    updated_sql = re.sub(values_pattern, replace_values, updated_sql)
    
    # Write the updated SQL file
    with open('fix_congressional_database_20250706_180216_updated.sql', 'w') as f:
        f.write(updated_sql)
    
    print("✅ SQL script updated successfully!")
    print("Created: fix_congressional_database_20250706_180216_updated.sql")

if __name__ == "__main__":
    fix_sql_script()