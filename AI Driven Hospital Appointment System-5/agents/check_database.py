import sqlite3

conn = sqlite3.connect("doctor.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM doctors")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
