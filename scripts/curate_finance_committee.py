import requests
from bs4 import BeautifulSoup
import psycopg2
from datetime import datetime

# --- 1. Configuration ---
COMMITTEE_NAME = "Finance"
COMMITTEE_URL = "https://www.finance.senate.gov/about/membership"
OUTPUT_SQL_FILE = f"infrastructure/populate_finance_committee_{datetime.now().strftime('%Y%m%d')}.sql"

# --- 2. Web Scraping ---
def scrape_finance_committee():
    """Scrapes the Finance Committee membership page."""
    print(f"Scraping members from: {COMMITTEE_URL}")
    try:
        response = requests.get(COMMITTEE_URL, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        members = []
        # The members are in 'div' elements with the class 'element-wrapper'
        for member_div in soup.find_all('div', class_='element-wrapper'):
            name_tag = member_div.find(['h3', 'h4', 'p'])
            if name_tag:
                # Name and state are often in the same tag, need to parse carefully
                text_content = name_tag.text.strip()
                # Example: "Michael F. Bennet (D - CO)"
                if '(' in text_content and ')' in text_content:
                    name = text_content.split('(')[0].strip()
                    details = text_content.split('(')[1].split(')')[0]
                    party = 'Democratic' if 'D' in details else 'Republican'
                    state = details.split('-')[-1].strip()
                    
                    # Handle multi-part first names
                    name_parts = name.split(' ')
                    first_name = name_parts[0]
                    last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ''
                    
                    # Special handling for the chairman, who has a different structure
                    if "Mike Crapo" in name:
                         role = "chair"
                    elif "Ron Wyden" in name: # Ranking member based on common knowledge
                        role = "ranking_member"
                    else:
                        role = "member"

                    members.append({
                        "first_name": first_name, 
                        "last_name": last_name, 
                        "state": state, 
                        "party": party,
                        "role": role
                    })

        print(f"Successfully scraped {len(members)} members.")
        return members
    except requests.exceptions.RequestException as e:
        print(f"Error scraping URL: {e}")
        return []

# --- 3. Database Interaction and SQL Generation ---
def process_roster(scraped_members):
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
        for member in scraped_members:
            cur.execute(
                "SELECT id FROM members WHERE first_name = %s AND last_name = %s AND state = %s AND chamber = 'Senate'",
                (member['first_name'], member['last_name'], member['state'])
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
            f"-- Generated on: {timestamp} from {COMMITTEE_URL}",
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
    scraped_data = scrape_finance_committee()
    if scraped_data:
        process_roster(scraped_data)
    else:
        print("Halting execution due to scraping failure.")
