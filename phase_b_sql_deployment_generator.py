#!/usr/bin/env python3
"""
Phase B: SQL Deployment Generator for Full Committee Expansion
=============================================================

Generate deployment-ready SQL from strategic expansion data using proven patterns.
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Any
import os

class SQLDeploymentGenerator:
    """Generate SQL deployment script from expansion data"""
    
    def __init__(self, expansion_file: str):
        self.expansion_file = expansion_file
        self.expansion_data = {}
        self.sql_statements = []
        
    def log_event(self, message: str, status: str = "info"):
        """Log generation events"""
        timestamp = datetime.now().isoformat()
        symbol = {"info": "ℹ️", "success": "✅", "error": "❌", "warning": "⚠️"}.get(status, "ℹ️")
        print(f"[{timestamp}] {symbol} {message}")
    
    def load_expansion_data(self) -> bool:
        """Load expansion data from JSON file"""
        try:
            if not os.path.exists(self.expansion_file):
                self.log_event(f"Expansion file not found: {self.expansion_file}", "error")
                return False
            
            with open(self.expansion_file, 'r') as f:
                self.expansion_data = json.load(f)
            
            committees_count = len(self.expansion_data.get('new_committees', []))
            self.log_event(f"Loaded expansion data: {committees_count} new committees", "success")
            return True
            
        except Exception as e:
            self.log_event(f"Failed to load expansion data: {e}", "error")
            return False
    
    def escape_sql_string(self, text: str) -> str:
        """Escape SQL strings properly"""
        if not text:
            return text
        # Escape single quotes by doubling them
        return text.replace("'", "''")
    
    def generate_committee_sql(self, committee: Dict[str, Any]) -> str:
        """Generate SQL INSERT statement for a committee"""
        
        # Extract and escape values
        name = self.escape_sql_string(committee.get('name', ''))
        chamber = committee.get('chamber', '')
        committee_code = committee.get('committee_code', '')
        congress_gov_id = committee.get('congress_gov_id', '')
        committee_type = committee.get('committee_type', 'Standing')
        is_active = committee.get('is_active', True)
        is_subcommittee = committee.get('is_subcommittee', False)
        website = committee.get('website', '')
        
        # Build INSERT statement using proven pattern
        sql = f"""
-- Committee: {name}
INSERT INTO committees (
    name, chamber, committee_code, congress_gov_id, committee_type,
    is_active, is_subcommittee, website, created_at
) VALUES (
    '{name}',
    '{chamber}',
    '{committee_code}',
    '{congress_gov_id}',
    '{committee_type}',
    {str(is_active).lower()},
    {str(is_subcommittee).lower()},
    '{website}',
    NOW()
) ON CONFLICT (congress_gov_id) DO NOTHING;"""
        
        return sql
    
    def generate_batch_sql(self, committees: List[Dict], batch_size: int = 50) -> List[str]:
        """Generate SQL in batches to avoid timeout issues"""
        self.log_event(f"Generating SQL in batches of {batch_size}")
        
        batches = []
        total_committees = len(committees)
        
        for i in range(0, total_committees, batch_size):
            batch_committees = committees[i:i + batch_size]
            batch_num = (i // batch_size) + 1
            total_batches = (total_committees + batch_size - 1) // batch_size
            
            # Create batch header
            batch_sql = f"""-- ====================================================================
-- Batch {batch_num} of {total_batches}: Committee Deployment
-- Generated: {datetime.now().isoformat()}
-- Committees in this batch: {len(batch_committees)}
-- ====================================================================

BEGIN;

"""
            
            # Add committee SQL statements
            for committee in batch_committees:
                committee_sql = self.generate_committee_sql(committee)
                batch_sql += committee_sql + "\n\n"
            
            # Add batch footer
            batch_sql += """COMMIT;

-- ====================================================================
-- End of Batch
-- ====================================================================

