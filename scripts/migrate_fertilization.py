import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)

def migrate():
    with engine.connect() as conn:
        print("Migrating fertilizations table...")
        
        # Add next_due_date
        try:
            conn.execute(text("ALTER TABLE fertilizations ADD COLUMN next_due_date DATE"))
            print("Added next_due_date column.")
        except Exception as e:
            print(f"Error adding next_due_date: {e}")

        # Add products_json
        try:
            conn.execute(text("ALTER TABLE fertilizations ADD COLUMN products_json TEXT"))
            print("Added products_json column.")
        except Exception as e:
            print(f"Error adding products_json: {e}")
        
        conn.commit()
        print("Migration completed.")

if __name__ == "__main__":
    migrate()
