import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

try:
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'payroll';")
    columns = cursor.fetchall()
    print("Payroll table columns:")
    for col in columns:
        print(col)
    cursor.close()
    conn.close()
except Exception as e:
    print(f"Error: {e}")