"""
            
            batches.append(batch_sql)
            self.log_event(f"Generated batch {batch_num}: {len(batch_committees)} committees")
        
        self.log_event(f"Generated {len(batches)} SQL batches", "success")
        return batches
    
    def generate_deployment_metadata(self) -> str:
        """Generate deployment metadata header"""
        metadata = self.expansion_data.get('metadata', {})
        
        header = f"""-- ====================================================================
-- FULL COMMITTEE EXPANSION DEPLOYMENT
-- ====================================================================
-- 
-- Generated: {datetime.now().isoformat()}
-- Source: Strategic Pattern-Based Expansion
-- 
-- Deployment Summary:
--   • Existing Committees: {metadata.get('existing_committees', 0)}
--   • New Committees: {metadata.get('new_committees_generated', 0)}
--   • Total Projected: {metadata.get('total_projected_committees', 0)}
--   • Target Coverage: {metadata.get('target_coverage', 'N/A')}
-- 
-- Chamber Breakdown (New):
--   • House: {metadata.get('chamber_breakdown_new', {}).get('House', 0)}
--   • Senate: {metadata.get('chamber_breakdown_new', {}).get('Senate', 0)}
--   • Joint: {metadata.get('chamber_breakdown_new', {}).get('Joint', 0)}
-- 
-- Type Breakdown (New):
--   • Standing: {metadata.get('type_breakdown_new', {}).get('Standing', 0)}
--   • Subcommittee: {metadata.get('type_breakdown_new', {}).get('Subcommittee', 0)}
--   • Joint: {metadata.get('type_breakdown_new', {}).get('Joint', 0)}
-- 
-- ====================================================================
-- DEPLOYMENT INSTRUCTIONS:
-- 
-- 1. Ensure Cloud SQL Proxy is running:
--    ./cloud-sql-proxy chefgavin:us-central1:congressional-db --port=5433
-- 
-- 2. Execute this script via proven deployment method:
--    python execute_committee_expansion_proxy_fixed.py
-- 
-- 3. Validate deployment:
--    python priority3_system_verification.py
-- 
-- ====================================================================

"""
        return header
    
    def generate_full_deployment_sql(self) -> str:
        """Generate complete deployment SQL file"""
        self.log_event("Generating full deployment SQL")
        
        if not self.expansion_data:
            self.log_event("No expansion data loaded", "error")
            return ""
        
        new_committees = self.expansion_data.get('new_committees', [])
        if not new_committees:
            self.log_event("No new committees found in expansion data", "warning")
            return ""
        
        # Generate metadata header
        full_sql = self.generate_deployment_metadata()
        
        # Sort committees by type for logical deployment order
        # 1. Main standing committees first
        # 2. Joint committees
        # 3. Subcommittees
        main_committees = [c for c in new_committees if not c.get('is_subcommittee', False)]
        subcommittees = [c for c in new_committees if c.get('is_subcommittee', False)]
        
        self.log_event(f"Organizing deployment: {len(main_committees)} main, {len(subcommittees)} subcommittees")
        
        # Deploy main committees first
        if main_committees:
            full_sql += f"""
-- ====================================================================
-- MAIN COMMITTEES DEPLOYMENT ({len(main_committees)} committees)
-- ====================================================================

BEGIN;

"""
            for committee in main_committees:
                committee_sql = self.generate_committee_sql(committee)
                full_sql += committee_sql + "\n\n"
            
            full_sql += "COMMIT;\n\n"
        
        # Deploy subcommittees in batches
        if subcommittees:
            batch_size = 50  # Proven batch size from successful deployments
            subcommittee_batches = self.generate_batch_sql(subcommittees, batch_size)
            
            full_sql += f"""
-- ====================================================================
-- SUBCOMMITTEES DEPLOYMENT ({len(subcommittees)} committees in {len(subcommittee_batches)} batches)
-- ====================================================================

"""
            for i, batch_sql in enumerate(subcommittee_batches):
                full_sql += batch_sql
        
        # Add validation footer
        full_sql += f"""
