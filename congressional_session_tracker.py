#!/usr/bin/env python3
"""
Congressional Session Tracker
Automatically detects current Congress session and flags outdated data.

This module provides:
- Current Congress number calculation based on date
- Data currency validation 
- Automated alerts for Congressional transitions
- Historical session tracking
"""

import json
from datetime import datetime, date
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import sqlite3
import os

@dataclass
class CongressionalSession:
    """Congressional session metadata"""
    congress_number: int
    start_date: date
    end_date: date
    is_current: bool
    party_control_house: Optional[str] = None
    party_control_senate: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary with ISO date strings"""
        data = asdict(self)
        data['start_date'] = self.start_date.isoformat()
        data['end_date'] = self.end_date.isoformat()
        return data

class CongressionalSessionTracker:
    """Track Congressional sessions and detect data currency"""
    
    def __init__(self, db_path: str = "congress_sessions.db"):
        self.db_path = db_path
        self._setup_database()
        
    def _setup_database(self):
        """Initialize session tracking database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS congressional_sessions (
                congress_number INTEGER PRIMARY KEY,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                is_current BOOLEAN NOT NULL,
                party_control_house TEXT,
                party_control_senate TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS data_currency_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                congress_number INTEGER NOT NULL,
                check_date TEXT NOT NULL,
                is_current BOOLEAN NOT NULL,
                days_since_transition INTEGER,
                alert_triggered BOOLEAN DEFAULT FALSE,
                notes TEXT
            )
        """)
        
        conn.commit()
        conn.close()
        
    def get_current_congress(self) -> int:
        """
        Calculate current Congress number based on date.
        
        Congress numbering:
        - 119th Congress: January 3, 2025 - January 3, 2027
        - Each Congress is 2 years, starting on odd years
        - First Congress: 1789-1791
        
        Returns:
            Current Congress number
        """
        current_year = datetime.now().year
        current_date = datetime.now().date()
        
        # Congress starts on January 3 of odd years
        if current_year % 2 == 1:  # Odd year
            congress_start = date(current_year, 1, 3)
            if current_date >= congress_start:
                # Calculate Congress number (119th started in 2025)
                return 119 + ((current_year - 2025) // 2)
            else:
                # Before January 3, still in previous Congress
                return 119 + ((current_year - 2025 - 2) // 2)
        else:  # Even year
            # In the second year of a Congress
            return 119 + ((current_year - 2026) // 2)
    
    def get_congress_dates(self, congress_number: int) -> Tuple[date, date]:
        """
        Get start and end dates for a specific Congress.
        
        Args:
            congress_number: The Congress number (e.g., 119)
            
        Returns:
            Tuple of (start_date, end_date)
        """
        # Calculate the starting year for this Congress
        # 119th Congress started in 2025
        start_year = 2025 + ((congress_number - 119) * 2)
        
        start_date = date(start_year, 1, 3)
        end_date = date(start_year + 2, 1, 3)
        
        return start_date, end_date
    
    def is_data_current(self, data_congress: int) -> Tuple[bool, Dict]:
        """
        Check if database contains current Congress data.
        
        Args:
            data_congress: Congress number in the database
            
        Returns:
            Tuple of (is_current, status_info)
        """
        current_congress = self.get_current_congress()
        is_current = data_congress == current_congress
        
        if not is_current:
            current_start, current_end = self.get_congress_dates(current_congress)
            data_start, data_end = self.get_congress_dates(data_congress)
            
            days_behind = (datetime.now().date() - current_start).days
            
            status = {
                'is_current': False,
                'current_congress': current_congress,
                'data_congress': data_congress,
                'congress_gap': current_congress - data_congress,
                'days_since_transition': days_behind,
                'current_period': f"{current_start.year}-{current_end.year}",
                'data_period': f"{data_start.year}-{data_end.year}",
                'alert_level': 'HIGH' if days_behind > 30 else 'MEDIUM'
            }
        else:
            status = {
                'is_current': True,
                'current_congress': current_congress,
                'data_congress': data_congress,
                'status': 'UP_TO_DATE'
            }
            
        return is_current, status
    
    def flag_outdated_data(self, data_congress: int) -> Dict:
        """
        Alert system when data needs updating.
        
        Args:
            data_congress: Congress number in the database
            
        Returns:
            Alert information dictionary
        """
        is_current, status = self.is_data_current(data_congress)
        
        alert = {
            'timestamp': datetime.now().isoformat(),
            'alert_triggered': not is_current,
            'severity': status.get('alert_level', 'LOW'),
            'message': self._generate_alert_message(status),
            'status': status,
            'action_required': not is_current
        }
        
        # Log the check
        self._log_currency_check(data_congress, is_current, status)
        
        return alert
    
    def _generate_alert_message(self, status: Dict) -> str:
        """Generate human-readable alert message"""
        if status.get('is_current'):
            return "✅ Data is current for the active Congressional session"
        
        congress_gap = status.get('congress_gap', 0)
        days_behind = status.get('days_since_transition', 0)
        
        if congress_gap == 1:
            return f"⚠️ Database contains {status['data_congress']}th Congress data. " \
                   f"Current {status['current_congress']}th Congress started {days_behind} days ago. " \
                   f"Committee assignments and leadership positions may be outdated."
        else:
            return f"🚨 Database is {congress_gap} Congressional sessions behind! " \
                   f"Current: {status['current_congress']}th Congress, " \
                   f"Database: {status['data_congress']}th Congress. " \
                   f"Immediate update required."
    
    def _log_currency_check(self, data_congress: int, is_current: bool, status: Dict):
        """Log data currency check to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO data_currency_log 
            (congress_number, check_date, is_current, days_since_transition, alert_triggered, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            data_congress,
            datetime.now().isoformat(),
            is_current,
            status.get('days_since_transition', 0),
            not is_current,
            json.dumps(status)
        ))
        
        conn.commit()
        conn.close()
    
    def get_historical_sessions(self) -> List[CongressionalSession]:
        """Get list of recent Congressional sessions"""
        current_congress = self.get_current_congress()
        sessions = []
        
        # Include current + 2 previous + 1 future
        for congress_num in range(current_congress - 2, current_congress + 2):
            start_date, end_date = self.get_congress_dates(congress_num)
            is_current = congress_num == current_congress
            
            session = CongressionalSession(
                congress_number=congress_num,
                start_date=start_date,
                end_date=end_date,
                is_current=is_current
            )
            sessions.append(session)
            
        return sessions
    
    def export_session_report(self, filepath: str = None) -> str:
        """Export comprehensive session tracking report"""
        if not filepath:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = f"congressional_session_report_{timestamp}.json"
            
        current_congress = self.get_current_congress()
        sessions = self.get_historical_sessions()
        
        # Check current data status (assuming 118th Congress data)
        data_congress = 118  # Current database state
        is_current, status = self.is_data_current(data_congress)
        alert = self.flag_outdated_data(data_congress)
        
        report = {
            'report_timestamp': datetime.now().isoformat(),
            'current_congress': current_congress,
            'data_congress_in_db': data_congress,
            'data_currency_status': status,
            'alert_info': alert,
            'historical_sessions': [session.to_dict() for session in sessions],
            'recommendations': self._generate_recommendations(status)
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
            
        return filepath
    
    def _generate_recommendations(self, status: Dict) -> List[str]:
        """Generate actionable recommendations"""
        if status.get('is_current'):
            return [
                "✅ No action required - data is current",
                "💡 Consider setting up automated checks for future transitions",
                "📅 Next transition: January 3, 2027 (121st Congress)"
            ]
        
        days_behind = status.get('days_since_transition', 0)
        congress_gap = status.get('congress_gap', 0)
        
        recommendations = [
            f"🎯 UPDATE REQUIRED: Transition from {status['data_congress']}th to {status['current_congress']}th Congress",
            "📊 Update committee structures and assignments",
            "👥 Update member committee assignments and leadership positions",
            "🏛️ Verify new committee chairs and ranking members"
        ]
        
        if days_behind > 7:
            recommendations.extend([
                "⚠️ HIGH PRIORITY: Data is significantly outdated",
                "🔄 Consider implementing automated Congressional transition detection"
            ])
            
        if congress_gap > 1:
            recommendations.extend([
                "🚨 CRITICAL: Multiple Congressional sessions behind",
                "📚 May need complete database rebuild with current structure"
            ])
            
        return recommendations

def main():
    """Main function for testing and demonstration"""
    print("🏛️ Congressional Session Tracker")
    print("=" * 50)
    
    tracker = CongressionalSessionTracker()
    
    # Get current Congress information
    current_congress = tracker.get_current_congress()
    print(f"Current Congress: {current_congress}th Congress")
    
    # Check data currency (assuming we have 118th Congress data)
    data_congress = 118
    is_current, status = tracker.is_data_current(data_congress)
    
    print(f"\nDatabase contains: {data_congress}th Congress data")
    print(f"Data is current: {is_current}")
    
    if not is_current:
        print(f"Days since 119th Congress started: {status.get('days_since_transition', 0)}")
        print(f"Congress gap: {status.get('congress_gap', 0)} sessions behind")
    
    # Generate alert
    alert = tracker.flag_outdated_data(data_congress)
    print(f"\nAlert: {alert['message']}")
    
    # Export report
    report_file = tracker.export_session_report()
    print(f"\nReport exported to: {report_file}")
    
    # Show historical sessions
    print(f"\nRecent Congressional Sessions:")
    sessions = tracker.get_historical_sessions()
    for session in sessions:
        status_icon = "✅" if session.is_current else "📅"
        print(f"{status_icon} {session.congress_number}th Congress: {session.start_date} - {session.end_date}")

if __name__ == "__main__":
    main()