#!/usr/bin/env python3
"""
Create a simplified database fix that works with the current schema.
"""

import json

def create_simple_fix():
    """Create a simplified database fix."""
    
    # Read the committee data
    with open('real_committees_20250706_175857.json', 'r') as f:
        committees_data = json.load(f)
    
    # Read the relationship data
    with open('real_relationships_20250706_175857.json', 'r') as f:
        relationships_data = json.load(f)
    
    sql_content = """-- Clear existing committee and relationship data
DELETE FROM committee_memberships;
DELETE FROM committees;

-- Insert real congressional committees
"""
    
    # Add committees
    for committee in committees_data:
        committee_type = "Subcommittee" if committee.get('is_subcommittee', False) else "Standing"
        jurisdiction = committee.get('jurisdiction', '').replace("'", "''")
        name = committee.get('name', '').replace("'", "''")
        
        sql_content += f"""INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee, committee_type) 
VALUES ({committee['id']}, '{name}', '{committee['chamber']}', '{jurisdiction}', {str(committee.get('is_active', True)).lower()}, {str(committee.get('is_subcommittee', False)).lower()}, '{committee_type}');
"""
    
    # Add relationships
    sql_content += "\n-- Insert committee memberships\n"
    for relationship in relationships_data:
        position = relationship.get('role', 'Member').replace("'", "''")
        sql_content += f"""INSERT INTO committee_memberships (member_id, committee_id, position, is_current) 
VALUES ({relationship['member_id']}, {relationship['committee_id']}, '{position}', true);
"""
    
    # Write the simple fix
    with open('simple_database_fix.sql', 'w') as f:
        f.write(sql_content)
    
    print("✅ Simple database fix created successfully!")
    print("Created: simple_database_fix.sql")

if __name__ == "__main__":
    create_simple_fix()