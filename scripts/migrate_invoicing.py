import psycopg2
import os

DATABASE_URL = "postgresql://postgres:050423@127.0.0.1:5432/agrosoft"

def migrate():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        print("Migrating 'sales' table...")
        cur.execute("ALTER TABLE sales ADD COLUMN IF NOT EXISTS paid_amount FLOAT;")
        
        print("Migrating 'harvests' table...")
        cur.execute("ALTER TABLE harvests ADD COLUMN IF NOT EXISTS buyer VARCHAR;")
        cur.execute("ALTER TABLE harvests ADD COLUMN IF NOT EXISTS paid_amount FLOAT;")
        
        conn.commit()
        cur.close()
        conn.close()
        print("Migration successful!")
    except Exception as e:
        print(f"Migration failed: {e}")

if __name__ == "__main__":
    migrate()
