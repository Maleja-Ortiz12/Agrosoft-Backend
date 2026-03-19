import sqlite3

def migrate():
    conn = sqlite3.connect('agrosoft.db')
    cursor = conn.cursor()
    
    # Check current columns
    cursor.execute("PRAGMA table_info(animals)")
    columns = [col[1] for col in cursor.fetchall()]
    print(f"Current columns: {columns}")
    
    if 'image_path' not in columns:
        print("Adding image_path column...")
        cursor.execute("ALTER TABLE animals ADD COLUMN image_path TEXT")
    
    if 'age' not in columns:
        print("Adding age column...")
        cursor.execute("ALTER TABLE animals ADD COLUMN age INTEGER")
        
    conn.commit()
    
    # Verify records
    cursor.execute("SELECT COUNT(*) FROM animals")
    count = cursor.fetchone()[0]
    print(f"Total animals in DB: {count}")
    
    conn.close()

if __name__ == "__main__":
    migrate()
