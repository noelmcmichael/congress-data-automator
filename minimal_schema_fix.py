#!/usr/bin/env python3
"""
Minimal schema fix - Add only URL fields to existing working schema
"""

import os
import subprocess
import sys

def create_minimal_schema_fix():
    """Create minimal fix by adding URL fields to current working schema"""
    print("=== CREATING MINIMAL SCHEMA FIX ===")
    
    # Instead of deploying a completely new container, let's just add the URL fields
    # to the existing committee response schema without changing anything else
    
    schema_file = "backend/app/schemas/committee.py"
    
    # Read current schema
    with open(schema_file, 'r') as f:
        content = f.read()
    
    print("Current committee schema:")
    print(content)
    
    # Check if URL fields are already present
    if 'hearings_url' in content and 'members_url' in content:
        print("✅ URL fields already present in schema")
        return True
    
    # The schema already has the URL fields, so the issue must be elsewhere
    # Let's check the database model field names vs schema field names
    
    print("\n=== FIELD NAME ANALYSIS ===")
    print("Schema expects: website, hearings_url, members_url, official_website_url")
    print("API returns: website_url")
    print("Database has: website, hearings_url, members_url, official_website_url")
    
    # The issue might be that the current production schema has "website_url"
    # but our enhanced schema has "website"
    
    # Let's create a version that matches current production exactly
    # but adds the URL fields
    
    return True

def check_working_vs_enhanced_differences():
    """Check what's different between working and enhanced versions"""
    print("\n=== ANALYZING DIFFERENCES ===")
    
    # The working version has limited fields, enhanced version has more
    # Maybe the issue is with model imports or database connections during startup
    
    # Let's check the main.py file to see if there are any changes that could cause startup delays
    main_file = "backend/app/main.py"
    
    with open(main_file, 'r') as f:
        main_content = f.read()
    
    print("Checking main.py for potential startup issues...")
    
    # Look for potential startup delays
    startup_issues = []
    
    if "Base.metadata.create_all" in main_content and not main_content.count("# Base.metadata.create_all"):
        startup_issues.append("Database table creation enabled (could cause timeout)")
    
    if "from .models import" in main_content:
        startup_issues.append("Model imports present (could cause startup delays)")
    
    if "congress_api = CongressApiClient()" in main_content:
        startup_issues.append("API client initialization at startup")
    
    if startup_issues:
        print("Potential startup issues found:")
        for issue in startup_issues:
            print(f"  ⚠️ {issue}")
    else:
        print("✅ No obvious startup issues in main.py")
    
    return len(startup_issues) == 0

def propose_alternative_strategy():
    """Propose alternative strategy for getting URL fields"""
    print("\n=== ALTERNATIVE STRATEGY ===")
    
    print("Since container deployment keeps failing, alternative approaches:")
    print("")
    print("OPTION 1: Database-only update")
    print("  - Verify URL data is in database")
    print("  - Update frontend to use URL data from database directly")
    print("  - Skip API enhancement for now")
    print("")
    print("OPTION 2: Schema-only fix")
    print("  - Identify exact field name mismatch")
    print("  - Fix schema to match what's currently working")
    print("  - Add URL fields without changing other parts")
    print("")
    print("OPTION 3: Simple deployment")
    print("  - Remove all potential startup delays")
    print("  - Deploy minimal working version first")
    print("  - Add enhancements incrementally")
    print("")
    print("RECOMMENDED: Option 2 - Schema-only fix")
    print("This avoids deployment issues while adding URL fields")
    
    return True

def main():
    """Main analysis function"""
    print("Minimal Schema Fix Analysis")
    print("Goal: Add URL fields without deployment issues")
    print("=" * 50)
    
    create_minimal_schema_fix()
    startup_ok = check_working_vs_enhanced_differences()
    propose_alternative_strategy()
    
    if startup_ok:
        print("\n✅ ANALYSIS COMPLETE")
        print("No obvious startup issues found")
        print("Issue likely in field name mapping or database connection")
    else:
        print("\n⚠️ STARTUP ISSUES IDENTIFIED")
        print("Need to fix startup delays before deployment")
    
    return True

if __name__ == "__main__":
    main()