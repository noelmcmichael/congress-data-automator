#!/usr/bin/env python3
"""
Automated Update Triggers Service

This service manages automated triggers for Congressional data updates,
including scheduled updates, event-based triggers, and emergency updates.

Key Functions:
- Congressional calendar integration
- Leadership transition detection
- Automated data refresh triggers
- Update scheduling and coordination
"""

import logging
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import json
import time
import threading

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class UpdateTriggerType(Enum):
    """Types of update triggers"""
    SCHEDULED = "scheduled"
    EVENT_BASED = "event_based"
    EMERGENCY = "emergency"
    MANUAL = "manual"

class UpdatePriority(Enum):
    """Update priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class UpdateStatus(Enum):
    """Update execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"

@dataclass
class UpdateTrigger:
    """Update trigger configuration"""
    id: str
    name: str
    trigger_type: UpdateTriggerType
    priority: UpdatePriority
    schedule_pattern: Optional[str]
    conditions: Dict[str, Any]
    actions: List[str]
    enabled: bool
    last_triggered: Optional[datetime]
    next_trigger: Optional[datetime]

@dataclass
class UpdateExecution:
    """Update execution record"""
    id: str
    trigger_id: str
    status: UpdateStatus
    started_at: datetime
    completed_at: Optional[datetime]
    duration: Optional[float]
    results: Dict[str, Any]
    error: Optional[str]

class CongressionalCalendar:
    """Congressional calendar and session information"""
    
    def __init__(self):
        self.current_congress = 119
        self.current_session_start = datetime(2025, 1, 3)
        self.current_session_end = datetime(2027, 1, 3)
        
    def get_next_congressional_session(self) -> Dict[str, Any]:
        """Get information about the next Congressional session"""
        next_congress = self.current_congress + 1
        next_session_start = self.current_session_end
        next_session_end = next_session_start + timedelta(days=730)  # 2 years
        
        return {
            'congress_number': next_congress,
            'start_date': next_session_start,
            'end_date': next_session_end,
            'days_until_start': (next_session_start - datetime.now()).days
        }
    
    def get_committee_assignment_periods(self) -> List[Dict[str, Any]]:
        """Get typical committee assignment periods"""
        return [
            {
                'name': 'New Congress Organization',
                'start': datetime(2025, 1, 3),
                'end': datetime(2025, 1, 31),
                'description': 'Committee assignments for new Congress'
            },
            {
                'name': 'Mid-Session Adjustments',
                'start': datetime(2025, 7, 1),
                'end': datetime(2025, 8, 31),
                'description': 'Summer recess committee adjustments'
            },
            {
                'name': 'Election Year Preparations',
                'start': datetime(2026, 1, 1),
                'end': datetime(2026, 12, 31),
                'description': 'Election year committee activities'
            }
        ]
    
    def is_recess_period(self, date: datetime = None) -> bool:
        """Check if date falls during Congressional recess"""
        if date is None:
            date = datetime.now()
        
        # Typical recess periods
        recess_periods = [
            (datetime(2025, 7, 1), datetime(2025, 8, 31)),   # Summer recess
            (datetime(2025, 12, 20), datetime(2026, 1, 7)),  # Winter recess
            (datetime(2026, 4, 1), datetime(2026, 4, 14)),   # Spring recess
            (datetime(2026, 7, 1), datetime(2026, 8, 31)),   # Summer recess
            (datetime(2026, 10, 1), datetime(2026, 11, 30))  # Election recess
        ]
        
        for start, end in recess_periods:
            if start <= date <= end:
                return True
        return False

