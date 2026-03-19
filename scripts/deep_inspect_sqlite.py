import sqlite3
import os

db_path = 'c:/Users/malej/Documents/agrosoft/agrosoft.db'

print(f"Inspecting: {db_path}")
if not os.path.exists(db_path):
    print("File not found.")
else:
    print(f"Size: {os.path.getsize(db_path)} bytes")
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"Tables found: {tables}")
        
        for table in tables:
            tname = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {tname};")
            count = cursor.fetchone()[0]
            print(f"Table '{tname}': {count} records")
            if count > 0:
                cursor.execute(f"SELECT * FROM {tname} LIMIT 1;")
                print(f"  Sample: {cursor.fetchone()}")
        
        conn.close()
    except Exception as e:
        print(f"Error: {e}")
