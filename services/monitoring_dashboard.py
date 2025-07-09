#!/usr/bin/env python3
"""
Monitoring Dashboard Service

This service provides a comprehensive monitoring dashboard that integrates
all monitoring components and provides a unified view of system health.

Key Functions:
- Integrated monitoring dashboard
- Real-time system status
- Historical trend analysis
- Alert management interface
"""

import logging
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MonitoringDashboard:
    """Comprehensive monitoring dashboard"""
    
    def __init__(self, db_path: str = "congress_119th.db"):
        self.db_path = db_path
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize all monitoring components"""
        try:
            from congressional_session_monitor import CongressionalSessionMonitor
            from data_freshness_validator import DataFreshnessValidator
            from system_health_monitor import SystemHealthMonitor
            from automated_update_triggers import AutomatedUpdateTriggers
            from alert_system import AlertSystem
            
            self.session_monitor = CongressionalSessionMonitor(self.db_path)
            self.data_validator = DataFreshnessValidator(self.db_path)
            self.health_monitor = SystemHealthMonitor(db_path=self.db_path)
            self.update_triggers = AutomatedUpdateTriggers(self.db_path)
            self.alert_system = AlertSystem(self.db_path)
            
            logger.info("Monitoring components initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing monitoring components: {e}")
            raise
    
    def get_comprehensive_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        logger.info("Generating comprehensive system status report")
        
        try:
            # Get Congressional session status
            session_report = self.session_monitor.get_data_freshness_report()
            
            # Get data freshness status
            freshness_report = self.data_validator.generate_freshness_report()
            
            # Get system health status
            health_report = self.health_monitor.generate_health_report()
            
            # Get update triggers status
            triggers_status = self.update_triggers.get_trigger_status()
            
            # Get recent alerts
            recent_alerts = self.alert_system.get_alert_history(limit=10)
            
            # Calculate overall system status
            overall_status = self._calculate_overall_status(
                session_report, freshness_report, health_report
            )
            
            # Generate recommendations
            recommendations = self._generate_recommendations(
                session_report, freshness_report, health_report, triggers_status
            )
            
            status = {
                'timestamp': datetime.now().isoformat(),
                'overall_status': overall_status,
                'components': {
                    'congressional_session': {
                        'status': session_report.get('session_status', 'unknown'),
                        'current_congress': session_report['current_session']['number'],
                        'leadership_current': session_report['leadership_currency']['is_current'],
                        'transition_detected': session_report['transition_detected'],
                        'last_updated': session_report['timestamp']
                    },
                    'data_freshness': {
                        'status': freshness_report['overall_status'],
                        'checks_passed': freshness_report['summary']['passed'],
                        'total_checks': freshness_report['summary']['total_checks'],
                        'critical_issues': freshness_report['summary']['critical'],
                        'warning_issues': freshness_report['summary']['warnings'],
                        'last_updated': freshness_report['timestamp']
                    },
                    'system_health': {
                        'status': health_report['overall_health'],
                        'healthy_components': health_report['summary']['healthy'],
                        'total_components': health_report['summary']['total_components'],
                        'avg_response_time': health_report['summary']['average_response_time'],
                        'last_updated': health_report['timestamp']
                    },
                    'update_triggers': {
                        'scheduler_running': triggers_status['scheduler_running'],
                        'total_triggers': len(triggers_status['triggers']),
                        'enabled_triggers': sum(1 for t in triggers_status['triggers'].values() if t['enabled']),
                        'next_trigger': self._get_next_trigger_time(triggers_status['triggers'])
                    },
                    'alerts': {
                        'recent_count': len(recent_alerts),
                        'last_alert': recent_alerts[0]['created_at'] if recent_alerts else None,
                        'critical_alerts_24h': sum(1 for a in recent_alerts if a['severity'] == 'critical' and 
                                                 self._is_within_24h(a['created_at'])),
                        'total_alerts_24h': sum(1 for a in recent_alerts if self._is_within_24h(a['created_at']))
                    }
                },
                'recommendations': recommendations,
                'metrics': {
                    'member_count': freshness_report['validations']['member_data']['metrics'].get('total_members', 0),
                    'committee_count': freshness_report['validations']['member_data']['metrics'].get('total_committees', 0),
                    'api_response_time': health_report['components']['api']['response_time'],
                    'database_response_time': health_report['components']['database']['response_time'],
                    'frontend_response_time': health_report['components']['frontend']['response_time']
                }
            }
            
            return status
            
        except Exception as e:
            logger.error(f"Error generating comprehensive status: {e}")
            return {
                'timestamp': datetime.now().isoformat(),
                'overall_status': 'ERROR',
                'error': str(e)
            }
    
    def _calculate_overall_status(self, session_report: Dict, freshness_report: Dict, health_report: Dict) -> str:
        """Calculate overall system status"""
        # Check for critical issues
        if freshness_report['summary']['critical'] > 0:
            return 'CRITICAL'
        if health_report['overall_health'] == 'critical':
            return 'CRITICAL'
        
        # Check for warnings
        if freshness_report['summary']['warnings'] > 0:
            return 'WARNING'
        if health_report['overall_health'] in ['unhealthy', 'degraded']:
            return 'WARNING'
        
        # Check session status
        if session_report.get('session_status') == 'outdated':
            return 'WARNING'
        
        # All good
        return 'HEALTHY'
    
    def _generate_recommendations(self, session_report: Dict, freshness_report: Dict, 
                                health_report: Dict, triggers_status: Dict) -> List[Dict[str, Any]]:
        """Generate system recommendations"""
        recommendations = []
        
        # Congressional session recommendations
        if session_report.get('session_status') == 'outdated':
            recommendations.append({
                'priority': 'high',
                'category': 'congressional_session',
                'title': 'Update Congressional Session Data',
                'description': 'Database contains outdated Congressional session data',
                'action': 'Run Congressional session update'
            })
        
        # Data freshness recommendations
        if freshness_report['summary']['critical'] > 0:
            recommendations.append({
                'priority': 'critical',
                'category': 'data_freshness',
                'title': 'Critical Data Issues',
                'description': f"{freshness_report['summary']['critical']} critical data issues detected",
                'action': 'Review and fix data quality issues'
            })
        
        # System health recommendations
        if health_report['overall_health'] == 'critical':
            recommendations.append({
                'priority': 'critical',
                'category': 'system_health',
                'title': 'System Health Critical',
                'description': 'One or more system components are in critical state',
                'action': 'Investigate and resolve system health issues'
            })
        
        # Update triggers recommendations
        if not triggers_status['scheduler_running']:
            recommendations.append({
                'priority': 'medium',
                'category': 'automation',
                'title': 'Automated Updates Disabled',
                'description': 'Automated update scheduler is not running',
                'action': 'Enable automated update scheduler'
            })
        
        return recommendations
    
    def _get_next_trigger_time(self, triggers: Dict[str, Any]) -> Optional[str]:
        """Get next trigger time"""
        next_times = []
        for trigger in triggers.values():
            if trigger.get('next_trigger'):
                next_times.append(trigger['next_trigger'])
        
        if next_times:
            return min(next_times)
        return None
    
    def _is_within_24h(self, timestamp_str: str) -> bool:
        """Check if timestamp is within last 24 hours"""
        try:
            timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            return datetime.now() - timestamp < timedelta(hours=24)
        except:
            return False
    
    def run_monitoring_cycle(self) -> Dict[str, Any]:
        """Run complete monitoring cycle"""
        logger.info("Running complete monitoring cycle")
        
        try:
            # Get comprehensive status
            status = self.get_comprehensive_status()
            
            # Process alerts based on status
            alerts_created = self.alert_system.process_monitoring_data({
                'data_freshness_status': status['components']['data_freshness']['status'],
                'data_freshness_issues': status['components']['data_freshness']['critical_issues'],
                'api_health_status': status['components']['system_health']['status'],
                'system_health_status': status['overall_status'],
                'critical_components': status['components']['system_health']['total_components'] - 
                                     status['components']['system_health']['healthy_components'],
                'congress_transition_detected': status['components']['congressional_session']['transition_detected'],
                'leadership_changes_detected': not status['components']['congressional_session']['leadership_current']
            })
            
            # Run trigger checks
            self.update_triggers.run_trigger_check()
            
            cycle_result = {
                'timestamp': datetime.now().isoformat(),
                'monitoring_cycle_completed': True,
                'status': status,
                'alerts_created': len(alerts_created),
                'trigger_checks_completed': True
            }
            
            logger.info(f"Monitoring cycle completed successfully. Created {len(alerts_created)} alerts.")
            
            return cycle_result
            
        except Exception as e:
            logger.error(f"Error in monitoring cycle: {e}")
            return {
                'timestamp': datetime.now().isoformat(),
                'monitoring_cycle_completed': False,
                'error': str(e)
            }
    
    def generate_monitoring_report(self) -> str:
        """Generate human-readable monitoring report"""
        status = self.get_comprehensive_status()
        
        report = f"""
{'='*60}
CONGRESSIONAL DATA AUTOMATOR - MONITORING REPORT
{'='*60}
Generated: {status['timestamp']}
Overall Status: {status['overall_status']}

