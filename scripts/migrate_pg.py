import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def migrate():
    db_url = os.getenv("DATABASE_URL")
    print(f"Connecting to: {db_url}")
    
    try:
        conn = psycopg2.connect(db_url)
        conn.autocommit = True
        cursor = conn.cursor()
        
        print("Checking for missing columns in 'animals' table...")
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'animals';
        """)
        columns = [row[0] for row in cursor.fetchall()]
        print(f"Existing columns: {columns}")
        
        if 'image_path' not in columns:
            print("Adding 'image_path' column...")
            cursor.execute("ALTER TABLE animals ADD COLUMN image_path VARCHAR;")
            
        if 'age' not in columns:
            print("Adding 'age' column...")
            cursor.execute("ALTER TABLE animals ADD COLUMN age INTEGER;")
            
        print("Migration successful.")
        
        cursor.execute("SELECT COUNT(*) FROM animals;")
        count = cursor.fetchone()[0]
        print(f"Total records in 'animals': {count}")
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error during migration: {e}")

if __name__ == "__main__":
    migrate()
