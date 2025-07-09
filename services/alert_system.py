#!/usr/bin/env python3
"""
Alert System Service

This service manages alerts and notifications for the Congressional Data Automator,
including email notifications, webhook integrations, and alert management.

Key Functions:
- Alert configuration and management
- Email notification system
- Webhook integration (Slack, Discord, etc.)
- Alert escalation and routing
"""

import logging
import sqlite3
import smtplib
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import json
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AlertSeverity(Enum):
    """Alert severity levels"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class AlertChannel(Enum):
    """Alert delivery channels"""
    EMAIL = "email"
    WEBHOOK = "webhook"
    SLACK = "slack"
    DISCORD = "discord"
    LOG = "log"

class AlertStatus(Enum):
    """Alert status"""
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"
    ACKNOWLEDGED = "acknowledged"

@dataclass
class Alert:
    """Alert definition"""
    id: str
    title: str
    message: str
    severity: AlertSeverity
    source: str
    channels: List[AlertChannel]
    created_at: datetime
    context: Dict[str, Any]
    status: AlertStatus = AlertStatus.PENDING
    sent_at: Optional[datetime] = None
    acknowledged_at: Optional[datetime] = None
    error: Optional[str] = None

@dataclass
class AlertRule:
    """Alert rule configuration"""
    id: str
    name: str
    condition: str
    severity: AlertSeverity
    channels: List[AlertChannel]
    enabled: bool
    cooldown_minutes: int
    escalation_rules: List[Dict[str, Any]]

class AlertSystem:
    """Manage alerts and notifications"""
    
    def __init__(self, db_path: str = "congress_119th.db"):
        self.db_path = db_path
        self.smtp_config = self._load_smtp_config()
        self.webhook_config = self._load_webhook_config()
        self.alert_rules = self._load_alert_rules()
        self._setup_database()
    
    def _load_smtp_config(self) -> Dict[str, Any]:
        """Load SMTP configuration from environment or defaults"""
        return {
            'smtp_server': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
            'smtp_port': int(os.getenv('SMTP_PORT', '587')),
            'smtp_username': os.getenv('SMTP_USERNAME', ''),
            'smtp_password': os.getenv('SMTP_PASSWORD', ''),
            'from_email': os.getenv('FROM_EMAIL', 'congress-monitor@example.com'),
            'to_emails': os.getenv('TO_EMAILS', '').split(',') if os.getenv('TO_EMAILS') else []
        }
    
    def _load_webhook_config(self) -> Dict[str, Any]:
        """Load webhook configuration from environment"""
        return {
            'slack_webhook': os.getenv('SLACK_WEBHOOK_URL', ''),
            'discord_webhook': os.getenv('DISCORD_WEBHOOK_URL', ''),
            'generic_webhook': os.getenv('GENERIC_WEBHOOK_URL', '')
        }
    
    def _load_alert_rules(self) -> Dict[str, AlertRule]:
        """Load alert rules configuration"""
        return {
            'data_freshness_critical': AlertRule(
                id='data_freshness_critical',
                name='Critical Data Freshness Issues',
                condition='data_freshness_status == "CRITICAL"',
                severity=AlertSeverity.CRITICAL,
                channels=[AlertChannel.EMAIL, AlertChannel.SLACK],
                enabled=True,
                cooldown_minutes=60,
                escalation_rules=[
                    {'delay_minutes': 30, 'channels': [AlertChannel.EMAIL]},
                    {'delay_minutes': 60, 'channels': [AlertChannel.SLACK]}
                ]
            ),
            'api_health_degraded': AlertRule(
                id='api_health_degraded',
                name='API Health Degraded',
                condition='api_health_status in ["DEGRADED", "UNHEALTHY", "CRITICAL"]',
                severity=AlertSeverity.WARNING,
                channels=[AlertChannel.EMAIL, AlertChannel.LOG],
                enabled=True,
                cooldown_minutes=30,
                escalation_rules=[]
            ),
            'congressional_transition': AlertRule(
                id='congressional_transition',
                name='Congressional Transition Detected',
                condition='congress_transition_detected == True',
                severity=AlertSeverity.INFO,
                channels=[AlertChannel.EMAIL, AlertChannel.SLACK],
                enabled=True,
                cooldown_minutes=1440,  # 24 hours
                escalation_rules=[]
            ),
            'leadership_changes': AlertRule(
                id='leadership_changes',
                name='Committee Leadership Changes',
                condition='leadership_changes_detected == True',
                severity=AlertSeverity.WARNING,
                channels=[AlertChannel.EMAIL],
                enabled=True,
                cooldown_minutes=180,  # 3 hours
                escalation_rules=[]
            ),
            'system_health_critical': AlertRule(
                id='system_health_critical',
                name='System Health Critical',
                condition='system_health_status == "CRITICAL"',
                severity=AlertSeverity.CRITICAL,
                channels=[AlertChannel.EMAIL, AlertChannel.SLACK],
                enabled=True,
                cooldown_minutes=15,
                escalation_rules=[
                    {'delay_minutes': 15, 'channels': [AlertChannel.EMAIL]},
                    {'delay_minutes': 30, 'channels': [AlertChannel.SLACK]}
                ]
            )
        }
    
    def _setup_database(self):
        """Setup database tables for alerts"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Alerts table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS alerts (
                        id TEXT PRIMARY KEY,
                        title TEXT NOT NULL,
                        message TEXT NOT NULL,
                        severity TEXT NOT NULL,
                        source TEXT NOT NULL,
                        channels TEXT NOT NULL,
                        created_at TEXT NOT NULL,
                        context TEXT,
                        status TEXT NOT NULL DEFAULT 'pending',
                        sent_at TEXT,
                        acknowledged_at TEXT,
                        error TEXT
                    )
                """)
                
                # Alert rules table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS alert_rules (
                        id TEXT PRIMARY KEY,
                        name TEXT NOT NULL,
                        condition TEXT NOT NULL,
                        severity TEXT NOT NULL,
                        channels TEXT NOT NULL,
                        enabled INTEGER DEFAULT 1,
                        cooldown_minutes INTEGER DEFAULT 60,
                        escalation_rules TEXT,
                        created_at TEXT DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Alert deliveries table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS alert_deliveries (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        alert_id TEXT NOT NULL,
                        channel TEXT NOT NULL,
                        status TEXT NOT NULL,
                        delivered_at TEXT,
                        error TEXT,
                        FOREIGN KEY (alert_id) REFERENCES alerts(id)
                    )
                """)
                
                conn.commit()
                logger.info("Alert system database tables created")
                
        except sqlite3.Error as e:
            logger.error(f"Error setting up alert database: {e}")
    
    def create_alert(self, title: str, message: str, severity: AlertSeverity, 
                    source: str, context: Dict[str, Any] = None) -> Alert:
        """Create a new alert"""
        alert_id = f"alert_{int(datetime.now().timestamp())}"
        
        # Determine channels based on severity
        if severity == AlertSeverity.CRITICAL:
            channels = [AlertChannel.EMAIL, AlertChannel.SLACK]
        elif severity == AlertSeverity.ERROR:
            channels = [AlertChannel.EMAIL]
        elif severity == AlertSeverity.WARNING:
            channels = [AlertChannel.EMAIL, AlertChannel.LOG]
        else:
            channels = [AlertChannel.LOG]
        
        alert = Alert(
            id=alert_id,
            title=title,
            message=message,
            severity=severity,
            source=source,
            channels=channels,
            created_at=datetime.now(),
            context=context or {}
        )
        
        # Save alert to database
        self._save_alert(alert)
        
        return alert
    
    def _save_alert(self, alert: Alert):
        """Save alert to database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO alerts 
                    (id, title, message, severity, source, channels, created_at, context, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    alert.id,
                    alert.title,
                    alert.message,
                    alert.severity.value,
                    alert.source,
                    json.dumps([c.value for c in alert.channels]),
                    alert.created_at.isoformat(),
                    json.dumps(alert.context),
                    alert.status.value
                ))
                
                conn.commit()
                
        except sqlite3.Error as e:
            logger.error(f"Error saving alert: {e}")
    
    def send_alert(self, alert: Alert) -> bool:
        """Send alert through configured channels"""
        success = True
        
        for channel in alert.channels:
            try:
                if channel == AlertChannel.EMAIL:
                    channel_success = self._send_email_alert(alert)
                elif channel == AlertChannel.SLACK:
                    channel_success = self._send_slack_alert(alert)
                elif channel == AlertChannel.WEBHOOK:
                    channel_success = self._send_webhook_alert(alert)
                elif channel == AlertChannel.LOG:
                    channel_success = self._send_log_alert(alert)
                else:
                    channel_success = False
                    logger.warning(f"Unknown alert channel: {channel}")
                
                # Record delivery attempt
                self._record_delivery(alert.id, channel, channel_success)
                
                if not channel_success:
                    success = False
                    
            except Exception as e:
                logger.error(f"Error sending alert via {channel}: {e}")
                self._record_delivery(alert.id, channel, False, str(e))
                success = False
        
        # Update alert status
        alert.status = AlertStatus.SENT if success else AlertStatus.FAILED
        alert.sent_at = datetime.now()
        self._update_alert_status(alert)
        
        return success
    
    def _send_email_alert(self, alert: Alert) -> bool:
        """Send email alert"""
        if not self.smtp_config['smtp_username'] or not self.smtp_config['to_emails']:
            logger.info("Email configuration not available, skipping email alert")
            return True  # Don't fail if email is not configured
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.smtp_config['from_email']
            msg['To'] = ', '.join(self.smtp_config['to_emails'])
            msg['Subject'] = f"[{alert.severity.value.upper()}] {alert.title}"
            
            # Create email body
            body = f"""
