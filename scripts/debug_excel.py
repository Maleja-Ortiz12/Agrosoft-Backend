import sys
import os
sys.path.append(os.getcwd())

from models import database, models
from api import crud
from sqlalchemy.orm import Session

db = database.SessionLocal()
try:
    print("Intentando generar el reporte Excel...")
    content = crud.get_tax_report_excel(db)
    if content:
        print(f"Éxito! Tamaño del reporte: {len(content)} bytes")
    else:
        print("El reporte regresó None (no hay datos).")
except Exception as e:
    import traceback
    print("ERROR DETECTADO:")
    traceback.print_exc()
finally:
    db.close()
