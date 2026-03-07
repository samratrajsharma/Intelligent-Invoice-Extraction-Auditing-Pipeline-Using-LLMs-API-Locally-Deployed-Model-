import sqlite3

conn = sqlite3.connect("finops.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM documents")
print(cursor.fetchall())