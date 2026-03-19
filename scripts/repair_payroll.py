import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import errors

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

try:
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    cursor = conn.cursor()
    
    # Ensure table exists first
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS payroll (
        id SERIAL PRIMARY KEY
    );
    """)
    print("Table 'payroll' verified.")

    # Add columns if they are missing
    columns_to_add = [
        ("worker_id", "INTEGER"),
        ("amount", "DOUBLE PRECISION"),
        ("payment_date", "DATE"),
        ("signature_data", "TEXT"),
        ("log_ids", "TEXT")
    ]
    
    for col_name, col_type in columns_to_add:
        try:
            cursor.execute(f"ALTER TABLE payroll ADD COLUMN {col_name} {col_type};")
            print(f"Added column {col_name}")
        except Exception as e:
            # Check for duplicate column error specifically
            if "already exists" in str(e):
                print(f"Column {col_name} already exists")
            else:
                print(f"Error adding {col_name}: {e}")

    cursor.close()
    conn.close()
    print("Database repair finished.")
except Exception as e:
    print(f"Connection error: {e}")
