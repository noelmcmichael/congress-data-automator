import psycopg2
from datetime import datetime

# --- 1. Configuration ---
COMMITTEE_NAME = "Commerce, Science, and Transportation"
OUTPUT_SQL_FILE = f"infrastructure/populate_commerce_committee_{datetime.now().strftime('%Y%m%d')}.sql"

# --- 2. User-Provided Roster ---
COMMERCE_ROSTER = {
    "Republican": [
        {"first_name": "Ted", "last_name": "Cruz", "state": "TX", "role": "chair"},
        {"first_name": "John", "last_name": "Thune", "state": "SD", "role": "member"},
        {"first_name": "Roger", "last_name": "Wicker", "state": "MS", "role": "member"},
        {"first_name": "Deb", "last_name": "Fischer", "state": "NE", "role": "member"},
        {"first_name": "Jerry", "last_name": "Moran", "state": "KS", "role": "member"},
        {"first_name": "Dan", "last_name": "Sullivan", "state": "AK", "role": "member"},
        {"first_name": "Marsha", "last_name": "Blackburn", "state": "TN", "role": "member"},
        {"first_name": "Todd", "last_name": "Young", "state": "IN", "role": "member"},
        {"first_name": "Ted", "last_name": "Budd", "state": "NC", "role": "member"},
        {"first_name": "Eric", "last_name": "Schmitt", "state": "MO", "role": "member"},
        {"first_name": "John", "last_name": "Curtis", "state": "UT", "role": "member"},
        {"first_name": "Bernie", "last_name": "Moreno", "state": "OH", "role": "member"},
        {"first_name": "Tim", "last_name": "Sheehy", "state": "MT", "role": "member"},
        {"first_name": "Shelley Moore", "last_name": "Capito", "state": "WV", "role": "member"},
        {"first_name": "Cynthia", "last_name": "Lummis", "state": "WY", "role": "member"},
    ],
    "Democratic": [
        {"first_name": "Maria", "last_name": "Cantwell", "state": "WA", "role": "ranking_member"},
        {"first_name": "Amy", "last_name": "Klobuchar", "state": "MN", "role": "member"},
        {"first_name": "Brian", "last_name": "Schatz", "state": "HI", "role": "member"},
        {"first_name": "Ed", "last_name": "Markey", "state": "MA", "role": "member"},
        {"first_name": "Gary", "last_name": "Peters", "state": "MI", "role": "member"},
        {"first_name": "Tammy", "last_name": "Baldwin", "state": "WI", "role": "member"},
        {"first_name": "Tammy", "last_name": "Duckworth", "state": "IL", "role": "member"},
        {"first_name": "Jacky", "last_name": "Rosen", "state": "NV", "role": "member"},
        {"first_name": "Ben Ray", "last_name": "Luján", "state": "NM", "role": "member"},
        {"first_name": "John", "last_name": "Hickenlooper", "state": "CO", "role": "member"},
        {"first_name": "John", "last_name": "Fetterman", "state": "PA", "role": "member"},
        {"first_name": "Andy", "last_name": "Kim", "state": "NJ", "role": "member"},
        {"first_name": "Lisa Blunt", "last_name": "Rochester", "state": "DE", "role": "member"},
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

        # Get Committee ID
        cur.execute("SELECT id FROM committees WHERE name = %s", (COMMITTEE_NAME,))
        committee_result = cur.fetchone()
        if not committee_result:
            print(f"Error: Committee '{COMMITTEE_NAME}' not found.")
            return
        committee_id = committee_result[0]
        print(f"Found Committee ID for '{COMMITTEE_NAME}': {committee_id}")

        # Find Member IDs
        members_with_ids = []
        all_members = COMMERCE_ROSTER["Republican"] + COMMERCE_ROSTER["Democratic"]
        for member in all_members:
            # Handle multi-part first names
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

        # Generate SQL Script
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
            f.write('\n'.join(sql))
        print(f"Successfully generated SQL script: {OUTPUT_SQL_FILE}")

    except psycopg2.Error as e:
        print(f"Database connection error: {e}")
    finally:
        if conn:
            conn.close()

# --- 4. Main Execution ---
if __name__ == "__main__":
    process_roster()
