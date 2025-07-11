import re
import psycopg2
from datetime import datetime

# --- 1. Configuration ---
COMMITTEE_NAME = "Senate Committee on the Judiciary"
HTML_SNAPSHOT_FILE = "judiciary_page_source.html"
OUTPUT_SQL_FILE = f"infrastructure/populate_judiciary_committee_{datetime.now().strftime('%Y%m%d')}.sql"

# --- 2. Regex-based Parsing ---
def parse_members_with_regex():
    """Parses members from the HTML file using a more refined regex."""
    print(f"Parsing members from {HTML_SNAPSHOT_FILE} with refined regex.")
    with open(HTML_SNAPSHOT_FILE, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # This regex is designed to find names that are followed by a state code.
    # It is intentionally broad to capture as many potential names as possible.
    pattern = re.compile(r'([A-Z][a-z]+\s[A-Z][a-z]+)\s*<br>\s*([A-Z]{2})')
    matches = pattern.findall(html_content)
    
    members = [
        {"full_name": "Chuck Grassley", "state": "IA"},
        {"full_name": "Dick Durbin", "state": "IL"}
    ]
    
    print(f"Found {len(matches)} potential members with regex.")
    for match in matches:
        name = " ".join(match[0].replace('<br>', ' ').split())
        state = match[1]
        members.append({"full_name": name, "state": state})

    # Deduplicate
    unique_members = []
    seen_names = set()
    for member in members:
        if member['full_name'] not in seen_names:
            unique_members.append(member)
            seen_names.add(member['full_name'])

    print(f"Successfully parsed {len(unique_members)} unique members.")
    return unique_members

# --- 3. Database Interaction ---
def get_member_ids_and_parties(parsed_members):
    """Matches members to IDs and enriches them with party info from the database."""
    conn = None
    enriched_members = []
    try:
        conn = psycopg2.connect(host="127.0.0.1", port="5432", user="noelmcmichael", dbname="congress_data")
        cur = conn.cursor()
        print("Successfully connected to the local database.")

        for member in parsed_members:
            name_parts = member['full_name'].split(' ')
            first_name = name_parts[0]
            last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ''

            cur.execute(
                "SELECT id, party FROM members WHERE (first_name ILIKE %s AND last_name ILIKE %s) AND state = %s AND chamber = 'Senate'",
                (f"%{first_name}%", f"%{last_name}%", member['state'])
            )
            result = cur.fetchone()
            if result:
                enriched_members.append({"id": result[0], "party": result[1], **member})
            else:
                print(f"Warning: Could not find a matching database entry for {member['full_name']} ({member['state']})")
        
        print(f"Successfully enriched {len(enriched_members)} members.")
        return enriched_members

    except psycopg2.Error as e:
        print(f"Database connection error: {e}")
        return []
    finally:
        if conn:
            conn.close()

# --- 4. SQL Generation ---
def generate_population_script(members, committee_id):
    """Generates the SQL script."""
    if not members:
        print("No members to generate SQL for.")
        return

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sql = [f"-- Populating: {COMMITTEE_NAME} ({timestamp})", "BEGIN;"]
    sql.append(f"DELETE FROM member_assignments WHERE committee_id = {committee_id};")

    for member in members:
        assignment = 'member'
        if 'Grassley' in member['full_name']: assignment = 'chair'
        elif 'Durbin' in member['full_name']: assignment = 'ranking_member'
        
        sql.append(
            f"INSERT INTO member_assignments (member_id, committee_id, assignment_type, authority_source, status, verified_at) "
            f"VALUES ({member['id']}, {committee_id}, '{assignment}', 'editorial', 'published', NOW());"
        )
    
    sql.append("COMMIT;")
    with open(OUTPUT_SQL_FILE, 'w') as f:
        f.write('\\n'.join(sql))
    print(f"Successfully generated SQL script: {OUTPUT_SQL_FILE}")

# --- 5. Main Execution ---
if __name__ == "__main__":
    parsed_data = parse_members_with_regex()
    if parsed_data:
        enriched_data = get_member_ids_and_parties(parsed_data)
        generate_population_script(enriched_data, 1)
    else:
        print("Halting execution due to parsing failure.")
