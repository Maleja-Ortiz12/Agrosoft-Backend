import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
url = os.getenv("DATABASE_URL")

print(f"Connecting to: {url}")

try:
    conn = psycopg2.connect(url)
    cursor = conn.cursor()
    cursor.execute("ALTER TABLE vaccinations ADD COLUMN IF NOT EXISTS next_due_date DATE;")
    conn.commit()
    print("SUCCESS: Column 'next_due_date' added or already exists.")
    cursor.close()
    conn.close()
except Exception as e:
    print(f"ERROR: {e}")
