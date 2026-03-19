import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def sync():
    print(f"Connecting to: {DATABASE_URL.split('@')[0]}@...")
    try:
        conn = psycopg2.connect(DATABASE_URL)
        conn.autocommit = True
        cur = conn.cursor()
        
        # Sync vaccinations
        print("Checking vaccinations table...")
        cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'vaccinations';")
        vcols = [r[0] for r in cur.fetchall()]
        
        if 'record_type' not in vcols:
            print("Adding 'record_type' to vaccinations...")
            cur.execute("ALTER TABLE vaccinations ADD COLUMN record_type VARCHAR DEFAULT 'Vacuna';")
            
        if 'observation' not in vcols:
            print("Adding 'observation' to vaccinations...")
            cur.execute("ALTER TABLE vaccinations ADD COLUMN observation TEXT;")
            
        if 'cost' not in vcols:
            print("Adding 'cost' to vaccinations...")
            cur.execute("ALTER TABLE vaccinations ADD COLUMN cost FLOAT DEFAULT 0.0;")

        # Check workers table for 'sector'
        print("Checking workers table...")
        cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'workers';")
        wcols = [r[0] for r in cur.fetchall()]
        if 'sector' not in wcols:
            print("Adding 'sector' to workers...")
            cur.execute("ALTER TABLE workers ADD COLUMN sector VARCHAR DEFAULT 'Ganadería';")

        # Check sales table for 'sector' and 'buyer'
        print("Checking sales table...")
        cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'sales';")
        scols = [r[0] for r in cur.fetchall()]
        if 'sector' not in scols:
            print("Adding 'sector' to sales...")
            cur.execute("ALTER TABLE sales ADD COLUMN sector VARCHAR DEFAULT 'Ganadería';")
        if 'buyer' not in scols:
            print("Adding 'buyer' to sales...")
            cur.execute("ALTER TABLE sales ADD COLUMN buyer VARCHAR;")

        print("Schema synchronization successful.")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    sync()
