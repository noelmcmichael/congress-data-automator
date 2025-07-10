#!/usr/bin/env python3
"""
Fix the committees endpoint by replacing ORM with raw SQL
"""

def create_fixed_committees_endpoint():
    """
    Create a fixed version of the committees endpoint using raw SQL
    """
    
    fixed_endpoint_code = '''
@router.get("/committees", response_model=List[dict])
async def get_committees_fixed(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(50, ge=1, le=200, description="Items per page"),
    search: Optional[str] = Query(None, description="Search by committee name"),
    chamber: Optional[str] = Query(None, description="Filter by chamber (House/Senate/Joint)"),
    active_only: bool = Query(True, description="Only return active committees"),
    sort_by: Optional[str] = Query("name", description="Sort by field (name, chamber)"),
    sort_order: Optional[str] = Query("asc", description="Sort order (asc/desc)"),
    db: Session = Depends(get_db)
):
    """
    Retrieve congressional committees with search, filtering, and sorting
    FIXED VERSION: Uses raw SQL to avoid ORM issues
    """
    from sqlalchemy import text
    
    # Build WHERE clause
    where_conditions = []
    params = {}
    
    if search:
        search_term = f"%{search}%"
        where_conditions.append("name ILIKE :search")
        params["search"] = search_term
    
    if chamber:
        # Use exact case-sensitive matching
        where_conditions.append("chamber = :chamber")
        params["chamber"] = chamber
    
    if active_only:
        where_conditions.append("is_active = :active_only")
        params["active_only"] = True
    
    # Build ORDER BY clause
    order_by = "name"
    if sort_by in ["name", "chamber", "committee_type", "created_at"]:
        order_by = sort_by
    
    if sort_order.lower() == "desc":
        order_by += " DESC"
    else:
        order_by += " ASC"
    
    # Build complete SQL
    where_clause = " AND ".join(where_conditions) if where_conditions else "1=1"
    offset = (page - 1) * limit
    
    sql = text(f"""
        SELECT id, congress_gov_id, committee_code, name, chamber, committee_type,
               parent_committee_id, is_subcommittee, description, jurisdiction,
               chair_member_id, ranking_member_id, phone, email, website, 
               office_location, is_active, congress_session, created_at, 
               updated_at, last_scraped_at, hearings_url, members_url, 
               official_website_url, last_url_update
        FROM committees 
        WHERE {where_clause}
        ORDER BY {order_by}
        LIMIT :limit OFFSET :offset
    """)
    
    params.update({"limit": limit, "offset": offset})
    
    # Execute the query
    result = db.execute(sql, params).fetchall()
    
    # Convert to response format
    committees_response = []
    for row in result:
        committee_data = {
            "id": row[0],
            "congress_gov_id": row[1],
            "committee_code": row[2],
            "name": row[3],
            "chamber": row[4],
            "committee_type": row[5],
            "parent_committee_id": row[6],
            "is_subcommittee": row[7],
            "description": row[8],
            "jurisdiction": row[9],
            "chair_member_id": row[10],
            "ranking_member_id": row[11],
            "phone": row[12],
            "email": row[13],
            "website": row[14],
            "office_location": row[15],
            "is_active": row[16],
            "congress_session": row[17],
            "created_at": row[18],
            "updated_at": row[19],
            "last_scraped_at": row[20],
            "hearings_url": row[21],
            "members_url": row[22],
            "official_website_url": row[23],
            "last_url_update": row[24]
        }
        committees_response.append(committee_data)
    
    return committees_response
'''
    
    return fixed_endpoint_code

def apply_fix():
    """
    Apply the fix to the data_retrieval.py file
    """
    import os
    
    # Read the current file
    file_path = "/Users/noelmcmichael/Workspace/congress_data_automator/backend/app/api/v1/data_retrieval.py"
    
    print("🔧 Applying fix to committees endpoint...")
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Find the old get_committees function and replace it
    old_function_start = '@router.get("/committees", response_model=List[CommitteeResponse])'
    new_function_start = '@router.get("/committees", response_model=List[dict])'
    
    # First, let's find where the function starts and ends
    start_index = content.find(old_function_start)
    if start_index == -1:
        print("❌ Could not find committees endpoint to replace")
        return False
    
    # Find the next @router declaration (end of function)
    next_function_start = content.find('@router.get', start_index + 1)
    if next_function_start == -1:
        # If no next function, find the end of the file
        end_index = len(content)
    else:
        end_index = next_function_start
    
    # Replace the function
    old_function = content[start_index:end_index]
    new_function = create_fixed_committees_endpoint()
    
    # Replace the content
    new_content = content[:start_index] + new_function + content[end_index:]
    
    # Write the fixed content back
    with open(file_path, 'w') as f:
        f.write(new_content)
    
    print("✅ Fix applied successfully")
    print("📝 Fixed committees endpoint to use raw SQL instead of ORM")
    
    return True

if __name__ == "__main__":
    print("🔧 Congressional Data System - Committee Endpoint Fix")
    print("=" * 60)
    
    # Apply the fix
    success = apply_fix()
    
    if success:
        print("\n✅ Fix applied successfully!")
        print("📋 Next steps:")
        print("1. Deploy the updated API to production")
        print("2. Test the fixed endpoint")
        print("3. Update system health verification")
        print("\n🚀 The House committees endpoint should now work correctly.")
    else:
        print("\n❌ Fix failed to apply")
        print("📋 Manual intervention required")