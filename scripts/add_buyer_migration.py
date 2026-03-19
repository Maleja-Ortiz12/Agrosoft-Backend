import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def migrate():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        # Check if the column already exists
        cur.execute("""
            SELECT count(*) 
            FROM information_schema.columns 
            WHERE table_name='sales' AND column_name='buyer';
        """)
        
        if cur.fetchone()[0] == 0:
            print("Adding 'buyer' column to 'sales' table...")
            cur.execute("ALTER TABLE sales ADD COLUMN buyer VARCHAR;")
            conn.commit()
            print("Migration successful.")
        else:
            print("Column 'buyer' already exists in 'sales' table.")
            
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error during migration: {e}")

if __name__ == "__main__":
    migrate()
