#!/usr/bin/env python3
"""
Phase 2 Runner - Loads environment and executes member collection
"""

import os
import sys
import asyncio
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Check for required environment variables
required_env_vars = ['CONGRESS_API_KEY', 'DATABASE_URL']
missing_vars = []

for var in required_env_vars:
    value = os.getenv(var)
    if not value:
        missing_vars.append(var)
    else:
        print(f"✓ {var} loaded")

if missing_vars:
    print(f"\n❌ Error: Missing required environment variables:")
    for var in missing_vars:
        print(f"   - {var}")
    print(f"\nPlease check your .env file and ensure these variables are set.")
    sys.exit(1)

print(f"\n✅ All required environment variables loaded")
print(f"🚀 Starting Phase 2: Complete Member Collection")

# Import and run the main Phase 2 coordinator
from phase2_member_collection import main

if __name__ == "__main__":
    asyncio.run(main())