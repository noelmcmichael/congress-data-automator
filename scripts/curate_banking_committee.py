import psycopg2
from datetime import datetime

# --- 1. Configuration ---
COMMITTEE_NAME = "Banking, Housing, and Urban Affairs"
OUTPUT_SQL_FILE = f"infrastructure/populate_banking_committee_{datetime.now().strftime('%Y%m%d')}.sql"

# --- 2. User-Provided Roster ---
BANKING_ROSTER = {
    "Republican": [
        {"first_name": "Tim", "last_name": "Scott", "state": "SC", "role": "chair"},
        {"first_name": "Mike", "last_name": "Crapo", "state": "ID", "role": "member"},
        {"first_name": "Mike", "last_name": "Rounds", "state": "SD", "role": "member"},
        {"first_name": "Thom", "last_name": "Tillis", "state": "NC", "role": "member"},
        {"first_name": "John", "last_name": "Kennedy", "state": "LA", "role": "member"},
        {"first_name": "Bill", "last_name": "Hagerty", "state": "TN", "role": "member"},
        {"first_name": "Cynthia", "last_name": "Lummis", "state": "WY", "role": "member"},
        {"first_name": "Katie", "last_name": "Britt", "state": "AL", "role": "member"},
        {"first_name": "Pete", "last_name": "Ricketts", "state": "NE", "role": "member"},
        {"first_name": "Jim", "last_name": "Banks", "state": "IN", "role": "member"},
        {"first_name": "Kevin", "last_name": "Cramer", "state": "ND", "role": "member"},
        {"first_name": "Bernie", "last_name": "Moreno", "state": "OH", "role": "member"},
        {"first_name": "Dave", "last_name": "McCormick", "state": "PA", "role": "member"},
    ],
    "Democratic": [
        {"first_name": "Elizabeth", "last_name": "Warren", "state": "MA", "role": "ranking_member"},
        {"first_name": "Jack", "last_name": "Reed", "state": "RI", "role": "member"},
        {"first_name": "Mark", "last_name": "Warner", "state": "VA", "role": "member"},
        {"first_name": "Chris", "last_name": "Van Hollen", "state": "MD", "role": "member"},
        {"first_name": "Catherine", "last_name": "Cortez Masto", "state": "NV", "role": "member"},
        {"first_name": "Tina", "last_name": "Smith", "state": "MN", "role": "member"},
        {"first_name": "Raphael", "last_name": "Warnock", "state": "GA", "role": "member"},
        {"first_name": "Andy", "last_name": "Kim", "state": "NJ", "role": "member"},
        {"first_name": "Ruben", "last_name": "Gallego", "state": "AZ", "role": "member"},
        {"first_name": "Lisa Blunt", "last_name": "Rochester", "state": "DE", "role": "member"},
        {"first_name": "Angela", "last_name": "Alsobrooks", "state": "MD", "role": "member"},
    ]
}

# --- 3. Database Interaction and SQL Generation ---
def process_roster():
    """Processes the roster, finds member IDs, and generates a SQL script."""
    conn = None
    try:
        conn = psycopg2.connect(host="127.0.0.1", port="5432", user="noelmcmichael", dbname="congress_data")
        cur = conn.cursor()
        print("Successfully connected to the local database.")

        cur.execute("SELECT id FROM committees WHERE name = %s", (COMMITTEE_NAME,))
        committee_result = cur.fetchone()
        if not committee_result:
            print(f"Error: Committee '{COMMITTEE_NAME}' not found.")
            return
        committee_id = committee_result[0]
        print(f"Found Committee ID for '{COMMITTEE_NAME}': {committee_id}")

        members_with_ids = []
        all_members = BANKING_ROSTER["Republican"] + BANKING_ROSTER["Democratic"]
        for member in all_members:
            first_name_like = member['first_name'].split(' ')[0]
            cur.execute(
                "SELECT id FROM members WHERE first_name ILIKE %s AND last_name = %s AND state = %s AND chamber = 'Senate'",
                (f"{first_name_like}%", member['last_name'], member['state'])
            )
            member_result = cur.fetchone()
            if member_result:
                members_with_ids.append({"id": member_result[0], **member})
            else:
                print(f"Warning: Could not find DB entry for {member['first_name']} {member['last_name']} ({member['state']})")

        print(f"Successfully matched {len(members_with_ids)} members to database IDs.")

        if not members_with_ids:
            print("No members matched. Aborting SQL generation.")
            return
            
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql = [
            f"-- Populating: {COMMITTEE_NAME}",
            f"-- Generated on: {timestamp} from user-provided list.",
            "BEGIN;",
            f"DELETE FROM member_assignments WHERE committee_id = {committee_id};"
        ]

        for member in members_with_ids:
            sql.append(
                f"INSERT INTO member_assignments (member_id, committee_id, assignment_type, authority_source, status, verified_at) "
                f"VALUES ({member['id']}, {committee_id}, '{member['role']}', 'editorial', 'published', NOW());"
            )
        
        sql.append("COMMIT;")
        
        with open(OUTPUT_SQL_FILE, 'w') as f:
            f.write('\\n'.join(sql))
        print(f"Successfully generated SQL script: {OUTPUT_SQL_FILE}")

    except psycopg2.Error as e:
        print(f"Database connection error: {e}")
    finally:
        if conn:
            conn.close()

# --- 4. Main Execution ---
if __name__ == "__main__":
    process_roster()
