from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import Optional
import os
import shutil
from models import models, database
from schemas import schemas
from api import crud
import io
import logging

# Monkeypatch passlib for Python 3.13 compatibility
import logging
import passlib.handlers.bcrypt
import bcrypt

# Fix for passlib on Python 3.13: it tries to read bcrypt.__version__ which is missing in newer versions
if not hasattr(bcrypt, "__version__"):
    bcrypt.__version__ = "4.0.1" # Dummy version to satisfy passlib

logging.getLogger('passlib').setLevel(logging.ERROR)

# Asegurarse de que exista el directorio de uploads
os.makedirs("uploads", exist_ok=True)

# Crear las tablas
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Agrosoft API",
    description="API para la digitalización del sector ganadero con enfoque en accesibilidad.",
    version="0.1.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar el directorio de uploads estáticamente
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Dependencia para obtener la DB
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Bienvenido a la API de Agrosoft"}

@app.get("/health-alerts/")
def get_health_alerts(days: int = 7, db: Session = Depends(get_db)):
    return crud.get_health_alerts(db, days=days)

@app.get("/fertilization-alerts/")
def get_fertilization_alerts(days: int = 7, db: Session = Depends(get_db)):
    return crud.get_fertilization_alerts(db, days=days)

@app.post("/animals/", response_model=schemas.Animal)
def create_animal(animal: schemas.AnimalCreate, db: Session = Depends(get_db)):
    db_animal = crud.get_animal_by_tag(db, tag_id=animal.tag_id)
    if db_animal:
        raise HTTPException(status_code=400, detail="La identificación (tag_id) ya está registrada")
    return crud.create_animal(db=db, animal=animal)

@app.get("/animals/", response_model=list[schemas.Animal])
def read_animals(skip: int = 0, limit: int = 100, include_inactive: bool = False, db: Session = Depends(get_db)):
    animals = crud.get_animals(db, skip=skip, limit=limit, include_inactive=include_inactive)
    return animals

@app.get("/animals/{animal_id}", response_model=schemas.Animal)
def read_animal(animal_id: int, db: Session = Depends(get_db)):
    db_animal = crud.get_animal(db, animal_id=animal_id)
    if db_animal is None:
        raise HTTPException(status_code=404, detail="Animal no encontrado")
    return db_animal

@app.patch("/animals/{animal_id}", response_model=schemas.Animal)
def update_animal(animal_id: int, update: schemas.AnimalUpdate, db: Session = Depends(get_db)):
    db_animal = crud.update_animal(db=db, animal_id=animal_id, update=update)
    if db_animal is None:
        raise HTTPException(status_code=404, detail="Animal no encontrado")
    return db_animal

@app.delete("/animals/{animal_id}")
def delete_animal(animal_id: int, db: Session = Depends(get_db)):
    db_animal = crud.delete_animal(db=db, animal_id=animal_id)
    if not db_animal:
        raise HTTPException(status_code=404, detail="Animal no encontrado")
    return {"message": "Animal eliminado correctamente"}