Congressional Data Automator Alert

Severity: {alert.severity.value.upper()}
Source: {alert.source}
Time: {alert.created_at.strftime('%Y-%m-%d %H:%M:%S')}

Message:
{alert.message}

Context:
{json.dumps(alert.context, indent=2) if alert.context else 'None'}

---
Congressional Data Automator
https://storage.googleapis.com/congressional-data-frontend/index.html
"""
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            server = smtplib.SMTP(self.smtp_config['smtp_server'], self.smtp_config['smtp_port'])
            server.starttls()
            server.login(self.smtp_config['smtp_username'], self.smtp_config['smtp_password'])
            server.send_message(msg)
            server.quit()
            
            logger.info(f"Email alert sent: {alert.title}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email alert: {e}")
            return False
    
    def _send_slack_alert(self, alert: Alert) -> bool:
        """Send Slack alert"""
        if not self.webhook_config['slack_webhook']:
            logger.info("Slack webhook not configured, skipping Slack alert")
            return True  # Don't fail if Slack is not configured
        
        try:
            # Format message for Slack
            color = {
                AlertSeverity.CRITICAL: "#ff0000",
                AlertSeverity.ERROR: "#ff9900",
                AlertSeverity.WARNING: "#ffff00",
                AlertSeverity.INFO: "#00ff00"
            }.get(alert.severity, "#808080")
            
            payload = {
                "attachments": [
                    {
                        "color": color,
                        "title": f"[{alert.severity.value.upper()}] {alert.title}",
                        "text": alert.message,
                        "fields": [
                            {"title": "Source", "value": alert.source, "short": True},
                            {"title": "Time", "value": alert.created_at.strftime('%Y-%m-%d %H:%M:%S'), "short": True}
                        ],
                        "footer": "Congressional Data Automator",
                        "ts": int(alert.created_at.timestamp())
                    }
                ]
            }
            
            response = requests.post(
                self.webhook_config['slack_webhook'],
                json=payload,
                timeout=10
            )
            
            response.raise_for_status()
            logger.info(f"Slack alert sent: {alert.title}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send Slack alert: {e}")
            return False
    
    def _send_webhook_alert(self, alert: Alert) -> bool:
        """Send generic webhook alert"""
        if not self.webhook_config['generic_webhook']:
            logger.info("Generic webhook not configured, skipping webhook alert")
            return True
        
        try:
            payload = {
                "id": alert.id,
                "title": alert.title,
                "message": alert.message,
                "severity": alert.severity.value,
                "source": alert.source,
                "created_at": alert.created_at.isoformat(),
                "context": alert.context
            }
            
            response = requests.post(
                self.webhook_config['generic_webhook'],
                json=payload,
                timeout=10
            )
            
            response.raise_for_status()
            logger.info(f"Webhook alert sent: {alert.title}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send webhook alert: {e}")
            return False
    
    def _send_log_alert(self, alert: Alert) -> bool:
        """Send log alert"""
        try:
            log_level = {
                AlertSeverity.CRITICAL: logging.CRITICAL,
                AlertSeverity.ERROR: logging.ERROR,
                AlertSeverity.WARNING: logging.WARNING,
                AlertSeverity.INFO: logging.INFO
            }.get(alert.severity, logging.INFO)
            
            logger.log(log_level, f"ALERT: {alert.title} - {alert.message}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send log alert: {e}")
            return False
    
    def _record_delivery(self, alert_id: str, channel: AlertChannel, success: bool, error: str = None):
        """Record alert delivery attempt"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO alert_deliveries 
                    (alert_id, channel, status, delivered_at, error)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    alert_id,
                    channel.value,
                    'sent' if success else 'failed',
                    datetime.now().isoformat() if success else None,
                    error
                ))
                
                conn.commit()
                
        except sqlite3.Error as e:
            logger.error(f"Error recording delivery: {e}")
    
    def _update_alert_status(self, alert: Alert):
        """Update alert status in database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    UPDATE alerts 
                    SET status = ?, sent_at = ?, acknowledged_at = ?, error = ?
                    WHERE id = ?
                """, (
                    alert.status.value,
                    alert.sent_at.isoformat() if alert.sent_at else None,
                    alert.acknowledged_at.isoformat() if alert.acknowledged_at else None,
                    alert.error,
                    alert.id
                ))
                
                conn.commit()
                
        except sqlite3.Error as e:
            logger.error(f"Error updating alert status: {e}")
    
    def process_monitoring_data(self, data: Dict[str, Any]) -> List[Alert]:
        """Process monitoring data and create alerts based on rules"""
        alerts = []
        
        # Check data freshness
        if data.get('data_freshness_status') == 'CRITICAL':
            alert = self.create_alert(
                title="Critical Data Freshness Issues Detected",
                message=f"Data freshness validation failed with {data.get('data_freshness_issues', 0)} critical issues",
                severity=AlertSeverity.CRITICAL,
                source="data_freshness_validator",
                context=data
            )
            alerts.append(alert)
        
        # Check API health
        if data.get('api_health_status') in ['DEGRADED', 'UNHEALTHY', 'CRITICAL']:
            alert = self.create_alert(
                title=f"API Health {data.get('api_health_status', 'UNKNOWN')}",
                message=f"API health check returned {data.get('api_health_status')} status",
                severity=AlertSeverity.WARNING if data.get('api_health_status') == 'DEGRADED' else AlertSeverity.ERROR,
                source="system_health_monitor",
                context=data
            )
            alerts.append(alert)
        
        # Check for Congressional transition
        if data.get('congress_transition_detected'):
            alert = self.create_alert(
                title="Congressional Transition Detected",
                message=f"Transition to {data.get('next_congress', 'unknown')}th Congress detected",
                severity=AlertSeverity.INFO,
                source="congressional_session_monitor",
                context=data
            )
            alerts.append(alert)
        
        # Check for leadership changes
        if data.get('leadership_changes_detected'):
            alert = self.create_alert(
                title="Committee Leadership Changes Detected",
                message="Changes in committee leadership positions detected",
                severity=AlertSeverity.WARNING,
                source="congressional_session_monitor",
                context=data
            )
            alerts.append(alert)
        
        # Check system health
        if data.get('system_health_status') == 'CRITICAL':
            alert = self.create_alert(
                title="System Health Critical",
                message=f"System health check failed with {data.get('critical_components', 0)} critical components",
                severity=AlertSeverity.CRITICAL,
                source="system_health_monitor",
                context=data
            )
            alerts.append(alert)
        
        # Send all created alerts
        for alert in alerts:
            self.send_alert(alert)
        
        return alerts
    
    def get_alert_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get alert history"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT * FROM alerts 
                    ORDER BY created_at DESC 
                    LIMIT ?
                """, (limit,))
                
                columns = [desc[0] for desc in cursor.description]
                alerts = [dict(zip(columns, row)) for row in cursor.fetchall()]
                
                return alerts
                
        except sqlite3.Error as e:
            logger.error(f"Error retrieving alert history: {e}")
            return []
    
    def test_alert_system(self) -> Dict[str, Any]:
        """Test alert system functionality"""
        logger.info("Testing alert system...")
        
        # Create test alert
        test_alert = self.create_alert(
            title="Alert System Test",
            message="This is a test alert to verify the alert system is working correctly.",
            severity=AlertSeverity.INFO,
            source="alert_system_test",
            context={"test": True, "timestamp": datetime.now().isoformat()}
        )
        
        # Send test alert
        success = self.send_alert(test_alert)
        
        # Get recent alerts
        recent_alerts = self.get_alert_history(limit=5)
        
        return {
            'test_alert_id': test_alert.id,
            'test_alert_sent': success,
            'recent_alerts_count': len(recent_alerts),
            'configured_channels': {
                'email': bool(self.smtp_config['smtp_username']),
                'slack': bool(self.webhook_config['slack_webhook']),
                'webhook': bool(self.webhook_config['generic_webhook'])
            }
        }

def main():
    """Main function for testing the Alert System"""
    alert_system = AlertSystem()
    
    # Test alert system
    test_results = alert_system.test_alert_system()
    
    print("\n" + "="*60)
    print("ALERT SYSTEM TEST RESULTS")
    print("="*60)
    print(f"Test Alert ID: {test_results['test_alert_id']}")
    print(f"Test Alert Sent: {'✅' if test_results['test_alert_sent'] else '❌'}")
    print(f"Recent Alerts: {test_results['recent_alerts_count']}")
    
    print("\nConfigured Channels:")
    for channel, configured in test_results['configured_channels'].items():
        print(f"  {channel.upper()}: {'✅' if configured else '❌'}")
    
    # Test different alert severities
    print("\nTesting different alert severities...")
    
    severities = [
        (AlertSeverity.INFO, "Information alert test"),
        (AlertSeverity.WARNING, "Warning alert test"),
        (AlertSeverity.ERROR, "Error alert test"),
        (AlertSeverity.CRITICAL, "Critical alert test")
    ]
    
    for severity, message in severities:
        alert = alert_system.create_alert(
            title=f"Test {severity.value.upper()} Alert",
            message=message,
            severity=severity,
            source="alert_system_test"
        )
        success = alert_system.send_alert(alert)
        print(f"  {severity.value.upper()}: {'✅' if success else '❌'}")
    
    print("="*60)

if __name__ == "__main__":
    main()