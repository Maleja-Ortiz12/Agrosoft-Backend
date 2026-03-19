import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def fix_db():
    db_url = os.getenv("DATABASE_URL")
    print(f"Connecting to: {db_url}")
    
    try:
        conn = psycopg2.connect(db_url)
        conn.autocommit = True
        cursor = conn.cursor()
        
        print("Alter columns to be nullable...")
        # Make birth_date and name nullable
        cursor.execute("ALTER TABLE animals ALTER COLUMN birth_date DROP NOT NULL;")
        cursor.execute("ALTER TABLE animals ALTER COLUMN name DROP NOT NULL;")
        
        # Ensure age and image_path are present (just in case)
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'animals';
        """)
        columns = [row[0] for row in cursor.fetchall()]
        
        if 'age' not in columns:
            cursor.execute("ALTER TABLE animals ADD COLUMN age INTEGER;")
        if 'image_path' not in columns:
            cursor.execute("ALTER TABLE animals ADD COLUMN image_path VARCHAR;")
            
        print("Database fix successful.")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fix_db()
