#!/usr/bin/env python3
"""
Congressional Session Monitor Service

This service monitors Congressional sessions, tracks transitions, and detects
when database data becomes outdated due to new Congressional sessions.

Key Functions:
- Current Congress detection (119th, 120th, etc.)
- Session transition monitoring
- Leadership transition detection
- Database currency validation
"""

import logging
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CongressionalSessionStatus(Enum):
    """Status of Congressional session data"""
    CURRENT = "current"
    OUTDATED = "outdated"
    TRANSITION = "transition"
    UNKNOWN = "unknown"

class PartyControl(Enum):
    """Party control types"""
    REPUBLICAN = "republican"
    DEMOCRATIC = "democratic"
    UNIFIED_REPUBLICAN = "unified_republican"
    UNIFIED_DEMOCRATIC = "unified_democratic"
    DIVIDED = "divided"

@dataclass
class CongressionalSession:
    """Congressional session information"""
    number: int
    start_date: datetime
    end_date: datetime
    house_majority: str
    senate_majority: str
    control_type: PartyControl
    is_current: bool

@dataclass
class SessionTransition:
    """Congressional session transition information"""
    from_session: int
    to_session: int
    transition_date: datetime
    party_control_change: bool
    leadership_changes_required: bool
    committee_changes_required: bool

