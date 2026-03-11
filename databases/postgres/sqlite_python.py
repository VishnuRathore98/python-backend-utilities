import sqlite3

# Connect to database (creates file if not exists)
conn = sqlite3.connect("students.db")

# Create cursor
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER
)
""")

# Insert data
cursor.execute("INSERT INTO students (name, age) VALUES (?, ?)", ("Rahul", 20))
cursor.execute("INSERT INTO students (name, age) VALUES (?, ?)", ("Aman", 22))

# Save changes
conn.commit()

# Read data
cursor.execute("SELECT * FROM students")
rows = cursor.fetchall()

for row in rows:
    print(row)

# Close connection
conn.close()