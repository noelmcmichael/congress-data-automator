#!/usr/bin/env python3
"""
Investigate Schema Issue
========================

Find which field is causing the character varying(50) constraint violation.
"""

import subprocess
import time
import psycopg2
import re
from datetime import datetime

class SchemaInvestigator:
    def __init__(self):
        self.proxy_process = None
        
    def log_event(self, message: str, status: str = "info"):
        timestamp = datetime.now().isoformat()
        symbol = {"info": "ℹ️", "success": "✅", "error": "❌", "warning": "⚠️"}.get(status, "ℹ️")
        print(f"[{timestamp}] {symbol} {message}")
        
    def start_proxy(self):
        """Start Cloud SQL proxy"""
        try:
            cmd = ["./cloud-sql-proxy", "chefgavin:us-central1:congressional-db", "--port=5433"]
            self.proxy_process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            time.sleep(5)  # Wait for startup
            
            if self.proxy_process.poll() is None:
                self.log_event("Proxy started", "success")
                return True
            else:
                self.log_event("Proxy failed to start", "error")
                return False
        except Exception as e:
            self.log_event(f"Proxy error: {e}", "error")
            return False
    
    def stop_proxy(self):
        """Stop proxy"""
        if self.proxy_process:
            self.proxy_process.terminate()
            
    def get_schema_info(self):
        """Get schema information for committees table"""
        try:
            conn = psycopg2.connect(
                host="localhost", port=5433, database="congress_data",
                user="postgres", password="mDf3S9ZnBpQqJvGsY1"
            )
            
            cursor = conn.cursor()
            
            # Get column information
            cursor.execute("""
                SELECT column_name, data_type, character_maximum_length, is_nullable
                FROM information_schema.columns 
                WHERE table_name = 'committees' 
                ORDER BY ordinal_position;
            """)
            
            columns = cursor.fetchall()
            
            self.log_event("Committees table schema:", "info")
            for col_name, data_type, max_len, nullable in columns:
                max_len_str = f"({max_len})" if max_len else ""
                nullable_str = "NULL" if nullable == "YES" else "NOT NULL"
                print(f"  {col_name}: {data_type}{max_len_str} {nullable_str}")
            
            cursor.close()
            conn.close()
            
            return columns
            
        except Exception as e:
            self.log_event(f"Schema check failed: {e}", "error")
            return None
    
    def find_long_values(self):
        """Find values that might be too long for varchar(50) fields"""
        
        # Read the deployment file
        with open("phase3_expansion_deployment_20250709_104859.sql", "r") as f:
            content = f.read()
        
        # Find all INSERT statements
        insert_pattern = r"INSERT INTO committees.*?VALUES\s*\((.*?)\)"
        matches = re.findall(insert_pattern, content, re.DOTALL)
        
        self.log_event(f"Found {len(matches)} INSERT statements")
        
        # Check for long values
        problematic_inserts = []
        
        for i, insert_values in enumerate(matches):
            # Extract individual values (simple parsing)
            values = []
            current_value = ""
            in_quotes = False
            
            for char in insert_values:
                if char == "'" and not in_quotes:
                    in_quotes = True
                    current_value = ""
                elif char == "'" and in_quotes:
                    in_quotes = False
                    values.append(current_value)
                    current_value = ""
                elif in_quotes:
                    current_value += char
                elif char == "," and not in_quotes:
                    if current_value.strip() and not current_value.strip().startswith("'"):
                        values.append(current_value.strip())
                        current_value = ""
                else:
                    if not in_quotes:
                        current_value += char
            
            # Add final value
            if current_value.strip():
                values.append(current_value.strip())
            
            # Check for values longer than 50 characters
            for j, value in enumerate(values):
                if isinstance(value, str) and len(value) > 50:
                    problematic_inserts.append({
                        "insert_number": i + 1,
                        "field_position": j + 1,
                        "value": value[:100] + "..." if len(value) > 100 else value,
                        "length": len(value)
                    })
        
        if problematic_inserts:
            self.log_event(f"Found {len(problematic_inserts)} values longer than 50 characters:", "warning")
            for issue in problematic_inserts[:10]:  # Show first 10
                self.log_event(f"  Insert {issue['insert_number']}, field {issue['field_position']}: {issue['length']} chars", "warning")
                self.log_event(f"    Value: {issue['value']}", "info")
        else:
            self.log_event("No values longer than 50 characters found", "success")
        
        return problematic_inserts
    
    def investigate(self):
        """Run complete investigation"""
        self.log_event("🔍 Starting schema constraint investigation")
        
        try:
            if not self.start_proxy():
                return False
            
            # Get schema info
            schema_info = self.get_schema_info()
            
            # Find problematic values
            long_values = self.find_long_values()
            
            # Analysis
            varchar50_fields = []
            if schema_info:
                varchar50_fields = [col[0] for col in schema_info if col[1] == 'character varying' and col[2] == 50]
                
                if varchar50_fields:
                    self.log_event(f"Fields with varchar(50) constraint: {varchar50_fields}", "warning")
                else:
                    self.log_event("No varchar(50) fields found - investigating other constraints", "info")
            
            return True
            
        finally:
            self.stop_proxy()

def main():
    investigator = SchemaInvestigator()
    investigator.investigate()

if __name__ == "__main__":
    main()