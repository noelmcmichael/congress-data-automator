#!/usr/bin/env python3
"""
Create Committee Expansion Deployment SQL
========================================

Modify the existing deployment SQL to allow new committee insertions.
"""

import re
from datetime import datetime

def create_expansion_deployment():
    """Create modified deployment SQL for committee expansion"""
    
    print("📝 Creating Committee Expansion Deployment SQL")
    print("=" * 50)
    
    # Read the original deployment file
    with open("phase3_full_deployment_20250709_091846.sql", "r") as f:
        original_sql = f.read()
    
    print(f"✅ Read original deployment SQL ({len(original_sql)} characters)")
    
    # Create the modified version by changing conflict resolution
    # From: ON CONFLICT (name, chamber) DO UPDATE SET ...
    # To: ON CONFLICT (name, chamber) DO NOTHING;
    
    # Pattern to match the entire ON CONFLICT clause with all its content
    conflict_pattern = r'ON CONFLICT \(name, chamber\) DO UPDATE SET[^;]*;'
    
    # Replace with simple DO NOTHING
    modified_sql = re.sub(
        conflict_pattern,
        'ON CONFLICT (name, chamber) DO NOTHING;',
        original_sql,
        flags=re.MULTILINE | re.DOTALL
    )
    
    # Count the number of replacements made
    original_conflicts = len(re.findall(conflict_pattern, original_sql, flags=re.MULTILINE | re.DOTALL))
    
    print(f"✅ Modified {original_conflicts} conflict resolution clauses")
    
    # Add header with modification info
    timestamp = datetime.now().isoformat()
    header = f"""-- Phase 3: Committee Structure Expansion Deployment
-- Modified: {timestamp}
-- Purpose: Allow insertion of new committees (changed DO UPDATE to DO NOTHING)
-- Original: phase3_full_deployment_20250709_091846.sql
-- Total Committees: 815

"""
    
    # Add header to the beginning (after the original header)
    lines = modified_sql.split('\n')
    # Find the end of the original header
    header_end = 0
    for i, line in enumerate(lines):
        if line.strip().startswith('BEGIN;'):
            header_end = i
            break
    
    # Insert our header before BEGIN;
    lines.insert(header_end, header)
    modified_sql = '\n'.join(lines)
    
    # Write the modified deployment file
    output_filename = f"phase3_expansion_deployment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
    with open(output_filename, "w") as f:
        f.write(modified_sql)
    
    print(f"✅ Created expansion deployment: {output_filename}")
    
    # Validate the modification by checking a sample
    sample_start = modified_sql.find("ON CONFLICT (name, chamber) DO NOTHING;")
    if sample_start >= 0:
        print("✅ Conflict resolution successfully modified")
        
        # Show sample of the modification
        sample_context = modified_sql[max(0, sample_start-100):sample_start+100]
        print("\nSample modification:")
        print("-" * 30)
        for line in sample_context.split('\n'):
            if 'ON CONFLICT' in line:
                print(f"  {line.strip()}")
        print("-" * 30)
    else:
        print("❌ Conflict resolution modification failed")
        return None
    
    return output_filename

def main():
    try:
        output_file = create_expansion_deployment()
        if output_file:
            print(f"\n🎯 Ready for Phase E3: Execute expansion deployment")
            print(f"   File: {output_file}")
            print("   Command: Execute via gcloud sql connect")
        else:
            print("\n❌ Failed to create expansion deployment")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()