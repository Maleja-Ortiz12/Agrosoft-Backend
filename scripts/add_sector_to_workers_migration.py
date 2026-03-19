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
            WHERE table_name='workers' AND column_name='sector';
        """)
        
        if cur.fetchone()[0] == 0:
            print("Adding 'sector' column to 'workers' table...")
            cur.execute("ALTER TABLE workers ADD COLUMN sector VARCHAR DEFAULT 'Ganadería';")
            # Update existing workers to 'Agricultura' if the user typically uses it there
            # but since "dale" was given to the plan that says "by default it's Ganaderia but we'll sum to Ag", 
            # I'll set 'Agricultura' for current workers as they are in the Agricultural module.
            cur.execute("UPDATE workers SET sector = 'Agricultura';")
            conn.commit()
            print("Migration successful.")
        else:
            print("Column 'sector' already exists in 'workers' table.")
            
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error during migration: {e}")

if __name__ == "__main__":
    migrate()
