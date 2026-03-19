import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
url = os.getenv("DATABASE_URL")
conn = psycopg2.connect(url)
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE vaccinations ADD COLUMN IF NOT EXISTS record_type VARCHAR DEFAULT 'Vacuna';")
    conn.commit()
    print("Column 'record_type' added successfully.")
except Exception as e:
    print("Error:", e)
finally:
    cursor.close()
    conn.close()
