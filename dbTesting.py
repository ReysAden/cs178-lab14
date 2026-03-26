import pymysql
import creds  # download creds.py from Blackboard — do NOT push to GitHub


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
    args: optional tuple of parameters for parameterized queries.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, args)
    rows = cursor.fetchall()
    conn.close()
    return rows


# ---------------------------------------------------------------------------
# Test query — run this file directly to verify your connection works:
#   python3 dbTesting.py
# ---------------------------------------------------------------------------

rows = execute_query("""
    SELECT ArtistId, Artist.Name, Track.Name, UnitPrice, Milliseconds
    FROM Artist
    JOIN Album USING (ArtistID)
    JOIN Track USING (AlbumID)
    JOIN MediaType USING (MediaTypeID)
                     
    LIMIT 10
""")

for row in rows:
    print(row[0], row[1], row[2], row[3], row[4])

# TODO: Exercise 1 — modify the query above to also return the Milliseconds column