CONGRESSIONAL SESSION STATUS
{'='*30}
Current Congress: {status['components']['congressional_session']['current_congress']}th Congress
Session Status: {status['components']['congressional_session']['status']}
Leadership Current: {'✅' if status['components']['congressional_session']['leadership_current'] else '❌'}
Transition Detected: {'✅' if status['components']['congressional_session']['transition_detected'] else '❌'}

DATA FRESHNESS STATUS
{'='*30}
Overall Status: {status['components']['data_freshness']['status']}
Checks Passed: {status['components']['data_freshness']['checks_passed']}/{status['components']['data_freshness']['total_checks']}
Critical Issues: {status['components']['data_freshness']['critical_issues']}
Warning Issues: {status['components']['data_freshness']['warning_issues']}

SYSTEM HEALTH STATUS
{'='*30}
Overall Health: {status['components']['system_health']['status']}
Healthy Components: {status['components']['system_health']['healthy_components']}/{status['components']['system_health']['total_components']}
Avg Response Time: {status['components']['system_health']['avg_response_time']:.3f}s

AUTOMATION STATUS
{'='*30}
Scheduler Running: {'✅' if status['components']['update_triggers']['scheduler_running'] else '❌'}
Enabled Triggers: {status['components']['update_triggers']['enabled_triggers']}/{status['components']['update_triggers']['total_triggers']}
Next Trigger: {status['components']['update_triggers']['next_trigger'] or 'None scheduled'}

