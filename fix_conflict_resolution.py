#!/usr/bin/env python3
"""
Fix Conflict Resolution
=======================

Update the SQL to use the correct unique constraint.
"""

import re
from datetime import datetime

def fix_conflict_resolution():
    """Fix the ON CONFLICT clause to use the correct constraint"""
    
    print("🔧 Fixing ON CONFLICT clause")
    
    # Read the fixed file
    with open("phase3_expansion_deployment_fixed_20250709_112609.sql", "r") as f:
        content = f.read()
    
    print(f"✅ Read fixed SQL ({len(content)} characters)")
    
    # Replace ON CONFLICT (name, chamber) with ON CONFLICT (congress_gov_id)
    # But first, we need to ensure congress_gov_id values are unique
    
    # Option 1: Use ON CONFLICT (congress_gov_id) DO NOTHING
    fixed_content = content.replace(
        "ON CONFLICT (name, chamber) DO NOTHING;",
        "ON CONFLICT (congress_gov_id) DO NOTHING;"
    )
    
    # Count replacements
    original_conflicts = content.count("ON CONFLICT (name, chamber) DO NOTHING;")
    new_conflicts = fixed_content.count("ON CONFLICT (congress_gov_id) DO NOTHING;")
    
    print(f"✅ Updated {new_conflicts} conflict resolution clauses")
    
    if new_conflicts == original_conflicts and new_conflicts > 0:
        # Create final deployment file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"phase3_expansion_deployment_final_{timestamp}.sql"
        
        # Add header
        header = f"""-- Phase 3: Committee Structure Expansion Deployment (FINAL)
-- Fixed: {datetime.now().isoformat()}
-- Purpose: Final deployment with correct constraints and conflict resolution
-- Original: phase3_expansion_deployment_20250709_104859.sql
-- Changes: 
--   1. Truncated congress_gov_id URLs to committee codes
--   2. Fixed ON CONFLICT to use congress_gov_id unique constraint
-- Total Committees: 815

"""
        
        with open(output_file, "w") as f:
            f.write(header + fixed_content)
        
        print(f"✅ Created final deployment file: {output_file}")
        return output_file
    else:
        print("❌ Failed to fix conflict resolution")
        return None

def main():
    fixed_file = fix_conflict_resolution()
    
    if fixed_file:
        print(f"\n🎯 Conflict resolution fixed!")
        print(f"   Final file: {fixed_file}")
        print(f"   Ready for final deployment")
    else:
        print(f"\n❌ Failed to fix conflict resolution")

if __name__ == "__main__":
    main()