#!/usr/bin/env python3
"""
System Health Monitor Service

This service monitors the overall health of the Congressional Data Automator system,
including API performance, database connectivity, and frontend deployment status.

Key Functions:
- API performance monitoring
- Database health checks
- Frontend deployment validation
- System metrics collection
"""

import logging
import sqlite3
import requests
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import json
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class HealthStatus(Enum):
    """Health status levels"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    CRITICAL = "critical"

class ComponentType(Enum):
    """System component types"""
    API = "api"
    DATABASE = "database"
    FRONTEND = "frontend"
    MONITORING = "monitoring"

@dataclass
class HealthCheck:
    """Health check result"""
    component: ComponentType
    status: HealthStatus
    response_time: float
    details: str
    metrics: Dict[str, Any]
    timestamp: datetime
    error: Optional[str] = None

class SystemHealthMonitor:
    """Monitor system health and performance"""
    
    def __init__(self, 
                 api_base_url: str = "https://congressional-data-api-v2-1066017671167.us-central1.run.app",
                 frontend_url: str = "https://storage.googleapis.com/congressional-data-frontend/index.html",
                 db_path: str = "congress_119th.db"):
        self.api_base_url = api_base_url
        self.frontend_url = frontend_url
        self.db_path = db_path
        self.timeout = 30  # seconds
        
    def check_api_health(self) -> HealthCheck:
        """Check API health and performance"""
        start_time = time.time()
        
        try:
            # Test health endpoint
            health_response = requests.get(
                f"{self.api_base_url}/health",
                timeout=self.timeout
            )
            
            # Test members endpoint
            members_response = requests.get(
                f"{self.api_base_url}/api/v1/members?limit=5",
                timeout=self.timeout
            )
            
            # Test committees endpoint
            committees_response = requests.get(
                f"{self.api_base_url}/api/v1/committees?limit=5",
                timeout=self.timeout
            )
            
            response_time = time.time() - start_time
            
            # Analyze responses
            endpoints_tested = 3
            endpoints_healthy = 0
            
            if health_response.status_code == 200:
                endpoints_healthy += 1
            if members_response.status_code == 200:
                endpoints_healthy += 1
            if committees_response.status_code == 200:
                endpoints_healthy += 1
            
            # Determine health status
            if endpoints_healthy == endpoints_tested:
                if response_time < 2.0:
                    status = HealthStatus.HEALTHY
                elif response_time < 5.0:
                    status = HealthStatus.DEGRADED
                else:
                    status = HealthStatus.UNHEALTHY
            elif endpoints_healthy >= 2:
                status = HealthStatus.DEGRADED
            else:
                status = HealthStatus.CRITICAL
            
            # Extract metrics
            metrics = {
                'endpoints_tested': endpoints_tested,
                'endpoints_healthy': endpoints_healthy,
                'response_time': response_time,
                'health_status_code': health_response.status_code,
                'members_status_code': members_response.status_code,
                'committees_status_code': committees_response.status_code,
                'success_rate': (endpoints_healthy / endpoints_tested) * 100
            }
            
            # Try to get member count from response
            if members_response.status_code == 200:
                try:
                    members_data = members_response.json()
                    if 'total' in members_data:
                        metrics['member_count'] = members_data['total']
                except:
                    pass
            
            details = f"API Health: {endpoints_healthy}/{endpoints_tested} endpoints healthy, {response_time:.2f}s response time"
            
            return HealthCheck(
                component=ComponentType.API,
                status=status,
                response_time=response_time,
                details=details,
                metrics=metrics,
                timestamp=datetime.now(),
                error=None
            )
            
        except requests.exceptions.Timeout:
            return HealthCheck(
                component=ComponentType.API,
                status=HealthStatus.CRITICAL,
                response_time=self.timeout,
                details="API request timed out",
                metrics={'timeout': True},
                timestamp=datetime.now(),
                error="Request timeout"
            )
        except requests.exceptions.ConnectionError as e:
            return HealthCheck(
                component=ComponentType.API,
                status=HealthStatus.CRITICAL,
                response_time=time.time() - start_time,
                details="API connection failed",
                metrics={'connection_error': True},
                timestamp=datetime.now(),
                error=str(e)
            )
        except Exception as e:
            return HealthCheck(
                component=ComponentType.API,
                status=HealthStatus.CRITICAL,
                response_time=time.time() - start_time,
                details=f"API health check failed: {str(e)}",
                metrics={'error': True},
                timestamp=datetime.now(),
                error=str(e)
            )
    
    def check_database_health(self) -> HealthCheck:
        """Check database health and performance"""
        start_time = time.time()
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Test basic connectivity
                cursor.execute("SELECT 1")
                cursor.fetchone()
                
                # Check table existence
                cursor.execute("""
                    SELECT name FROM sqlite_master 
                    WHERE type='table' AND name IN ('members_119th', 'committees_119th', 'committee_memberships_119th')
                """)
                tables = [row[0] for row in cursor.fetchall()]
                
                # Check data counts
                cursor.execute("SELECT COUNT(*) FROM members_119th")
                member_count = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM committees_119th")
                committee_count = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM committee_memberships_119th")
                membership_count = cursor.fetchone()[0]
                
                # Check database file size
                db_size = os.path.getsize(self.db_path) if os.path.exists(self.db_path) else 0
                
                response_time = time.time() - start_time
                
                # Determine health status
                required_tables = {'members_119th', 'committees_119th', 'committee_memberships_119th'}
                tables_present = set(tables)
                
                if required_tables.issubset(tables_present):
                    if member_count > 0 and committee_count > 0:
                        if response_time < 0.1:
                            status = HealthStatus.HEALTHY
                        elif response_time < 0.5:
                            status = HealthStatus.DEGRADED
                        else:
                            status = HealthStatus.UNHEALTHY
                    else:
                        status = HealthStatus.UNHEALTHY
                else:
                    status = HealthStatus.CRITICAL
                
                metrics = {
                    'response_time': response_time,
                    'member_count': member_count,
                    'committee_count': committee_count,
                    'membership_count': membership_count,
                    'db_size_bytes': db_size,
                    'db_size_mb': round(db_size / (1024 * 1024), 2),
                    'tables_present': len(tables_present),
                    'tables_required': len(required_tables),
                    'schema_complete': required_tables.issubset(tables_present)
                }
                
                details = f"Database Health: {member_count} members, {committee_count} committees, {response_time:.3f}s query time"
                
                return HealthCheck(
                    component=ComponentType.DATABASE,
                    status=status,
                    response_time=response_time,
                    details=details,
                    metrics=metrics,
                    timestamp=datetime.now(),
                    error=None
                )
                
        except sqlite3.Error as e:
            return HealthCheck(
                component=ComponentType.DATABASE,
                status=HealthStatus.CRITICAL,
                response_time=time.time() - start_time,
                details=f"Database error: {str(e)}",
                metrics={'database_error': True},
                timestamp=datetime.now(),
                error=str(e)
            )
        except Exception as e:
            return HealthCheck(
                component=ComponentType.DATABASE,
                status=HealthStatus.CRITICAL,
                response_time=time.time() - start_time,
                details=f"Database health check failed: {str(e)}",
                metrics={'error': True},
                timestamp=datetime.now(),
                error=str(e)
            )
    
    def check_frontend_health(self) -> HealthCheck:
        """Check frontend deployment health"""
        start_time = time.time()
        
        try:
            # Test frontend availability
            response = requests.get(self.frontend_url, timeout=self.timeout)
            
            response_time = time.time() - start_time
            
            # Check response characteristics
            is_html = 'text/html' in response.headers.get('content-type', '')
            has_react = 'react' in response.text.lower() if response.text else False
            has_congress = 'congress' in response.text.lower() if response.text else False
            content_length = len(response.content)
            
            # Determine health status
            if response.status_code == 200:
                if is_html and has_react and content_length > 1000:
                    if response_time < 2.0:
                        status = HealthStatus.HEALTHY
                    elif response_time < 5.0:
                        status = HealthStatus.DEGRADED
                    else:
                        status = HealthStatus.UNHEALTHY
                else:
                    status = HealthStatus.DEGRADED
            else:
                status = HealthStatus.CRITICAL
            
            metrics = {
                'response_time': response_time,
                'status_code': response.status_code,
                'content_length': content_length,
                'content_type': response.headers.get('content-type', ''),
                'is_html': is_html,
                'has_react': has_react,
                'has_congress': has_congress,
                'cache_control': response.headers.get('cache-control', ''),
                'last_modified': response.headers.get('last-modified', '')
            }
            
            details = f"Frontend Health: {response.status_code} status, {content_length} bytes, {response_time:.2f}s load time"
            
            return HealthCheck(
                component=ComponentType.FRONTEND,
                status=status,
                response_time=response_time,
                details=details,
                metrics=metrics,
                timestamp=datetime.now(),
                error=None
            )
            
        except requests.exceptions.Timeout:
            return HealthCheck(
                component=ComponentType.FRONTEND,
                status=HealthStatus.CRITICAL,
                response_time=self.timeout,
                details="Frontend request timed out",
                metrics={'timeout': True},
                timestamp=datetime.now(),
                error="Request timeout"
            )
        except requests.exceptions.ConnectionError as e:
            return HealthCheck(
                component=ComponentType.FRONTEND,
                status=HealthStatus.CRITICAL,
                response_time=time.time() - start_time,
                details="Frontend connection failed",
                metrics={'connection_error': True},
                timestamp=datetime.now(),
                error=str(e)
            )
        except Exception as e:
            return HealthCheck(
                component=ComponentType.FRONTEND,
                status=HealthStatus.CRITICAL,
                response_time=time.time() - start_time,
                details=f"Frontend health check failed: {str(e)}",
                metrics={'error': True},
                timestamp=datetime.now(),
                error=str(e)
            )
    
    def check_monitoring_health(self) -> HealthCheck:
        """Check monitoring system health"""
        start_time = time.time()
        
        try:
            # Check if monitoring services are functional
            from congressional_session_monitor import CongressionalSessionMonitor
            from data_freshness_validator import DataFreshnessValidator
            
            # Test session monitor
            session_monitor = CongressionalSessionMonitor(self.db_path)
            session_status = session_monitor.get_session_status()
            
            # Test data validator
            data_validator = DataFreshnessValidator(self.db_path)
            validation_result = data_validator.validate_member_data_currency()
            
            response_time = time.time() - start_time
            
            # Determine health status
            if session_status and validation_result:
                if response_time < 1.0:
                    status = HealthStatus.HEALTHY
                elif response_time < 3.0:
                    status = HealthStatus.DEGRADED
                else:
                    status = HealthStatus.UNHEALTHY
            else:
                status = HealthStatus.CRITICAL
            
            metrics = {
                'response_time': response_time,
                'session_monitor_working': session_status is not None,
                'data_validator_working': validation_result is not None,
                'session_status': session_status.value if session_status else None,
                'validation_status': validation_result.status.value if validation_result else None
            }
            
            details = f"Monitoring Health: Session monitoring and data validation operational, {response_time:.2f}s"
            
            return HealthCheck(
                component=ComponentType.MONITORING,
                status=status,
                response_time=response_time,
                details=details,
                metrics=metrics,
                timestamp=datetime.now(),
                error=None
            )
            
        except Exception as e:
            return HealthCheck(
                component=ComponentType.MONITORING,
                status=HealthStatus.CRITICAL,
                response_time=time.time() - start_time,
                details=f"Monitoring health check failed: {str(e)}",
                metrics={'error': True},
                timestamp=datetime.now(),
                error=str(e)
            )
    
    def run_comprehensive_health_check(self) -> Dict[str, HealthCheck]:
        """Run comprehensive system health check"""
        logger.info("Running comprehensive system health check")
        
        health_checks = {
            'api': self.check_api_health(),
            'database': self.check_database_health(),
            'frontend': self.check_frontend_health(),
            'monitoring': self.check_monitoring_health()
        }
        
        return health_checks
    
    def generate_health_report(self) -> Dict[str, Any]:
        """Generate comprehensive system health report"""
        health_checks = self.run_comprehensive_health_check()
        
        # Calculate overall system health
        critical_components = sum(1 for check in health_checks.values() if check.status == HealthStatus.CRITICAL)
        unhealthy_components = sum(1 for check in health_checks.values() if check.status == HealthStatus.UNHEALTHY)
        degraded_components = sum(1 for check in health_checks.values() if check.status == HealthStatus.DEGRADED)
        healthy_components = sum(1 for check in health_checks.values() if check.status == HealthStatus.HEALTHY)
        
        if critical_components > 0:
            overall_health = HealthStatus.CRITICAL
        elif unhealthy_components > 0:
            overall_health = HealthStatus.UNHEALTHY
        elif degraded_components > 0:
            overall_health = HealthStatus.DEGRADED
        else:
            overall_health = HealthStatus.HEALTHY
        
        # Calculate average response time
        avg_response_time = sum(check.response_time for check in health_checks.values()) / len(health_checks)
        
        # Generate recommendations
        recommendations = []
        for name, check in health_checks.items():
            if check.status != HealthStatus.HEALTHY:
                recommendations.append({
                    'component': name,
                    'status': check.status.value,
                    'issue': check.details,
                    'error': check.error
                })
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'overall_health': overall_health.value,
            'summary': {
                'total_components': len(health_checks),
                'healthy': healthy_components,
                'degraded': degraded_components,
                'unhealthy': unhealthy_components,
                'critical': critical_components,
                'average_response_time': round(avg_response_time, 3)
            },
            'components': {
                name: {
                    'status': check.status.value,
                    'response_time': check.response_time,
                    'details': check.details,
                    'metrics': check.metrics,
                    'error': check.error
                }
                for name, check in health_checks.items()
            },
            'recommendations': recommendations,
            'next_check_recommended': (datetime.now() + timedelta(minutes=5)).isoformat()
        }
        
        return report
    
    def save_health_metrics(self, health_checks: Dict[str, HealthCheck]):
        """Save health metrics to database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Create health metrics table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS system_health_metrics (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        component TEXT NOT NULL,
                        status TEXT NOT NULL,
                        response_time REAL NOT NULL,
                        details TEXT,
                        metrics TEXT,
                        error TEXT,
                        timestamp TEXT DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Insert health check results
                for name, check in health_checks.items():
                    cursor.execute("""
                        INSERT INTO system_health_metrics 
                        (component, status, response_time, details, metrics, error)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (
                        check.component.value,
                        check.status.value,
                        check.response_time,
                        check.details,
                        json.dumps(check.metrics),
                        check.error
                    ))
                
                conn.commit()
                logger.info(f"Saved {len(health_checks)} health metrics")
                
        except sqlite3.Error as e:
            logger.error(f"Error saving health metrics: {e}")

def main():
    """Main function for testing the System Health Monitor"""
    monitor = SystemHealthMonitor()
    
    # Run comprehensive health check
    report = monitor.generate_health_report()
    
    print("\n" + "="*60)
    print("SYSTEM HEALTH MONITORING REPORT")
    print("="*60)
    print(f"Timestamp: {report['timestamp']}")
    print(f"Overall Health: {report['overall_health'].upper()}")
    print(f"Components: {report['summary']['healthy']}/{report['summary']['total_components']} healthy")
    print(f"Average Response Time: {report['summary']['average_response_time']:.3f}s")
    
    print("\nComponent Health:")
    for name, component in report['components'].items():
        status_icon = "✅" if component['status'] == 'healthy' else "⚠️" if component['status'] == 'degraded' else "❌"
        print(f"  {status_icon} {name.upper()}: {component['status'].upper()} ({component['response_time']:.3f}s)")
        print(f"    {component['details']}")
        if component['error']:
            print(f"    Error: {component['error']}")
    
    if report['recommendations']:
        print("\nRecommendations:")
        for rec in report['recommendations']:
            print(f"  • {rec['component'].upper()}: {rec['issue']}")
            if rec['error']:
                print(f"    Error: {rec['error']}")
    
    print(f"\nNext check recommended: {report['next_check_recommended']}")
    print("="*60)

if __name__ == "__main__":
    main()