import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

try:
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    cur.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE  table_schema = 'public'
            AND    table_name   = 'animals'
        );
    """)
    exists = cur.fetchone()[0]
    print(f"Table 'animals' exists: {exists}")
    
    if exists:
        cur.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'animals';")
        cols = cur.fetchall()
        print("Columns:")
        for col in cols:
            print(f" - {col[0]}: {col[1]}")
            
    cur.close()
    conn.close()
except Exception as e:
    print(f"Error: {e}")
