#!/usr/bin/env python3
"""
Check which senators are causing the excess
"""

import psycopg2
from psycopg2.extras import RealDictCursor

def check_excess_senators():
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5433,
            database="congress_data",
            user="postgres",
            password="mDf3S9ZnBpQqJvGsY1"
        )
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Check Florida senators
        cursor.execute("""
            SELECT bioguide_id, first_name, last_name, party, term_start, term_end
            FROM members
            WHERE state = 'FL' AND chamber = 'Senate'
            ORDER BY last_name
        """)
        fl_senators = cursor.fetchall()
        
        print("📊 FLORIDA SENATORS:")
        for senator in fl_senators:
            print(f"   {senator['first_name']} {senator['last_name']} ({senator['party']}) - {senator['term_start']} to {senator['term_end']}")
        
        # Check Ohio senators
        cursor.execute("""
            SELECT bioguide_id, first_name, last_name, party, term_start, term_end
            FROM members
            WHERE state = 'OH' AND chamber = 'Senate'
            ORDER BY last_name
        """)
        oh_senators = cursor.fetchall()
        
        print("\n📊 OHIO SENATORS:")
        for senator in oh_senators:
            print(f"   {senator['first_name']} {senator['last_name']} ({senator['party']}) - {senator['term_start']} to {senator['term_end']}")
        
        # Check if there are any senators with expired terms
        cursor.execute("""
            SELECT state, first_name, last_name, party, term_start, term_end
            FROM members
            WHERE chamber = 'Senate' AND term_end < '2025-01-01'
            ORDER BY state, last_name
        """)
        expired_senators = cursor.fetchall()
        
        if expired_senators:
            print("\n⚠️  SENATORS WITH EXPIRED TERMS:")
            for senator in expired_senators:
                print(f"   {senator['first_name']} {senator['last_name']} ({senator['party']}-{senator['state']}) - Expired: {senator['term_end']}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_excess_senators()