ALERTS STATUS
{'='*30}
Recent Alerts: {status['components']['alerts']['recent_count']}
Critical Alerts (24h): {status['components']['alerts']['critical_alerts_24h']}
Total Alerts (24h): {status['components']['alerts']['total_alerts_24h']}
Last Alert: {status['components']['alerts']['last_alert'] or 'None'}

KEY METRICS
{'='*30}
Members: {status['metrics']['member_count']}
Committees: {status['metrics']['committee_count']}
API Response Time: {status['metrics']['api_response_time']:.3f}s
Database Response Time: {status['metrics']['database_response_time']:.3f}s
Frontend Response Time: {status['metrics']['frontend_response_time']:.3f}s
"""
        
        if status['recommendations']:
            report += f"\nRECOMMENDATIONS\n{'='*30}\n"
            for i, rec in enumerate(status['recommendations'], 1):
                priority_icon = "🚨" if rec['priority'] == 'critical' else "⚠️" if rec['priority'] == 'high' else "ℹ️"
                report += f"{i}. {priority_icon} {rec['title']}\n"
                report += f"   {rec['description']}\n"
                report += f"   Action: {rec['action']}\n\n"
        
        report += f"{'='*60}\n"
        
        return report

def main():
    """Main function for testing the Monitoring Dashboard"""
    dashboard = MonitoringDashboard()
    
    # Run monitoring cycle
    cycle_result = dashboard.run_monitoring_cycle()
    
    # Generate and display report
    report = dashboard.generate_monitoring_report()
    print(report)
    
    # Display cycle results
    print("MONITORING CYCLE RESULTS")
    print("="*30)
    print(f"Cycle Completed: {'✅' if cycle_result['monitoring_cycle_completed'] else '❌'}")
    print(f"Alerts Created: {cycle_result.get('alerts_created', 0)}")
    print(f"Trigger Checks: {'✅' if cycle_result.get('trigger_checks_completed', False) else '❌'}")
    
    if cycle_result.get('error'):
        print(f"Error: {cycle_result['error']}")

if __name__ == "__main__":
    main()