import sqlite3

conn = sqlite3.connect("problems.db")
cur = conn.cursor()
cur.execute("""
CREATE TABLE problems (
indx TEXT,
input TEXT,
output TEXT
)
""")
print("done")