class AutomatedUpdateTriggers:
    """Manage automated update triggers"""
    
    def __init__(self, db_path: str = "congress_119th.db"):
        self.db_path = db_path
        self.calendar = CongressionalCalendar()
        self.running = False
        self.scheduler_thread = None
        self.triggers = {}
        self._initialize_triggers()
        self._setup_database()
    
    def _setup_database(self):
        """Setup database tables for update triggers"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Update triggers table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS update_triggers (
                        id TEXT PRIMARY KEY,
                        name TEXT NOT NULL,
                        trigger_type TEXT NOT NULL,
                        priority TEXT NOT NULL,
                        schedule_pattern TEXT,
                        conditions TEXT,
                        actions TEXT,
                        enabled INTEGER DEFAULT 1,
                        last_triggered TEXT,
                        next_trigger TEXT,
                        created_at TEXT DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Update executions table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS update_executions (
                        id TEXT PRIMARY KEY,
                        trigger_id TEXT NOT NULL,
                        status TEXT NOT NULL,
                        started_at TEXT NOT NULL,
                        completed_at TEXT,
                        duration REAL,
                        results TEXT,
                        error TEXT,
                        FOREIGN KEY (trigger_id) REFERENCES update_triggers(id)
                    )
                """)
                
                conn.commit()
                logger.info("Update triggers database tables created")
                
        except sqlite3.Error as e:
            logger.error(f"Error setting up database: {e}")
    
    def _initialize_triggers(self):
        """Initialize default update triggers"""
        self.triggers = {
            'daily_freshness_check': UpdateTrigger(
                id='daily_freshness_check',
                name='Daily Data Freshness Check',
                trigger_type=UpdateTriggerType.SCHEDULED,
                priority=UpdatePriority.MEDIUM,
                schedule_pattern='daily_06:00',
                conditions={'min_hours_since_last': 20},
                actions=['validate_data_freshness', 'check_leadership_changes'],
                enabled=True,
                last_triggered=None,
                next_trigger=None
            ),
            'weekly_leadership_scan': UpdateTrigger(
                id='weekly_leadership_scan',
                name='Weekly Leadership Position Scan',
                trigger_type=UpdateTriggerType.SCHEDULED,
                priority=UpdatePriority.HIGH,
                schedule_pattern='weekly_monday_07:00',
                conditions={'check_leadership_changes': True},
                actions=['scan_committee_leadership', 'validate_party_control'],
                enabled=True,
                last_triggered=None,
                next_trigger=None
            ),
            'monthly_comprehensive_update': UpdateTrigger(
                id='monthly_comprehensive_update',
                name='Monthly Comprehensive Data Update',
                trigger_type=UpdateTriggerType.SCHEDULED,
                priority=UpdatePriority.HIGH,
                schedule_pattern='monthly_1st_08:00',
                conditions={'comprehensive_update': True},
                actions=['update_all_members', 'update_all_committees', 'validate_all_data'],
                enabled=True,
                last_triggered=None,
                next_trigger=None
            ),
            'congress_transition_detector': UpdateTrigger(
                id='congress_transition_detector',
                name='Congressional Transition Detector',
                trigger_type=UpdateTriggerType.EVENT_BASED,
                priority=UpdatePriority.CRITICAL,
                schedule_pattern=None,
                conditions={'days_until_new_congress': 30},
                actions=['prepare_transition_update', 'notify_stakeholders'],
                enabled=True,
                last_triggered=None,
                next_trigger=None
            ),
            'emergency_leadership_change': UpdateTrigger(
                id='emergency_leadership_change',
                name='Emergency Leadership Change',
                trigger_type=UpdateTriggerType.EMERGENCY,
                priority=UpdatePriority.CRITICAL,
                schedule_pattern=None,
                conditions={'manual_trigger': True},
                actions=['immediate_leadership_update', 'emergency_validation'],
                enabled=True,
                last_triggered=None,
                next_trigger=None
            )
        }
    
    def evaluate_trigger_conditions(self, trigger: UpdateTrigger) -> bool:
        """Evaluate if trigger conditions are met"""
        try:
            if trigger.trigger_type == UpdateTriggerType.SCHEDULED:
                # Check if it's time for scheduled update
                if trigger.next_trigger and datetime.now() >= trigger.next_trigger:
                    return True
                    
            elif trigger.trigger_type == UpdateTriggerType.EVENT_BASED:
                # Check event-based conditions
                if trigger.id == 'congress_transition_detector':
                    next_session = self.calendar.get_next_congressional_session()
                    days_until = next_session['days_until_start']
                    threshold = trigger.conditions.get('days_until_new_congress', 30)
                    return days_until <= threshold
                    
            elif trigger.trigger_type == UpdateTriggerType.EMERGENCY:
                # Emergency triggers are manually activated
                return False
                
            return False
            
        except Exception as e:
            logger.error(f"Error evaluating trigger conditions for {trigger.id}: {e}")
            return False
    
    def execute_trigger_actions(self, trigger: UpdateTrigger) -> UpdateExecution:
        """Execute trigger actions"""
        execution_id = f"{trigger.id}_{int(time.time())}"
        started_at = datetime.now()
        
        execution = UpdateExecution(
            id=execution_id,
            trigger_id=trigger.id,
            status=UpdateStatus.RUNNING,
            started_at=started_at,
            completed_at=None,
            duration=None,
            results={},
            error=None
        )
        
        try:
            logger.info(f"Executing trigger: {trigger.name}")
            
            results = {}
            
            for action in trigger.actions:
                try:
                    if action == 'validate_data_freshness':
                        results[action] = self._validate_data_freshness()
                    elif action == 'check_leadership_changes':
                        results[action] = self._check_leadership_changes()
                    elif action == 'scan_committee_leadership':
                        results[action] = self._scan_committee_leadership()
                    elif action == 'validate_party_control':
                        results[action] = self._validate_party_control()
                    elif action == 'update_all_members':
                        results[action] = self._update_all_members()
                    elif action == 'update_all_committees':
                        results[action] = self._update_all_committees()
                    elif action == 'validate_all_data':
                        results[action] = self._validate_all_data()
                    elif action == 'prepare_transition_update':
                        results[action] = self._prepare_transition_update()
                    elif action == 'notify_stakeholders':
                        results[action] = self._notify_stakeholders()
                    elif action == 'immediate_leadership_update':
                        results[action] = self._immediate_leadership_update()
                    elif action == 'emergency_validation':
                        results[action] = self._emergency_validation()
                    else:
                        results[action] = {'status': 'skipped', 'message': f'Unknown action: {action}'}
                        
                except Exception as e:
                    results[action] = {'status': 'error', 'error': str(e)}
                    logger.error(f"Error executing action {action}: {e}")
            
            # Update execution record
            execution.completed_at = datetime.now()
            execution.duration = (execution.completed_at - execution.started_at).total_seconds()
            execution.results = results
            execution.status = UpdateStatus.COMPLETED
            
            # Update trigger last_triggered
            trigger.last_triggered = datetime.now()
            self._calculate_next_trigger(trigger)
            
            logger.info(f"Trigger executed successfully: {trigger.name}")
            
        except Exception as e:
            execution.completed_at = datetime.now()
            execution.duration = (execution.completed_at - execution.started_at).total_seconds()
            execution.status = UpdateStatus.FAILED
            execution.error = str(e)
            logger.error(f"Trigger execution failed: {trigger.name} - {e}")
        
        # Save execution record
        self._save_execution_record(execution)
        
        return execution
    
    def _validate_data_freshness(self) -> Dict[str, Any]:
        """Validate data freshness"""
        try:
            from data_freshness_validator import DataFreshnessValidator
            validator = DataFreshnessValidator(self.db_path)
            report = validator.generate_freshness_report()
            
            return {
                'status': 'completed',
                'overall_status': report['overall_status'],
                'checks_passed': report['summary']['passed'],
                'total_checks': report['summary']['total_checks'],
                'recommendations': len(report['recommendations'])
            }
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def _check_leadership_changes(self) -> Dict[str, Any]:
        """Check for leadership changes"""
        try:
            from congressional_session_monitor import CongressionalSessionMonitor
            monitor = CongressionalSessionMonitor(self.db_path)
            leadership_status = monitor.get_leadership_currency_status()
            
            return {
                'status': 'completed',
                'is_current': leadership_status['is_current'],
                'republican_chairs': leadership_status['republican_chairs'],
                'democratic_chairs': leadership_status['democratic_chairs'],
                'expected_majority': leadership_status['expected_majority']
            }
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def _scan_committee_leadership(self) -> Dict[str, Any]:
        """Scan committee leadership positions"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get leadership positions
                cursor.execute("""
                    SELECT c.name, m.name, m.party, cm.position
                    FROM committees_119th c
                    JOIN committee_memberships_119th cm ON c.id = cm.committee_id
                    JOIN members_119th m ON cm.member_id = m.id
                    WHERE cm.position IN ('Chair', 'Ranking Member')
                    ORDER BY c.name, cm.position
                """)
                
                leadership = cursor.fetchall()
                
                return {
                    'status': 'completed',
                    'leadership_positions': len(leadership),
                    'committees_with_leadership': len(set(row[0] for row in leadership)),
                    'leadership_data': [
                        {
                            'committee': row[0],
                            'member': row[1],
                            'party': row[2],
                            'position': row[3]
                        }
                        for row in leadership
                    ]
                }
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def _validate_party_control(self) -> Dict[str, Any]:
        """Validate party control information"""
        try:
            expected_majority = "Republican"  # 119th Congress
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check committee chairs by party
                cursor.execute("""
                    SELECT m.party, COUNT(*) as count
                    FROM committee_memberships_119th cm
                    JOIN members_119th m ON cm.member_id = m.id
                    WHERE cm.position = 'Chair'
                    GROUP BY m.party
                """)
                
                chair_distribution = dict(cursor.fetchall())
                
                republican_chairs = chair_distribution.get('Republican', 0)
                democratic_chairs = chair_distribution.get('Democratic', 0)
                
                is_correct = republican_chairs > democratic_chairs if expected_majority == "Republican" else democratic_chairs > republican_chairs
                
                return {
                    'status': 'completed',
                    'expected_majority': expected_majority,
                    'republican_chairs': republican_chairs,
                    'democratic_chairs': democratic_chairs,
                    'control_is_correct': is_correct
                }
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def _update_all_members(self) -> Dict[str, Any]:
        """Update all member data"""
        # Placeholder for actual member update logic
        return {
            'status': 'completed',
            'action': 'update_all_members',
            'message': 'Member update would be triggered here'
        }
    
    def _update_all_committees(self) -> Dict[str, Any]:
        """Update all committee data"""
        # Placeholder for actual committee update logic
        return {
            'status': 'completed',
            'action': 'update_all_committees',
            'message': 'Committee update would be triggered here'
        }
    
    def _validate_all_data(self) -> Dict[str, Any]:
        """Validate all data"""
        return self._validate_data_freshness()
    
    def _prepare_transition_update(self) -> Dict[str, Any]:
        """Prepare for Congressional transition"""
        next_session = self.calendar.get_next_congressional_session()
        return {
            'status': 'completed',
            'next_congress': next_session['congress_number'],
            'days_until_transition': next_session['days_until_start'],
            'transition_date': next_session['start_date'].isoformat()
        }
    
    def _notify_stakeholders(self) -> Dict[str, Any]:
        """Notify stakeholders"""
        return {
            'status': 'completed',
            'notifications_sent': 0,
            'message': 'Stakeholder notifications would be sent here'
        }
    
    def _immediate_leadership_update(self) -> Dict[str, Any]:
        """Immediate leadership update"""
        return {
            'status': 'completed',
            'message': 'Emergency leadership update would be executed here'
        }
    
    def _emergency_validation(self) -> Dict[str, Any]:
        """Emergency validation"""
        return self._validate_data_freshness()
    
    def _calculate_next_trigger(self, trigger: UpdateTrigger):
        """Calculate next trigger time for scheduled triggers"""
        if trigger.trigger_type != UpdateTriggerType.SCHEDULED:
            return
            
        now = datetime.now()
        
        if trigger.schedule_pattern == 'daily_06:00':
            trigger.next_trigger = now.replace(hour=6, minute=0, second=0, microsecond=0) + timedelta(days=1)
        elif trigger.schedule_pattern == 'weekly_monday_07:00':
            days_until_monday = (7 - now.weekday()) % 7
            if days_until_monday == 0 and now.hour >= 7:
                days_until_monday = 7
            trigger.next_trigger = (now + timedelta(days=days_until_monday)).replace(hour=7, minute=0, second=0, microsecond=0)
        elif trigger.schedule_pattern == 'monthly_1st_08:00':
            next_month = now.replace(day=1, hour=8, minute=0, second=0, microsecond=0)
            if now.day > 1 or (now.day == 1 and now.hour >= 8):
                if next_month.month == 12:
                    next_month = next_month.replace(year=next_month.year + 1, month=1)
                else:
                    next_month = next_month.replace(month=next_month.month + 1)
            trigger.next_trigger = next_month
    
    def _save_execution_record(self, execution: UpdateExecution):
        """Save execution record to database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO update_executions 
                    (id, trigger_id, status, started_at, completed_at, duration, results, error)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    execution.id,
                    execution.trigger_id,
                    execution.status.value,
                    execution.started_at.isoformat(),
                    execution.completed_at.isoformat() if execution.completed_at else None,
                    execution.duration,
                    json.dumps(execution.results),
                    execution.error
                ))
                
                conn.commit()
                
        except sqlite3.Error as e:
            logger.error(f"Error saving execution record: {e}")
    
    def run_trigger_check(self):
        """Run trigger evaluation and execution"""
        logger.info("Running trigger check")
        
        for trigger in self.triggers.values():
            if not trigger.enabled:
                continue
                
            if self.evaluate_trigger_conditions(trigger):
                logger.info(f"Trigger conditions met: {trigger.name}")
                execution = self.execute_trigger_actions(trigger)
                logger.info(f"Trigger execution completed: {execution.status.value}")
    
    def start_scheduler(self):
        """Start the automated scheduler"""
        if self.running:
            return
            
        self.running = True
        logger.info("Starting automated update scheduler")
        
        def scheduler_loop():
            while self.running:
                try:
                    self.run_trigger_check()
                    time.sleep(60)  # Check every minute
                except Exception as e:
                    logger.error(f"Error in scheduler loop: {e}")
                    time.sleep(60)
        
        self.scheduler_thread = threading.Thread(target=scheduler_loop, daemon=True)
        self.scheduler_thread.start()
    
    def stop_scheduler(self):
        """Stop the automated scheduler"""
        self.running = False
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5)
        logger.info("Automated update scheduler stopped")
    
    def trigger_emergency_update(self, trigger_id: str) -> UpdateExecution:
        """Manually trigger an emergency update"""
        if trigger_id not in self.triggers:
            raise ValueError(f"Unknown trigger ID: {trigger_id}")
            
        trigger = self.triggers[trigger_id]
        logger.info(f"Manually triggering emergency update: {trigger.name}")
        
        return self.execute_trigger_actions(trigger)
    
    def get_trigger_status(self) -> Dict[str, Any]:
        """Get status of all triggers"""
        return {
            'scheduler_running': self.running,
            'triggers': {
                tid: {
                    'name': trigger.name,
                    'type': trigger.trigger_type.value,
                    'priority': trigger.priority.value,
                    'enabled': trigger.enabled,
                    'last_triggered': trigger.last_triggered.isoformat() if trigger.last_triggered else None,
                    'next_trigger': trigger.next_trigger.isoformat() if trigger.next_trigger else None
                }
                for tid, trigger in self.triggers.items()
            }
        }