class CongressionalSessionMonitor:
    """Monitor Congressional sessions and detect transitions"""
    
    def __init__(self, db_path: str = "congress_119th.db"):
        self.db_path = db_path
        self.current_session = self._determine_current_session()
        self.session_history = self._load_session_history()
        
    def _determine_current_session(self) -> CongressionalSession:
        """Determine the current Congressional session based on date"""
        current_date = datetime.now()
        
        # Congressional sessions start on January 3rd of odd-numbered years
        # 119th Congress: January 3, 2025 - January 3, 2027
        # 120th Congress: January 3, 2027 - January 3, 2029
        
        if current_date >= datetime(2025, 1, 3) and current_date < datetime(2027, 1, 3):
            return CongressionalSession(
                number=119,
                start_date=datetime(2025, 1, 3),
                end_date=datetime(2027, 1, 3),
                house_majority="Republican",
                senate_majority="Republican",
                control_type=PartyControl.UNIFIED_REPUBLICAN,
                is_current=True
            )
        elif current_date >= datetime(2027, 1, 3) and current_date < datetime(2029, 1, 3):
            return CongressionalSession(
                number=120,
                start_date=datetime(2027, 1, 3),
                end_date=datetime(2029, 1, 3),
                house_majority="TBD",  # Will be determined by elections
                senate_majority="TBD",
                control_type=PartyControl.DIVIDED,  # Default assumption
                is_current=True
            )
        else:
            # Fallback for testing or edge cases
            return CongressionalSession(
                number=119,
                start_date=datetime(2025, 1, 3),
                end_date=datetime(2027, 1, 3),
                house_majority="Republican",
                senate_majority="Republican",
                control_type=PartyControl.UNIFIED_REPUBLICAN,
                is_current=True
            )
    
    def _load_session_history(self) -> List[CongressionalSession]:
        """Load historical Congressional session data"""
        sessions = [
            CongressionalSession(
                number=117,
                start_date=datetime(2021, 1, 3),
                end_date=datetime(2023, 1, 3),
                house_majority="Democratic",
                senate_majority="Democratic",
                control_type=PartyControl.UNIFIED_DEMOCRATIC,
                is_current=False
            ),
            CongressionalSession(
                number=118,
                start_date=datetime(2023, 1, 3),
                end_date=datetime(2025, 1, 3),
                house_majority="Republican",
                senate_majority="Democratic",
                control_type=PartyControl.DIVIDED,
                is_current=False
            ),
            self.current_session
        ]
        return sessions
    
    def get_current_session(self) -> CongressionalSession:
        """Get the current Congressional session"""
        return self.current_session
    
    def get_session_status(self) -> CongressionalSessionStatus:
        """Determine if database is current with Congressional session"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check if database has current session data
                cursor.execute("""
                    SELECT COUNT(*) 
                    FROM congressional_sessions 
                    WHERE congress_number = ? AND is_current = 1
                """, (self.current_session.number,))
                
                current_session_count = cursor.fetchone()[0]
                
                if current_session_count > 0:
                    return CongressionalSessionStatus.CURRENT
                else:
                    return CongressionalSessionStatus.OUTDATED
                    
        except sqlite3.Error as e:
            logger.error(f"Database error checking session status: {e}")
            return CongressionalSessionStatus.UNKNOWN
    
    def detect_transition(self) -> Optional[SessionTransition]:
        """Detect if a Congressional session transition is occurring"""
        current_date = datetime.now()
        transition_window = timedelta(days=30)  # 30-day transition window
        
        for session in self.session_history:
            if session.is_current:
                continue
                
            # Check if we're within transition window of session end
            if (session.end_date - transition_window <= current_date <= session.end_date + transition_window):
                next_session = self._get_next_session(session.number)
                if next_session:
                    return SessionTransition(
                        from_session=session.number,
                        to_session=next_session.number,
                        transition_date=session.end_date,
                        party_control_change=session.control_type != next_session.control_type,
                        leadership_changes_required=True,
                        committee_changes_required=True
                    )
        
        return None
    
    def _get_next_session(self, session_number: int) -> Optional[CongressionalSession]:
        """Get the next Congressional session"""
        for session in self.session_history:
            if session.number == session_number + 1:
                return session
        return None
    
    def get_leadership_currency_status(self) -> Dict[str, any]:
        """Check if committee leadership data is current"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check committee chairs by party
                cursor.execute("""
                    SELECT c.name, m.party, cm.position
                    FROM committees_119th c
                    JOIN committee_memberships_119th cm ON c.id = cm.committee_id
                    JOIN members_119th m ON cm.member_id = m.id
                    WHERE cm.position = 'Chair'
                    ORDER BY c.name
                """)
                
                chairs = cursor.fetchall()
                
                # Analyze party control of chairs
                republican_chairs = sum(1 for chair in chairs if chair[1] == 'Republican')
                democratic_chairs = sum(1 for chair in chairs if chair[1] == 'Democratic')
                
                # Expected leadership based on current session
                expected_majority = self.current_session.house_majority
                
                status = {
                    'total_chairs': len(chairs),
                    'republican_chairs': republican_chairs,
                    'democratic_chairs': democratic_chairs,
                    'expected_majority': expected_majority,
                    'is_current': True,
                    'last_updated': datetime.now().isoformat()
                }
                
                # Determine if leadership is current
                if expected_majority == 'Republican':
                    status['is_current'] = republican_chairs > democratic_chairs
                elif expected_majority == 'Democratic':
                    status['is_current'] = democratic_chairs > republican_chairs
                
                return status
                
        except sqlite3.Error as e:
            logger.error(f"Database error checking leadership currency: {e}")
            return {'error': str(e), 'is_current': False}
    
    def get_data_freshness_report(self) -> Dict[str, any]:
        """Generate comprehensive data freshness report"""
        session_status = self.get_session_status()
        leadership_status = self.get_leadership_currency_status()
        transition = self.detect_transition()
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'current_session': {
                'number': self.current_session.number,
                'start_date': self.current_session.start_date.isoformat(),
                'end_date': self.current_session.end_date.isoformat(),
                'house_majority': self.current_session.house_majority,
                'senate_majority': self.current_session.senate_majority,
                'control_type': self.current_session.control_type.value
            },
            'session_status': session_status.value,
            'leadership_currency': leadership_status,
            'transition_detected': transition is not None,
            'transition_details': None,
            'recommendations': []
        }
        
        if transition:
            report['transition_details'] = {
                'from_session': transition.from_session,
                'to_session': transition.to_session,
                'transition_date': transition.transition_date.isoformat(),
                'party_control_change': transition.party_control_change,
                'leadership_changes_required': transition.leadership_changes_required,
                'committee_changes_required': transition.committee_changes_required
            }
        
        # Generate recommendations
        if session_status == CongressionalSessionStatus.OUTDATED:
            report['recommendations'].append({
                'type': 'critical',
                'message': f'Database contains outdated Congressional session data. Update to {self.current_session.number}th Congress.',
                'action': 'update_congressional_session'
            })
        
        if not leadership_status.get('is_current', False):
            report['recommendations'].append({
                'type': 'warning',
                'message': f'Committee leadership may be outdated. Expected {self.current_session.house_majority} majority chairs.',
                'action': 'update_committee_leadership'
            })
        
        if transition:
            report['recommendations'].append({
                'type': 'info',
                'message': f'Congressional transition detected: {transition.from_session}th → {transition.to_session}th Congress',
                'action': 'prepare_transition_update'
            })
        
        return report
    
    def create_monitoring_tables(self):
        """Create database tables for session monitoring"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Congressional sessions table - skip if exists
                cursor.execute("""
                    SELECT COUNT(*) FROM sqlite_master 
                    WHERE type='table' AND name='congressional_sessions'
                """)
                table_exists = cursor.fetchone()[0] > 0
                
                if not table_exists:
                    cursor.execute("""
                        CREATE TABLE congressional_sessions (
                            session_id INTEGER PRIMARY KEY,
                            congress_number INTEGER UNIQUE NOT NULL,
                            start_date TEXT NOT NULL,
                            end_date TEXT NOT NULL,
                            is_current BOOLEAN NOT NULL DEFAULT FALSE,
                            party_control_house TEXT,
                            party_control_senate TEXT,
                            created_at TEXT DEFAULT CURRENT_TIMESTAMP
                        )
                    """)
                
                # Data freshness log table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS data_freshness_log (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        check_type TEXT NOT NULL,
                        status TEXT NOT NULL,
                        details TEXT,
                        recommendations TEXT,
                        created_at TEXT DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Insert current session if not exists
                cursor.execute("""
                    INSERT OR REPLACE INTO congressional_sessions 
                    (congress_number, start_date, end_date, party_control_house, party_control_senate, is_current)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    self.current_session.number,
                    self.current_session.start_date.isoformat(),
                    self.current_session.end_date.isoformat(),
                    self.current_session.house_majority,
                    self.current_session.senate_majority,
                    1 if self.current_session.is_current else 0
                ))
                
                conn.commit()
                logger.info("Congressional session monitoring tables created successfully")
                
        except sqlite3.Error as e:
            logger.error(f"Error creating monitoring tables: {e}")
            raise

