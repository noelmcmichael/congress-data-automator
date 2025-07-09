#!/usr/bin/env python3
"""
Fix Deployment SQL
==================

Fix the constraint violations in the committee deployment SQL.
"""

import re
from datetime import datetime

def fix_deployment_sql():
    """Fix the deployment SQL to resolve constraint violations"""
    
    print("🔧 Fixing deployment SQL constraint violations")
    
    # Read the original file
    with open("phase3_expansion_deployment_20250709_104859.sql", "r") as f:
        content = f.read()
    
    print(f"✅ Read original SQL ({len(content)} characters)")
    
    # Fix 1: Replace full API URLs in congress_gov_id with just the committee codes
    # Pattern: https://api.congress.gov/v3/committee/{chamber}/{code}?format=json
    def extract_committee_code(match):
        url = match.group(1)
        # Extract the committee code from the URL
        code_match = re.search(r'/([^/]+)\?format=json', url)
        if code_match:
            return f"'{code_match.group(1)}'"
        else:
            return "'unknown'"
    
    # Replace congress_gov_id values (field 4 in INSERT statements)
    # This is complex due to the SQL structure, so let's do a targeted replacement
    
    # Pattern to match the INSERT VALUES section
    insert_pattern = r"INSERT INTO committees \([^)]+\) VALUES \(\s*'([^']+)',\s*'([^']+)',\s*'([^']*)',\s*'([^']+)',\s*([^,]+),\s*([^,]+),\s*'([^']+)',\s*([^)]+)\)"
    
    def fix_insert_values(match):
        name = match.group(1)
        chamber = match.group(2)
        committee_code = match.group(3)
        congress_gov_id_url = match.group(4)
        is_active = match.group(5)
        is_subcommittee = match.group(6)
        website_url = match.group(7)
        created_at = match.group(8)
        
        # Extract committee code from congress_gov_id URL
        code_match = re.search(r'/([^/]+)\?format=json', congress_gov_id_url)
        if code_match:
            congress_gov_id = code_match.group(1)
        else:
            congress_gov_id = committee_code or 'unknown'
        
        # Truncate congress_gov_id to 50 characters if needed
        congress_gov_id = congress_gov_id[:50]
        
        # Reconstruct the INSERT statement
        return f"""INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, is_active, 
    is_subcommittee, website, created_at
) VALUES (
    '{name}',
    '{chamber}',
    '{committee_code}',
    '{congress_gov_id}',
    {is_active},
    {is_subcommittee},
    '{website_url}',
    {created_at}
)"""
    
    # Apply the fix
    fixed_content = re.sub(insert_pattern, fix_insert_values, content, flags=re.MULTILINE)
    
    # If the complex regex didn't work, try a simpler approach
    if fixed_content == content:
        print("⚠️ Complex regex replacement didn't work, trying simpler approach")
        
        # Simple approach: replace all long URLs with just the committee codes
        def simple_url_replacement(match):
            full_url = match.group(0)
            # Extract committee code
            code_match = re.search(r'/([^/]+)\?format=json', full_url)
            if code_match:
                return f"'{code_match.group(1)}'"
            else:
                return "'unknown'"
        
        # Replace URLs that are too long for varchar(50)
        url_pattern = r"'https://api\.congress\.gov/v3/committee/[^']+'"
        fixed_content = re.sub(url_pattern, simple_url_replacement, content)
    
    changes_made = len(content) != len(fixed_content)
    
    if changes_made:
        print("✅ Applied constraint violation fixes")
        
        # Create new filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"phase3_expansion_deployment_fixed_{timestamp}.sql"
        
        # Add header
        header = f"""-- Phase 3: Committee Structure Expansion Deployment (FIXED)
-- Fixed: {datetime.now().isoformat()}
-- Purpose: Resolved varchar(50) constraint violations
-- Original: phase3_expansion_deployment_20250709_104859.sql
-- Changes: Truncated congress_gov_id URLs to committee codes
-- Total Committees: 815

"""
        
        # Write fixed content
        with open(output_file, "w") as f:
            f.write(header + fixed_content)
        
        print(f"✅ Created fixed deployment file: {output_file}")
        return output_file
    else:
        print("⚠️ No changes were made to the SQL")
        return None

def main():
    fixed_file = fix_deployment_sql()
    
    if fixed_file:
        print(f"\n🎯 SQL constraint violations fixed!")
        print(f"   Fixed file: {fixed_file}")
        print(f"   Ready for deployment execution")
    else:
        print(f"\n❌ Failed to fix SQL constraints")

if __name__ == "__main__":
    main()