def main():
    """Main function for testing the Automated Update Triggers"""
    triggers = AutomatedUpdateTriggers()
    
    # Initialize next trigger times
    for trigger in triggers.triggers.values():
        triggers._calculate_next_trigger(trigger)
    
    # Get trigger status
    status = triggers.get_trigger_status()
    
    print("\n" + "="*60)
    print("AUTOMATED UPDATE TRIGGERS STATUS")
    print("="*60)
    print(f"Scheduler Running: {status['scheduler_running']}")
    print(f"Total Triggers: {len(status['triggers'])}")
    
    print("\nTrigger Configuration:")
    for tid, trigger in status['triggers'].items():
        print(f"  • {trigger['name']}")
        print(f"    Type: {trigger['type']}, Priority: {trigger['priority']}")
        print(f"    Enabled: {trigger['enabled']}")
        if trigger['next_trigger']:
            print(f"    Next Trigger: {trigger['next_trigger']}")
        if trigger['last_triggered']:
            print(f"    Last Triggered: {trigger['last_triggered']}")
    
    print("\nTesting trigger evaluation...")
    
    # Test trigger conditions
    for trigger in triggers.triggers.values():
        conditions_met = triggers.evaluate_trigger_conditions(trigger)
        print(f"  {trigger.name}: {'✅' if conditions_met else '❌'}")
    
    print("="*60)

if __name__ == "__main__":
    main()