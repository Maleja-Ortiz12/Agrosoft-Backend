import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
url = os.getenv("DATABASE_URL")
conn = psycopg2.connect(url)
cursor = conn.cursor()

try:
    cursor.execute("DELETE FROM vaccinations WHERE treatment_name IN ('Test', 'TestFinal');")
    conn.commit()
    print("Deleted test records successfully.")
except Exception as e:
    print("Error:", e)
finally:
    cursor.close()
    conn.close()
