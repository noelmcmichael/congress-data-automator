#!/usr/bin/env python3
"""Script to fix Pydantic v2 compatibility issues."""

import os
import re

def fix_pydantic_v2_in_file(file_path: str):
    """Fix Pydantic v2 compatibility in a single file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace .from_orm( with .model_validate(
    content = re.sub(r'\.from_orm\(', '.model_validate(', content)
    
    # Replace @validator with @field_validator
    content = re.sub(r'@validator\(', '@field_validator(', content)
    
    # Add @classmethod decorator after @field_validator
    content = re.sub(r'(@field_validator\([^)]+\))\s*\n\s*def\s+(\w+)\s*\(cls,', r'\1\n    @classmethod\n    def \2(cls,', content)
    
    # Replace validator import
    content = re.sub(r'from pydantic import ([^,\n]*,\s*)?validator', r'from pydantic import \1field_validator', content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Fixed {file_path}")

def fix_all_files():
    """Fix all Python files."""
    # Fix endpoints
    endpoints_dir = "api/endpoints"
    for filename in os.listdir(endpoints_dir):
        if filename.endswith('.py'):
            file_path = os.path.join(endpoints_dir, filename)
            fix_pydantic_v2_in_file(file_path)
    
    # Fix models
    models_dir = "api/models"
    for filename in os.listdir(models_dir):
        if filename.endswith('.py'):
            file_path = os.path.join(models_dir, filename)
            fix_pydantic_v2_in_file(file_path)

if __name__ == "__main__":
    fix_all_files()
    print("All Pydantic v2 compatibility issues fixed!")