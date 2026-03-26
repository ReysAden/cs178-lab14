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
    return """
    <h1>Lab 14 Flask App</h1>
    <p>Available routes:</p>
    <ul>
        <li><a href="/viewdb">/viewdb</a> - View first 10 tracks</li>
        <li><a href="/pricequerytextbox">/pricequerytextbox</a> - Query by price</li>
        <li><a href="/timequerytextbox">/timequerytextbox</a> - Query by duration</li>
        <li><a href="/artistquery/1">/artistquery/&lt;artist_id&gt;</a> - Query by artist</li>
    </ul>
    """


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
@app.route("/artistquery/<artist_id>")
def artistquery(artist_id):
    rows = execute_query("""
        SELECT ArtistId, Artist.Name, Track.Name, UnitPrice, Milliseconds
        FROM Artist
        JOIN Album USING (ArtistID)
        JOIN Track USING (AlbumID)
        JOIN MediaType USING (MediaTypeID)
        WHERE ArtistId = %s
        LIMIT 10
    """, (artist_id,))
    return display_html(rows)

@app.route("/pricequery/<price>")
def viewprices(price):
    rows = execute_query("""
        SELECT ArtistId, Artist.Name, Track.Name, UnitPrice, Milliseconds
        FROM Artist
        JOIN Album USING (ArtistID)
        JOIN Track USING (AlbumID)
        WHERE UnitPrice = %s
        ORDER BY Track.Name
        LIMIT 500
    """, (str(price),))
    return display_html(rows)


# TODO: Section 3 — add your /pricequerytextbox GET and POST routes here

@app.route("/pricequerytextbox", methods=['GET'])
def price_form():
    return render_template('textbox.html', fieldname="Price")

@app.route("/pricequerytextbox", methods=['POST'])
def price_form_post():
    text = request.form['text']
    return viewprices(text)


# TODO: Section 3 — add your /timequerytextbox GET and POST routes here

@app.route("/timequery/<time>")
def viewtime(time):
    rows = execute_query("""
        SELECT ArtistId, Artist.Name, Track.Name, UnitPrice, Milliseconds
        FROM Artist
        JOIN Album USING (ArtistID)
        JOIN Track USING (AlbumID)
        WHERE Milliseconds > %s
        ORDER BY Milliseconds DESC
        LIMIT 500
    """, (str(time),))
    return display_html(rows)

@app.route("/timequerytextbox", methods=['GET'])
def time_form():
    return render_template('textbox.html', fieldname="Time (ms)")

@app.route("/timequerytextbox", methods=['POST'])
def time_form_post():
    text = request.form['text']
    rows = execute_query("""
        SELECT ArtistId, Artist.Name, Track.Name, UnitPrice, Milliseconds
        FROM Artist
        JOIN Album USING (ArtistID)
        JOIN Track USING (AlbumID)
        WHERE Milliseconds > %s
        ORDER BY Milliseconds DESC
        LIMIT 500
    """, (str(text),))
    return display_html(rows)

# ---------------------------------------------------------------------------
# Run the app
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
