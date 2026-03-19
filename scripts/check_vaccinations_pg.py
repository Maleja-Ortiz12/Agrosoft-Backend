import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

try:
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    table_name = 'vaccinations'
    cur.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table_name}';")
    cols = cur.fetchall()
    print(f"Columns for {table_name}:")
    for col in cols:
        print(f" - {col[0]}: {col[1]}")
            
    cur.close()
    conn.close()
except Exception as e:
    print(f"Error: {e}")
