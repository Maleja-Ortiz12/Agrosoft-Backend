import psycopg2
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

print(f"Connecting to: {DATABASE_URL.split('@')[0]}@...")

try:
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    # Check animal table
    cur.execute("SELECT COUNT(*) FROM animals;")
    count = cur.fetchone()[0]
    print(f"Total animals: {count}")
    
    # Check for null genders
    cur.execute("SELECT id, name, tag_id, gender FROM animals WHERE gender IS NULL;")
    null_genders = cur.fetchall()
    print(f"Animals with NULL gender: {len(null_genders)}")
    for row in null_genders:
        print(row)
        
    # Check for other potential issues (e.g. empty strings)
    cur.execute("SELECT id, name, tag_id, gender FROM animals WHERE gender = '';")
    empty_genders = cur.fetchall()
    print(f"Animals with empty string gender: {len(empty_genders)}")

    cur.close()
    conn.close()
except Exception as e:
    print(f"Error: {e}")
