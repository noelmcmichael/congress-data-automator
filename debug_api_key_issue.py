#!/usr/bin/env python3
"""
Debug API key issue by adding a debug endpoint.
"""
import os

# Add a debug endpoint to check environment variables
debug_endpoint = '''
@router.get("/debug/environment")
async def debug_environment():
    """Debug endpoint to check environment variables."""
    return {
        "congress_api_key_exists": bool(os.getenv("CONGRESS_API_KEY")),
        "congress_api_key_length": len(os.getenv("CONGRESS_API_KEY", "")),
        "congress_api_key_prefix": os.getenv("CONGRESS_API_KEY", "")[:8] if os.getenv("CONGRESS_API_KEY") else None,
        "all_env_vars": list(os.environ.keys()),
        "database_url_exists": bool(os.getenv("DATABASE_URL")),
        "secret_key_exists": bool(os.getenv("SECRET_KEY"))
    }
'''

# Read the current data_updates.py file
with open('/Users/noelmcmichael/Workspace/congress_data_automator/backend/app/api/v1/data_updates.py', 'r') as f:
    content = f.read()

# Add the debug endpoint before the existing endpoints
if "debug/environment" not in content:
    # Find the first router.get or router.post line
    lines = content.split('\n')
    insert_index = None
    for i, line in enumerate(lines):
        if "@router.post" in line or "@router.get" in line:
            insert_index = i
            break
    
    if insert_index:
        # Insert the debug endpoint
        import_line = "import os"
        if import_line not in content:
            lines.insert(1, import_line)
            insert_index += 1
        
        debug_lines = debug_endpoint.strip().split('\n')
        for j, debug_line in enumerate(debug_lines):
            lines.insert(insert_index + j, debug_line)
        
        # Write the updated content
        with open('/Users/noelmcmichael/Workspace/congress_data_automator/backend/app/api/v1/data_updates.py', 'w') as f:
            f.write('\n'.join(lines))
        
        print("✅ Debug endpoint added to data_updates.py")
    else:
        print("❌ Could not find insertion point")
else:
    print("✅ Debug endpoint already exists")

print("Debug endpoint added. Now rebuilding and deploying...")