-- ====================================================================
-- DEPLOYMENT VALIDATION
-- ====================================================================

-- Check total committee count after deployment
SELECT 
    'Total Committees' as metric,
    COUNT(*) as count,
    '{self.expansion_data.get('metadata', {}).get('total_projected_committees', 'Unknown')}' as expected
FROM committees;

-- Check chamber distribution
SELECT 
    chamber,
    COUNT(*) as count
FROM committees 
GROUP BY chamber 
ORDER BY chamber;

-- Check committee types
SELECT 
    committee_type,
    COUNT(*) as count
FROM committees 
GROUP BY committee_type 
ORDER BY committee_type;

-- Check for any committees with missing congress_gov_id
SELECT 
    'Missing congress_gov_id' as issue,
    COUNT(*) as count
FROM committees 
WHERE congress_gov_id IS NULL OR congress_gov_id = '';

-- ====================================================================
-- END OF DEPLOYMENT
-- ====================================================================
"""
        
        self.log_event(f"Generated full deployment SQL: {len(full_sql)} characters", "success")
        return full_sql
    
    def save_deployment_sql(self, sql_content: str, filename: str = None) -> str:
        """Save deployment SQL to file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"full_committee_expansion_deployment_{timestamp}.sql"
        
        filepath = os.path.join(os.getcwd(), filename)
        
        with open(filepath, 'w') as f:
            f.write(sql_content)
        
        self.log_event(f"Deployment SQL saved to: {filepath}", "success")
        return filepath
    
    def run_sql_generation(self) -> Dict[str, Any]:
        """Run complete SQL generation process"""
        self.log_event("🚀 Starting SQL deployment generation", "info")
        
        # Load expansion data
        if not self.load_expansion_data():
            return {}
        
        # Generate SQL
        deployment_sql = self.generate_full_deployment_sql()
        if not deployment_sql:
            self.log_event("Failed to generate deployment SQL", "error")
            return {}
        
        # Save SQL file
        sql_file = self.save_deployment_sql(deployment_sql)
        
        # Create result summary
        metadata = self.expansion_data.get('metadata', {})
        result = {
            'sql_file': sql_file,
            'committees_count': metadata.get('new_committees_generated', 0),
            'total_projected': metadata.get('total_projected_committees', 0),
            'deployment_ready': True,
            'next_steps': [
                'Start Cloud SQL Proxy',
                'Execute deployment via proxy',
                'Run system verification'
            ]
        }
        
        self.log_event("✅ SQL deployment generation complete", "success")
        return result

def main():
    """Main execution function"""
    # Use the latest expansion file
    expansion_file = "strategic_full_expansion_20250709_115834.json"
    
    if not os.path.exists(expansion_file):
        print(f"❌ Expansion file not found: {expansion_file}")
        print("   Run strategic_full_expansion_generator.py first")
        return False
    
    # Generate SQL deployment
    generator = SQLDeploymentGenerator(expansion_file)
    result = generator.run_sql_generation()
    
    if not result:
        print("\n❌ SQL generation failed")
        return False
    
    # Summary
    print(f"\n🎯 SQL Deployment Generation Summary:")
    print(f"   New Committees: {result['committees_count']}")
    print(f"   Total Projected: {result['total_projected']}")
    print(f"   SQL File: {result['sql_file']}")
    print(f"   Status: {'✅ Ready for deployment' if result['deployment_ready'] else '❌ Not ready'}")
    
    print(f"\n📋 Next Steps:")
    for i, step in enumerate(result['next_steps'], 1):
        print(f"   {i}. {step}")
    
    if result['deployment_ready']:
        print(f"\n✅ Phase B complete - Ready for Phase C (deployment)")
        return True
    else:
        print(f"\n⚠️ Phase B incomplete - Review generated SQL")
        return False

if __name__ == "__main__":
    main()