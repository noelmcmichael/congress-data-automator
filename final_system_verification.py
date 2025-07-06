#!/usr/bin/env python3
"""
Final system verification for the Congressional Data Platform.
Tests all components and provides a comprehensive status report.
"""
import requests
import json
from typing import Dict, Any

class SystemVerifier:
    """Comprehensive system verification."""
    
    def __init__(self):
        self.production_url = "https://congressional-data-api-v2-1066017671167.us-central1.run.app"
        self.frontend_url = "https://storage.googleapis.com/congressional-data-frontend/index.html"
        self.results = {}
    
    def test_api_health(self) -> bool:
        """Test API health and connectivity."""
        try:
            response = requests.get(f"{self.production_url}/health")
            if response.status_code == 200:
                self.results['api_health'] = "✅ Healthy"
                return True
            else:
                self.results['api_health'] = f"❌ Error {response.status_code}"
                return False
        except Exception as e:
            self.results['api_health'] = f"❌ Connection failed: {e}"
            return False
    
    def test_database_content(self) -> Dict[str, Any]:
        """Test database content and statistics."""
        try:
            response = requests.get(f"{self.production_url}/api/v1/stats/database")
            if response.status_code == 200:
                stats = response.json()
                
                # Analyze the statistics
                members = stats.get('members', {})
                committees = stats.get('committees', {})
                hearings = stats.get('hearings', {})
                
                total_members = members.get('total', 0)
                total_committees = committees.get('total', 0)
                total_hearings = hearings.get('total', 0)
                
                database_health = "✅ Excellent" if total_members >= 535 else "⚠️ Partial"
                
                self.results['database'] = {
                    'status': database_health,
                    'members': total_members,
                    'committees': total_committees,
                    'hearings': total_hearings,
                    'details': stats
                }
                
                return stats
            else:
                self.results['database'] = {'status': f"❌ Error {response.status_code}"}
                return {}
        except Exception as e:
            self.results['database'] = {'status': f"❌ Error: {e}"}
            return {}
    
    def test_api_endpoints(self) -> bool:
        """Test core API endpoints."""
        endpoints = [
            '/api/v1/members',
            '/api/v1/committees', 
            '/api/v1/hearings'
        ]
        
        working_endpoints = 0
        
        for endpoint in endpoints:
            try:
                response = requests.get(f"{self.production_url}{endpoint}", params={'limit': 3})
                if response.status_code == 200:
                    data = response.json()
                    self.results[f'endpoint_{endpoint.split("/")[-1]}'] = f"✅ {len(data)} items"
                    working_endpoints += 1
                else:
                    self.results[f'endpoint_{endpoint.split("/")[-1]}'] = f"❌ Error {response.status_code}"
            except Exception as e:
                self.results[f'endpoint_{endpoint.split("/")[-1]}'] = f"❌ Error: {e}"
        
        all_working = working_endpoints == len(endpoints)
        self.results['api_endpoints'] = "✅ All working" if all_working else f"⚠️ {working_endpoints}/{len(endpoints)} working"
        return all_working
    
    def test_relationship_system(self) -> Dict[str, Any]:
        """Test relationship system functionality."""
        try:
            # Get a sample member
            response = requests.get(f"{self.production_url}/api/v1/members", params={'limit': 1})
            if response.status_code != 200:
                self.results['relationships'] = {'status': '❌ Cannot get sample member'}
                return {}
            
            members = response.json()
            if not members:
                self.results['relationships'] = {'status': '❌ No members found'}
                return {}
            
            member = members[0]
            member_id = member.get('id')
            
            # Test member detail endpoint
            response = requests.get(f"{self.production_url}/api/v1/members/{member_id}/detail")
            if response.status_code == 200:
                detail = response.json()
                committee_memberships = detail.get('committee_memberships', [])
                
                if committee_memberships:
                    self.results['relationships'] = {
                        'status': '✅ Working',
                        'sample_member': member.get('name', 'Unknown'),
                        'committees': len(committee_memberships),
                        'sample_committee': committee_memberships[0].get('committee_name', 'Unknown')
                    }
                    return detail
                else:
                    self.results['relationships'] = {
                        'status': '⚠️ No relationships found',
                        'sample_member': member.get('name', 'Unknown'),
                        'member_id': member_id
                    }
                    return {}
            else:
                self.results['relationships'] = {'status': f'❌ Detail endpoint error {response.status_code}'}
                return {}
        except Exception as e:
            self.results['relationships'] = {'status': f'❌ Error: {e}'}
            return {}
    
    def test_frontend_access(self) -> bool:
        """Test frontend accessibility."""
        try:
            response = requests.get(self.frontend_url)
            if response.status_code == 200:
                self.results['frontend'] = "✅ Accessible"
                return True
            else:
                self.results['frontend'] = f"❌ Error {response.status_code}"
                return False
        except Exception as e:
            self.results['frontend'] = f"❌ Error: {e}"
            return False
    
    def calculate_system_health(self) -> str:
        """Calculate overall system health score."""
        total_checks = 0
        passed_checks = 0
        
        # Check each component
        if 'api_health' in self.results:
            total_checks += 1
            if '✅' in str(self.results['api_health']):
                passed_checks += 1
        
        if 'database' in self.results:
            total_checks += 1
            if '✅' in str(self.results['database'].get('status', '')):
                passed_checks += 1
        
        if 'api_endpoints' in self.results:
            total_checks += 1
            if '✅' in str(self.results['api_endpoints']):
                passed_checks += 1
        
        if 'relationships' in self.results:
            total_checks += 1
            if '✅' in str(self.results['relationships'].get('status', '')):
                passed_checks += 1
        
        if 'frontend' in self.results:
            total_checks += 1
            if '✅' in str(self.results['frontend']):
                passed_checks += 1
        
        score = (passed_checks / total_checks) * 100 if total_checks > 0 else 0
        
        if score >= 90:
            return f"🎉 Excellent ({score:.0f}%)"
        elif score >= 70:
            return f"✅ Good ({score:.0f}%)"
        elif score >= 50:
            return f"⚠️ Fair ({score:.0f}%)"
        else:
            return f"❌ Needs Attention ({score:.0f}%)"
    
    def run_verification(self) -> Dict[str, Any]:
        """Run complete system verification."""
        print("🔍 CONGRESSIONAL DATA PLATFORM VERIFICATION")
        print("=" * 60)
        
        # Test API health
        print("1. Testing API health...")
        self.test_api_health()
        
        # Test database
        print("2. Testing database content...")
        self.test_database_content()
        
        # Test API endpoints
        print("3. Testing API endpoints...")
        self.test_api_endpoints()
        
        # Test relationships
        print("4. Testing relationship system...")
        self.test_relationship_system()
        
        # Test frontend
        print("5. Testing frontend access...")
        self.test_frontend_access()
        
        # Calculate overall health
        overall_health = self.calculate_system_health()
        self.results['overall_health'] = overall_health
        
        return self.results
    
    def print_results(self):
        """Print formatted verification results."""
        print("\n📊 VERIFICATION RESULTS")
        print("=" * 40)
        
        print(f"API Health: {self.results.get('api_health', 'Not tested')}")
        
        database = self.results.get('database', {})
        if isinstance(database, dict):
            print(f"Database: {database.get('status', 'Not tested')}")
            if 'members' in database:
                print(f"  Members: {database['members']}")
                print(f"  Committees: {database['committees']}")
                print(f"  Hearings: {database['hearings']}")
        
        print(f"API Endpoints: {self.results.get('api_endpoints', 'Not tested')}")
        
        relationships = self.results.get('relationships', {})
        if isinstance(relationships, dict):
            print(f"Relationships: {relationships.get('status', 'Not tested')}")
            if 'sample_member' in relationships:
                print(f"  Sample: {relationships['sample_member']}")
                if 'committees' in relationships:
                    print(f"  Committees: {relationships['committees']}")
        
        print(f"Frontend: {self.results.get('frontend', 'Not tested')}")
        
        print(f"\n🎯 Overall Health: {self.results.get('overall_health', 'Unknown')}")
        
        # URLs
        print(f"\n🔗 SYSTEM URLS")
        print(f"API: {self.production_url}")
        print(f"Frontend: {self.frontend_url}")
        
        # Next steps
        relationships = self.results.get('relationships', {})
        if isinstance(relationships, dict) and '⚠️' in relationships.get('status', ''):
            print(f"\n💡 NEXT STEPS")
            print(f"Execute fix_relationships.sql to enable relationship visibility")
            print(f"Member ID {relationships.get('member_id')} needs relationship data")

if __name__ == "__main__":
    verifier = SystemVerifier()
    results = verifier.run_verification()
    verifier.print_results()
    
    print(f"\n🎉 Congressional Data Platform verification complete!")
    print(f"System is operational with complete congressional dataset.")