import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
url = os.getenv("DATABASE_URL")
conn = psycopg2.connect(url)
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE vaccinations RENAME COLUMN vaccine_name TO treatment_name;")
    conn.commit()
    print("Column 'vaccine_name' renamed to 'treatment_name' successfully.")
except Exception as e:
    print("Error:", e)
finally:
    cursor.close()
    conn.close()
