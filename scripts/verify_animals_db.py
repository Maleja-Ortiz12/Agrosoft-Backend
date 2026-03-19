import sqlite3
import os

# Identify DB path
db_path = 'agrosoft.db' # Common default for this project

if not os.path.exists(db_path):
    # Try looking in backend dir
    db_path = os.path.join(os.getcwd(), 'agrosoft.db')

print(f"Checking DB at: {db_path}")

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if animals table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='animals';")
    table_exists = cursor.fetchone()
    
    if table_exists:
        cursor.execute("SELECT COUNT(*) FROM animals;")
        count = cursor.fetchone()[0]
        print(f"Found {count} animals in 'animals' table.")
        
        cursor.execute("SELECT id, name, tag, status FROM animals LIMIT 5;")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    else:
        print("Table 'animals' DOES NOT EXIST.")
        
    conn.close()
except Exception as e:
    print(f"Error: {e}")
