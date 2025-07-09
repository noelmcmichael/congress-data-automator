#!/usr/bin/env python3
"""
Add Committee Type Field
========================

Add committee_type field to the deployment SQL.
"""

import re
from datetime import datetime

def add_committee_type_field():
    """Add committee_type to the INSERT statements"""
    
    print("🔧 Adding committee_type field to deployment SQL")
    
    # Read the final file
    with open("phase3_expansion_deployment_final_20250709_112817.sql", "r") as f:
        content = f.read()
    
    print(f"✅ Read final SQL ({len(content)} characters)")
    
    # Pattern to match INSERT statements
    # Current: INSERT INTO committees (name, chamber, committee_code, congress_gov_id, is_active, is_subcommittee, website, created_at)
    # New: INSERT INTO committees (name, chamber, committee_code, congress_gov_id, committee_type, is_active, is_subcommittee, website, created_at)
    
    # Replace column list
    old_columns = "INSERT INTO committees (\n    name, chamber, committee_code, congress_gov_id, is_active, \n    is_subcommittee, website, created_at\n)"
    new_columns = "INSERT INTO committees (\n    name, chamber, committee_code, congress_gov_id, committee_type, is_active, \n    is_subcommittee, website, created_at\n)"
    
    fixed_content = content.replace(old_columns, new_columns)
    
    # Now we need to add committee_type values to each VALUES clause
    # Pattern: VALUES ('name', 'chamber', 'code', 'id', true/false, true/false, 'website', NOW())
    # Need to insert committee_type between congress_gov_id and is_active
    
    def add_committee_type_value(match):
        full_match = match.group(0)
        
        # Extract the values
        values_content = match.group(1)
        
        # Split by comma, respecting quotes
        values = []
        current_value = ""
        in_quotes = False
        paren_depth = 0
        
        for char in values_content:
            if char == "'" and not in_quotes:
                in_quotes = True
                current_value += char
            elif char == "'" and in_quotes:
                in_quotes = False
                current_value += char
            elif char == "(" and not in_quotes:
                paren_depth += 1
                current_value += char
            elif char == ")" and not in_quotes:
                paren_depth -= 1
                current_value += char
            elif char == "," and not in_quotes and paren_depth == 0:
                values.append(current_value.strip())
                current_value = ""
            else:
                current_value += char
        
        # Add the last value
        if current_value.strip():
            values.append(current_value.strip())
        
        if len(values) >= 6:
            # Insert committee_type based on is_subcommittee value
            is_subcommittee = values[5].strip()  # 6th value (0-indexed)
            
            if is_subcommittee.lower() == "true":
                committee_type = "'Subcommittee'"
            else:
                committee_type = "'Standing'"
            
            # Insert committee_type as 5th value (after congress_gov_id, before is_active)
            values.insert(4, committee_type)
            
            # Reconstruct the VALUES clause
            new_values = ",\n    ".join(values)
            return f") VALUES (\n    {new_values}\n)"
        else:
            # If we can't parse properly, return original
            return full_match
    
    # Apply the fix to VALUES clauses
    values_pattern = r"\) VALUES \(\s*(.*?)\s*\)\s*ON CONFLICT"
    fixed_content = re.sub(values_pattern, add_committee_type_value, fixed_content, flags=re.DOTALL)
    
    # Check if changes were made
    changes_made = len(content) != len(fixed_content)
    
    if changes_made:
        print("✅ Added committee_type field to INSERT statements")
        
        # Create final deployment file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"phase3_expansion_deployment_complete_{timestamp}.sql"
        
        # Add header
        header = f"""-- Phase 3: Committee Structure Expansion Deployment (COMPLETE)
-- Fixed: {datetime.now().isoformat()}
-- Purpose: Complete deployment with all required fields
-- Original: phase3_expansion_deployment_20250709_104859.sql
-- Changes: 
--   1. Truncated congress_gov_id URLs to committee codes
--   2. Fixed ON CONFLICT to use congress_gov_id unique constraint
--   3. Added committee_type field (Standing/Subcommittee)
-- Total Committees: 815

"""
        
        with open(output_file, "w") as f:
            f.write(header + fixed_content)
        
        print(f"✅ Created complete deployment file: {output_file}")
        return output_file
    else:
        print("⚠️ No changes were made to the SQL")
        return None

def main():
    complete_file = add_committee_type_field()
    
    if complete_file:
        print(f"\n🎯 Committee type field added!")
        print(f"   Complete file: {complete_file}")
        print(f"   Ready for final deployment")
    else:
        print(f"\n❌ Failed to add committee type field")

if __name__ == "__main__":
    main()