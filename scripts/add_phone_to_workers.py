
from models import database
from sqlalchemy import text

def migrate():
    engine = database.engine
    with engine.connect() as conn:
        print("Añadiendo columna 'phone' a la tabla 'workers'...")
        try:
            conn.execute(text("ALTER TABLE workers ADD COLUMN phone VARCHAR;"))
            conn.commit()
            print("Columna 'phone' añadida exitosamente.")
        except Exception as e:
            print(f"Error (podría ser que la columna ya existe): {e}")

if __name__ == "__main__":
    migrate()
