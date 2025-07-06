#!/usr/bin/env python3
"""
Debug API parameter handling by adding logging to the data_retrieval.py file
"""
import os
import sys

# Add backend to path
sys.path.insert(0, '/Users/noelmcmichael/Workspace/congress_data_automator/backend')

from fastapi import FastAPI, Query, Depends
from sqlalchemy.orm import Session
from typing import Optional

# Mock dependencies for testing
def mock_get_db():
    """Mock database session for testing"""
    return None

def test_parameter_parsing():
    """Test how FastAPI parses query parameters"""
    print("Testing FastAPI Parameter Parsing")
    print("="*40)
    
    # Simulate the function signature from data_retrieval.py
    def get_members(
        page: int = Query(1, ge=1, description="Page number"),
        limit: int = Query(50, ge=1, le=200, description="Items per page"),
        search: Optional[str] = Query(None, description="Search by name"),
        chamber: Optional[str] = Query(None, description="Filter by chamber (house/senate)"),
        state: Optional[str] = Query(None, description="Filter by state"),
        party: Optional[str] = Query(None, description="Filter by party"),
        sort_by: Optional[str] = Query("last_name", description="Sort by field"),
        sort_order: Optional[str] = Query("asc", description="Sort order"),
        db: Session = Depends(mock_get_db)
    ):
        """Mock version of get_members to test parameter handling"""
        print(f"Received parameters:")
        print(f"  page: {page} (type: {type(page)})")
        print(f"  limit: {limit} (type: {type(limit)})")
        print(f"  search: {search} (type: {type(search)})")
        print(f"  chamber: {chamber} (type: {type(chamber)})")
        print(f"  state: {state} (type: {type(state)})")
        print(f"  party: {party} (type: {type(party)})")
        print(f"  sort_by: {sort_by} (type: {type(sort_by)})")
        print(f"  sort_order: {sort_order} (type: {type(sort_order)})")
        
        # Check for None values
        filters_applied = []
        if search: filters_applied.append(f"search={search}")
        if chamber: filters_applied.append(f"chamber={chamber}")
        if state: filters_applied.append(f"state={state}")
        if party: filters_applied.append(f"party={party}")
        
        print(f"  Filters that would be applied: {filters_applied}")
        
        return {"message": "Parameters parsed successfully"}
    
    # Test with various parameter combinations
    test_cases = [
        {"party": "Republican"},
        {"chamber": "House"},
        {"state": "CA"},
        {"party": "Democratic", "state": "CA"},
        {"chamber": "house", "party": "Republican"},
    ]
    
    for i, params in enumerate(test_cases, 1):
        print(f"\nTest case {i}: {params}")
        # This would normally be called by FastAPI's dependency injection
        # We'll just simulate the parameter values
        result = get_members(
            page=1,
            limit=50,
            search=params.get("search"),
            chamber=params.get("chamber"),
            state=params.get("state"),
            party=params.get("party"),
            sort_by="last_name",
            sort_order="asc",
            db=None
        )
        print(f"Result: {result}")

def analyze_data_retrieval_logic():
    """Analyze the actual data retrieval logic"""
    print("\n" + "="*50)
    print("ANALYZING DATA RETRIEVAL LOGIC")
    print("="*50)
    
    # Read and analyze the data_retrieval.py file
    file_path = "/Users/noelmcmichael/Workspace/congress_data_automator/backend/app/api/v1/data_retrieval.py"
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Look for filter logic
    lines = content.split('\n')
    filter_lines = []
    
    for i, line in enumerate(lines):
        if any(keyword in line.lower() for keyword in ['filter', 'query', 'where', 'chamber', 'party', 'state']):
            filter_lines.append(f"Line {i+1}: {line.strip()}")
    
    print("Filter-related lines found:")
    for line in filter_lines:
        print(f"  {line}")
    
    # Check for common issues
    print("\nChecking for common issues:")
    
    # Check if filters are actually being applied
    if "query = query.filter(" in content:
        print("  ✅ Filter method calls found")
    else:
        print("  ❌ No filter method calls found")
    
    # Check if there's proper parameter handling
    if "if chamber:" in content:
        print("  ✅ Chamber parameter check found")
    else:
        print("  ❌ Chamber parameter check not found")
    
    if "if party:" in content:
        print("  ✅ Party parameter check found")
    else:
        print("  ❌ Party parameter check not found")
    
    if "if state:" in content:
        print("  ✅ State parameter check found")
    else:
        print("  ❌ State parameter check not found")

def main():
    """Main execution function"""
    test_parameter_parsing()
    analyze_data_retrieval_logic()

if __name__ == "__main__":
    main()