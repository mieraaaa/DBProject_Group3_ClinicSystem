import sqlite3

DATABASE_FILE = 'clinic.db'
SCHEMA_FILE = 'clinic.sql' 

conn = sqlite3.connect(DATABASE_FILE)

print(f"Membaca skema dari {SCHEMA_FILE}...")

with open(SCHEMA_FILE) as f:
    schema_sql = f.read()

conn.executescript(schema_sql)

print(f"Database dan semua tabel berhasil dibuat di '{DATABASE_FILE}'")

conn.commit()
conn.close()