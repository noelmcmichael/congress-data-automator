#!/usr/bin/env python3
"""
Create Simple Deployment
========================

Create a simple, working committee deployment SQL without complex parsing.
"""

from datetime import datetime

def create_simple_deployment():
    """Create a simple deployment that just adds a few test committees"""
    
    print("🔧 Creating simple test deployment")
    
    # Simple deployment to test if our approach works
    sql_content = """-- Simple Committee Test Deployment
-- Testing committee insertion approach

BEGIN;

-- Test Committee 1: Joint Economic Committee
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type, 
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Joint Economic Committee',
    'Joint',
    'jhje00',
    'jhje00',
    'Standing',
    true,
    false,
    'https://www.jec.senate.gov/',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;

-- Test Committee 2: House Committee on Agriculture
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'House Committee on Agriculture',
    'House',
    'hsag00',
    'hsag00',
    'Standing',
    true,
    false,
    'https://agriculture.house.gov/',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;

-- Test Committee 3: Senate Committee on Agriculture
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    'Senate Committee on Agriculture, Nutrition, and Forestry',
    'Senate',
    'ssaf00',
    'ssaf00',
    'Standing',
    true,
    false,
    'https://www.agriculture.senate.gov/',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;

COMMIT;
"""
    
    # Write test deployment
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"committee_expansion_test_{timestamp}.sql"
    
    with open(output_file, "w") as f:
        f.write(sql_content)
    
    print(f"✅ Created test deployment: {output_file}")
    return output_file

def main():
    test_file = create_simple_deployment()
    print(f"\n🎯 Test deployment created: {test_file}")
    print("   This will test if our deployment approach works")
    print("   If successful, we can create the full 815-committee deployment")

if __name__ == "__main__":
    main()