def main():
    """Main function for testing the Congressional Session Monitor"""
    monitor = CongressionalSessionMonitor()
    
    # Create monitoring tables
    monitor.create_monitoring_tables()
    
    # Generate data freshness report
    report = monitor.get_data_freshness_report()
    
    print("\n" + "="*60)
    print("CONGRESSIONAL SESSION MONITORING REPORT")
    print("="*60)
    print(f"Timestamp: {report['timestamp']}")
    print(f"Current Session: {report['current_session']['number']}th Congress")
    print(f"Session Status: {report['session_status']}")
    print(f"Leadership Currency: {'✅ Current' if report['leadership_currency']['is_current'] else '❌ Outdated'}")
    print(f"Transition Detected: {'✅ Yes' if report['transition_detected'] else '❌ No'}")
    
    if report['recommendations']:
        print("\nRecommendations:")
        for rec in report['recommendations']:
            icon = "🚨" if rec['type'] == 'critical' else "⚠️" if rec['type'] == 'warning' else "ℹ️"
            print(f"  {icon} {rec['message']}")
    
    print("\nLeadership Analysis:")
    leadership = report['leadership_currency']
    print(f"  Total Chairs: {leadership['total_chairs']}")
    print(f"  Republican Chairs: {leadership['republican_chairs']}")
    print(f"  Democratic Chairs: {leadership['democratic_chairs']}")
    print(f"  Expected Majority: {leadership['expected_majority']}")
    
    print("="*60)

if __name__ == "__main__":
    main()