@app.post("/animals/{animal_id}/image", response_model=schemas.Animal)
async def upload_animal_image(animal_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    db_animal = crud.get_animal(db, animal_id=animal_id)
    if not db_animal:
        raise HTTPException(status_code=404, detail="Animal no encontrado")

    # Guardar el archivo
    file_path = f"uploads/animal_{animal_id}_{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Actualizar la ruta en la base de datos
    db_animal.image_path = file_path
    db.commit()
    db.refresh(db_animal)
    
    return db_animal

# Endpoints para Ventas
@app.post("/sales/", response_model=schemas.Sale)
def create_sale(sale: schemas.SaleCreate, db: Session = Depends(get_db)):
    return crud.create_sale(db=db, sale=sale)

@app.get("/sales/", response_model=list[schemas.Sale])
def read_sales(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_sales(db, skip=skip, limit=limit)

@app.patch("/sales/{sale_id}", response_model=schemas.Sale)
def update_sale(sale_id: int, update: schemas.SaleUpdate, db: Session = Depends(get_db)):
    db_sale = crud.update_sale(db=db, sale_id=sale_id, update=update)
    if not db_sale:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    return db_sale

@app.delete("/sales/{sale_id}")
def delete_sale(sale_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_sale(db=db, sale_id=sale_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    return {"message": "Venta eliminada"}

@app.get("/predictions/milk")
def get_milk_prediction(db: Session = Depends(get_db)):
    prediction = crud.get_milk_prediction(db)
    return {
        "prediction": prediction,
        "unit": "Litros",
        "message": f"Se estima una producción de {prediction} litros para mañana." if prediction > 0 else "No hay datos suficientes para predecir."
    }

@app.get("/vaccinations/", response_model=list[schemas.Vaccination])
def read_vaccinations(animal_id: Optional[int] = None, db: Session = Depends(get_db)):
    return crud.get_vaccinations(db, animal_id=animal_id)

@app.get("/health/alerts", response_model=list)
def read_health_alerts(days: int = 7, db: Session = Depends(get_db)):
    return crud.get_health_alerts(db, days=days)

@app.post("/vaccinations/", response_model=schemas.Vaccination)
def create_vaccination(vaccination: schemas.VaccinationCreate, db: Session = Depends(get_db)):
    return crud.create_vaccination(db=db, vaccination=vaccination)

@app.post("/vaccinations/bulk", response_model=list[schemas.Vaccination])
def create_bulk_vaccinations(bulk_vaccine: schemas.BulkVaccinationCreate, db: Session = Depends(get_db)):
    return crud.create_bulk_vaccinations(db=db, bulk_vaccine=bulk_vaccine)

@app.patch("/vaccinations/{vaccination_id}", response_model=schemas.Vaccination)
def update_vaccination(vaccination_id: int, update: schemas.VaccinationUpdate, db: Session = Depends(get_db)):
    db_vac = crud.update_vaccination(db=db, vaccination_id=vaccination_id, update=update)
    if not db_vac:
        raise HTTPException(status_code=404, detail="Registro de salud no encontrado")
    return db_vac

@app.delete("/vaccinations/{vaccination_id}")
def delete_vaccination(vaccination_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_vaccination(db=db, vaccination_id=vaccination_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Vaccination not found")
    return {"message": "Vaccination deleted successfully"}

@app.get("/expenses/", response_model=list[schemas.Expense])
def read_expenses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_expenses(db, skip=skip, limit=limit)

@app.post("/expenses/", response_model=schemas.Expense)
def create_expense(expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    return crud.create_expense(db=db, expense=expense)

@app.patch("/expenses/{expense_id}", response_model=schemas.Expense)
def update_expense(expense_id: int, update: schemas.ExpenseUpdate, db: Session = Depends(get_db)):
    db_exp = crud.update_expense(db=db, expense_id=expense_id, update=update)
    if not db_exp:
        raise HTTPException(status_code=404, detail="Gasto no encontrado")
    return db_exp

@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_expense(db=db, expense_id=expense_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Gasto no encontrado")
    return {"message": "Gasto eliminado"}

@app.get("/reports/summary")
def read_financial_summary(db: Session = Depends(get_db)):
    return crud.get_financial_summary(db)

@app.get("/inseminations/", response_model=list[schemas.Insemination])
def read_inseminations(animal_id: Optional[int] = None, db: Session = Depends(get_db)):
    return crud.get_inseminations(db, animal_id=animal_id)

@app.post("/inseminations/", response_model=schemas.Insemination)
def create_insemination(insemination: schemas.InseminationCreate, db: Session = Depends(get_db)):
    return crud.create_insemination(db=db, insemination=insemination)

@app.patch("/inseminations/{insemination_id}", response_model=schemas.Insemination)
def update_insemination(insemination_id: int, update: schemas.InseminationUpdate, db: Session = Depends(get_db)):
    return crud.update_insemination(db=db, insemination_id=insemination_id, update=update)

@app.delete("/inseminations/{insemination_id}")
def delete_insemination(insemination_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_insemination(db=db, insemination_id=insemination_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Inseminación no encontrada")
    return {"message": "Inseminación eliminada"}

@app.get("/weight-records/", response_model=list[schemas.WeightRecord])
def read_weight_records(animal_id: Optional[int] = None, db: Session = Depends(get_db)):
    return crud.get_weight_records(db, animal_id=animal_id)

@app.post("/weight-records/", response_model=schemas.WeightRecord)
def create_weight_record(weight_record: schemas.WeightRecordCreate, db: Session = Depends(get_db)):
    return crud.create_weight_record(db=db, weight_record=weight_record)

@app.patch("/weight-records/{weight_id}", response_model=schemas.WeightRecord)
def update_weight_record(weight_id: int, update: schemas.WeightRecordUpdate, db: Session = Depends(get_db)):
    db_w = crud.update_weight_record(db=db, weight_id=weight_id, update=update)
    if not db_w:
        raise HTTPException(status_code=404, detail="Registro de peso no encontrado")
    return db_w

@app.delete("/weight-records/{weight_id}")
def delete_weight_record(weight_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_weight_record(db=db, weight_id=weight_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Registro de peso no encontrado")
    return {"message": "Registro de peso eliminado"}

# --- ENDPOINTS AGRICULTURA ---

@app.get("/crops/", response_model=list[schemas.Crop])
def read_crops(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_crops(db, skip=skip, limit=limit)

@app.post("/crops/", response_model=schemas.Crop)
def create_crop(crop: schemas.CropCreate, db: Session = Depends(get_db)):
    return crud.create_crop(db=db, crop=crop)

@app.patch("/crops/{crop_id}", response_model=schemas.Crop)
def update_crop(crop_id: int, update: schemas.CropUpdate, db: Session = Depends(get_db)):
    db_crop = crud.update_crop(db=db, crop_id=crop_id, update=update)
    if not db_crop:
        raise HTTPException(status_code=404, detail="Cultivo no encontrado")
    return db_crop

@app.delete("/crops/{crop_id}")
def delete_crop(crop_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_crop(db, crop_id=crop_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Cultivo no encontrado")
    return {"message": "Cultivo eliminado"}

@app.get("/irrigations/", response_model=list[schemas.Irrigation])
def read_irrigations(crop_id: Optional[int] = None, db: Session = Depends(get_db)):
    return crud.get_irrigations(db, crop_id=crop_id)

@app.post("/irrigations/", response_model=schemas.Irrigation)
def create_irrigation(irrigation: schemas.IrrigationCreate, db: Session = Depends(get_db)):
    return crud.create_irrigation(db=db, irrigation=irrigation)

@app.patch("/irrigations/{irrigation_id}", response_model=schemas.Irrigation)
def update_irrigation(irrigation_id: int, update: schemas.IrrigationUpdate, db: Session = Depends(get_db)):
    db_irr = crud.update_irrigation(db=db, irrigation_id=irrigation_id, update=update)
    if not db_irr:
        raise HTTPException(status_code=404, detail="Riego no encontrado")
    return db_irr

@app.delete("/irrigations/{irrigation_id}")
def delete_irrigation(irrigation_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_irrigation(db, irrigation_id=irrigation_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Riego no encontrado")
    return {"message": "Riego eliminado"}

@app.get("/fertilizations/", response_model=list[schemas.Fertilization])
def read_fertilizations(crop_id: Optional[int] = None, db: Session = Depends(get_db)):
    return crud.get_fertilizations(db, crop_id=crop_id)

@app.post("/fertilizations/", response_model=schemas.Fertilization)
def create_fertilization(fertilization: schemas.FertilizationCreate, db: Session = Depends(get_db)):
    return crud.create_fertilization(db=db, fertilization=fertilization)

@app.patch("/fertilizations/{fertilization_id}", response_model=schemas.Fertilization)
def update_fertilization(fertilization_id: int, update: schemas.FertilizationUpdate, db: Session = Depends(get_db)):
    db_f = crud.update_fertilization(db=db, fertilization_id=fertilization_id, update=update)
    if not db_f:
        raise HTTPException(status_code=404, detail="Fertilización no encontrada")
    return db_f

@app.delete("/fertilizations/{fertilization_id}")
def delete_fertilization(fertilization_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_fertilization(db, fertilization_id=fertilization_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Fertilización no encontrada")
    return {"message": "Fertilización eliminada"}

@app.get("/pests/", response_model=list[schemas.Pest])
def read_pests(crop_id: Optional[int] = None, db: Session = Depends(get_db)):
    return crud.get_pests(db, crop_id=crop_id)

@app.post("/pests/", response_model=schemas.Pest)
def create_pest(pest: schemas.PestCreate, db: Session = Depends(get_db)):
    return crud.create_pest(db=db, pest=pest)

@app.patch("/pests/{pest_id}", response_model=schemas.Pest)
def update_pest(pest_id: int, update: schemas.PestUpdate, db: Session = Depends(get_db)):
    db_p = crud.update_pest(db=db, pest_id=pest_id, update=update)
    if not db_p:
        raise HTTPException(status_code=404, detail="Reporte de plaga no encontrado")
    return db_p

@app.delete("/pests/{pest_id}")
def delete_pest(pest_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_pest(db, pest_id=pest_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Reporte de plaga no encontrado")
    return {"message": "Reporte de plaga eliminado"}

@app.get("/harvests/", response_model=list[schemas.Harvest])
def read_harvests(crop_id: Optional[int] = None, db: Session = Depends(get_db)):
    return crud.get_harvests(db, crop_id=crop_id)

@app.post("/harvests/", response_model=schemas.Harvest)
def create_harvest(harvest: schemas.HarvestCreate, db: Session = Depends(get_db)):
    return crud.create_harvest(db=db, harvest=harvest)

@app.patch("/harvests/{harvest_id}", response_model=schemas.Harvest)
def update_harvest(harvest_id: int, update: schemas.HarvestUpdate, db: Session = Depends(get_db)):
    db_h = crud.update_harvest(db=db, harvest_id=harvest_id, update=update)
    if not db_h:
        raise HTTPException(status_code=404, detail="Cosecha no encontrada")
    return db_h

@app.delete("/harvests/{harvest_id}")
def delete_harvest(harvest_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_harvest(db, harvest_id=harvest_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Cosecha no encontrada")
    return {"message": "Cosecha eliminada"}

# --- ENDPOINTS PERSONAL ---

@app.get("/workers/", response_model=list[schemas.Worker])
def read_workers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_workers(db, skip=skip, limit=limit)

@app.post("/workers/", response_model=schemas.Worker)
def create_worker(worker: schemas.WorkerCreate, db: Session = Depends(get_db)):
    return crud.create_worker(db=db, worker=worker)

@app.patch("/workers/{worker_id}", response_model=schemas.Worker)
def update_worker(worker_id: int, update: schemas.WorkerUpdate, db: Session = Depends(get_db)):
    db_w = crud.update_worker(db=db, worker_id=worker_id, update=update)
    if not db_w:
        raise HTTPException(status_code=404, detail="Trabajador no encontrado")
    return db_w

@app.delete("/workers/{worker_id}")
def delete_worker(worker_id: int, db: Session = Depends(get_db)):
    db_worker = crud.delete_worker(db, worker_id=worker_id)
    if db_worker is None:
        raise HTTPException(status_code=404, detail="Trabajador no encontrado")
    return {"message": "Trabajador eliminado"}

@app.get("/work-logs/", response_model=list[schemas.WorkLog])
def read_work_logs(worker_id: Optional[int] = None, only_unpaid: bool = False, db: Session = Depends(get_db)):
    return crud.get_work_logs(db, worker_id=worker_id, only_unpaid=only_unpaid)

@app.post("/work-logs/", response_model=schemas.WorkLog)
def create_work_log(work_log: schemas.WorkLogCreate, db: Session = Depends(get_db)):
    return crud.create_work_log(db=db, work_log=work_log)

@app.post("/work-logs/batch/", response_model=list[schemas.WorkLog])
def create_work_logs_batch(batch: schemas.WorkLogBatchCreate, db: Session = Depends(get_db)):
    return crud.create_work_logs_batch(db=db, batch=batch)

@app.patch("/work-logs/{log_id}", response_model=schemas.WorkLog)
def update_work_log(log_id: int, update: schemas.WorkLogUpdate, db: Session = Depends(get_db)):
    db_log = crud.update_work_log(db=db, log_id=log_id, update=update)
    if not db_log:
        raise HTTPException(status_code=404, detail="Bitácora no encontrada")
    return db_log

@app.delete("/work-logs/{log_id}")
def delete_work_log(log_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_work_log(db=db, log_id=log_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Bitácora no encontrada")
    return {"message": "Bitácora eliminada"}

from fastapi.responses import StreamingResponse

@app.get("/reports/tax-report")
def get_tax_report(db: Session = Depends(get_db)):
    excel_content = crud.get_tax_report_excel(db)
    if excel_content is None:
        raise HTTPException(status_code=404, detail="No hay datos suficientes para el reporte")
    
    return StreamingResponse(
        io.BytesIO(excel_content),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=reporte_impuestos_agrosoft.xlsx"}
    )

# --- ENDPOINTS DE AUTENTICACION ---

@app.post("/auth/register", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="El nombre de usuario ya existe")
    return crud.create_user(db=db, user=user)

@app.post("/auth/login")
def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user_credentials.username)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    if not crud.verify_password(user_credentials.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")
    
    return {
        "status": "success",
        "user_id": db_user.id,
        "username": db_user.username,
        "full_name": db_user.full_name
    }

# --- ENDPOINTS NOMINA ---

@app.post("/payroll/", response_model=schemas.Payroll)
def create_payroll(payroll: schemas.PayrollCreate, db: Session = Depends(get_db)):
    return crud.create_payroll(db=db, payroll=payroll)

@app.get("/payroll/", response_model=list[schemas.Payroll])
def read_payroll(worker_id: int, db: Session = Depends(get_db)):
    return crud.get_payroll_by_worker(db, worker_id=worker_id)

@app.delete("/payroll/{payroll_id}")
def delete_payroll(payroll_id: int, db: Session = Depends(get_db)):
    db_payroll = crud.delete_payroll(db, payroll_id=payroll_id)
    if not db_payroll:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return {"status": "deleted"}
