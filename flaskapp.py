from flask import Flask, render_template, request
import pymysql
import creds  # download creds.py from Blackboard — do NOT push to GitHub

app = Flask(__name__)


# ---------------------------------------------------------------------------
# Database helpers
# ---------------------------------------------------------------------------

def get_connection():
    """Opens and returns a connection to the RDS MySQL database."""
    return pymysql.connect(
        host=creds.host,
        user=creds.user,
        password=creds.password,
        db=creds.db
    )

def execute_query(query, args=()):
    """
    Runs a SQL query and returns all result rows as a list of tuples.
    Always use parameterized queries (args) when inserting user input —
    never build SQL strings with f-strings or concatenation.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, args)
    rows = cursor.fetchall()
    conn.close()
    return rows

def display_html(rows):
    """
    Converts query result rows into a simple HTML table string.
    Flask routes can return this directly as a response.
    """
    html = "<table border='1'>"
    for row in rows:
        html += "<tr>"
        for col in row:
            html += f"<td>{col}</td>"
        html += "</tr>"
    html += "</table>"
    return html


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    return "<h1>Lab 14 Flask App</h1><p>Your routes go below this one.</p>"


# TODO: Section 1 — add your dbTesting code to dbTesting.py (not here)

# TODO: Section 2 — add your /viewdb route here

@app.route("/viewdb")
def viewdb():
    rows = execute_query("""
        SELECT ArtistId, Artist.Name, Track.Name, UnitPrice, Milliseconds
        FROM Artist
        JOIN Album USING (ArtistID)
        JOIN Track USING (AlbumID)
        JOIN MediaType USING (MediaTypeID)
                         
        LIMIT 10
    """)
    return display_html(rows)

# TODO: Section 2 — add your /artistquery/<artist_id> route here

# TODO: Section 3 — add your /pricequerytextbox GET and POST routes here

# TODO: Section 3 — add your /timequerytextbox GET and POST routes here


# ---------------------------------------------------------------------------
# Run the app
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
