#!/usr/bin/env python3
"""Check current production database state."""

import psycopg2

def main():
    # Connect to production database
    conn = psycopg2.connect(
        host="127.0.0.1",
        port=5433,
        database="congress_data",
        user="postgres",
        password="mDf3S9ZnBpQqJvGsY1"
    )

    with conn.cursor() as cur:
        # Check current max IDs
        cur.execute("SELECT MAX(id) FROM members")
        max_member_id = cur.fetchone()[0]
        
        cur.execute("SELECT MAX(id) FROM committees")
        max_committee_id = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM members WHERE congress_session = 119")
        congress_119_members = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM committees WHERE congress_session = 119")
        congress_119_committees = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM congressional_sessions WHERE congress_number = 119")
        has_119th_session = cur.fetchone()[0]
        
        print(f"Production Database State:")
        print(f"  Max Member ID: {max_member_id}")
        print(f"  Max Committee ID: {max_committee_id}")
        print(f"  119th Congress Members: {congress_119_members}")
        print(f"  119th Congress Committees: {congress_119_committees}")
        print(f"  119th Session Record: {has_119th_session}")
        
        # Check some specific 119th Congress members
        cur.execute("SELECT first_name, last_name, party, chamber FROM members WHERE congress_session = 119 LIMIT 5")
        members = cur.fetchall()
        print(f"\nSample 119th Congress Members:")
        for member in members:
            print(f"  {member[0]} {member[1]} ({member[2]}, {member[3]})")

    conn.close()

if __name__ == "__main__":
    main()