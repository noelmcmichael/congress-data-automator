from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

# --- Database Connection ---
def get_db_connection():
    """Establishes a connection to the database."""
    conn = psycopg2.connect(
        host="127.0.0.1",
        port="5432",
        user="noelmcmichael",
        dbname="congress_data"
    )
    return conn

# --- Routes ---
@app.route('/')
def index():
    """Main page, lists the manageable committees."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, name, chamber 
        FROM committees 
        WHERE chamber = 'Senate' AND name IN (
            'Commerce, Science, and Transportation', 
            'Judiciary', 
            'Banking, Housing, and Urban Affairs', 
            'Finance', 
            'Health, Education, Labor, and Pensions', 
            'Homeland Security and Governmental Affairs'
        )
        ORDER BY name;
    """)
    committees = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', committees=committees)

@app.route('/committee/<int:committee_id>')
def edit_committee(committee_id):
    """Page for editing a specific committee."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT id, name FROM committees WHERE id = %s", (committee_id,))
    committee = cur.fetchone()
    
    cur.execute("""
        SELECT m.id, m.first_name, m.last_name, m.state, ma.assignment_type
        FROM members m
        JOIN member_assignments ma ON m.id = ma.member_id
        WHERE ma.committee_id = %s
        ORDER BY m.last_name, m.first_name;
    """, (committee_id,))
    assigned_members = cur.fetchall()
    
    cur.execute("""
        SELECT id, first_name, last_name, state
        FROM members
        WHERE chamber = 'Senate' AND id NOT IN (
            SELECT member_id FROM member_assignments WHERE committee_id = %s
        )
        ORDER BY last_name, first_name;
    """, (committee_id,))
    unassigned_members = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return render_template(
        'edit_committee.html', 
        committee=committee, 
        assigned_members=assigned_members,
        unassigned_members=unassigned_members
    )

@app.route('/committee/<int:committee_id>/update', methods=['POST'])
def update_assignments(committee_id):
    """Handles bulk updates: role changes and removals."""
    conn = get_db_connection()
    cur = conn.cursor()

    # Handle removals
    removed_ids = request.form.getlist('remove_ids')
    if removed_ids:
        # Convert IDs to integers for the query
        removed_ids_int = [int(id) for id in removed_ids]
        cur.execute(
            "DELETE FROM member_assignments WHERE committee_id = %s AND member_id = ANY(%s)",
            (committee_id, removed_ids_int)
        )

    # Handle role changes
    for key, value in request.form.items():
        if key.startswith('role_'):
            member_id = int(key.split('_')[1])
            if str(member_id) not in removed_ids: # Don't update roles for members being removed
                cur.execute(
                    "UPDATE member_assignments SET assignment_type = %s WHERE committee_id = %s AND member_id = %s",
                    (value, committee_id, member_id)
                )

    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('edit_committee', committee_id=committee_id))

@app.route('/committee/<int:committee_id>/add_bulk', methods=['POST'])
def add_bulk(committee_id):
    """Handles bulk addition of members."""
    member_ids = request.form.getlist('member_ids')
    if member_ids:
        conn = get_db_connection()
        cur = conn.cursor()
        for member_id in member_ids:
            cur.execute(
                "INSERT INTO member_assignments (committee_id, member_id, status) VALUES (%s, %s, 'published') ON CONFLICT DO NOTHING",
                (committee_id, int(member_id))
            )
        conn.commit()
        cur.close()
        conn.close()
    return redirect(url_for('edit_committee', committee_id=committee_id))

if __name__ == '__main__':
    app.run(debug=True, port=5001)
