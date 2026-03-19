from pydantic import BaseModel
from datetime import date
from typing import Optional, List

class AnimalBase(BaseModel):
    tag_id: str
    name: Optional[str] = None
    species: str = "Bovino"
    breed: Optional[str] = None
    birth_date: Optional[date] = None # Permitimos que sea opcional
    age: Optional[int] = None # Added age
    gender: str
    category: str = "Ternera"  # Ternera, Novilla, Vaca, Toro
    status: str = "Activo"  # Activo, Vendido, Muerto
    removal_date: Optional[date] = None
    mother_id: Optional[int] = None
    father_id: Optional[int] = None
    father_breed: Optional[str] = None
    image_path: Optional[str] = None

class AnimalCreate(AnimalBase):
    pass

class AnimalUpdate(BaseModel):
    tag_id: Optional[str] = None
    name: Optional[str] = None
    breed: Optional[str] = None
    birth_date: Optional[date] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    category: Optional[str] = None
    status: Optional[str] = None
    removal_date: Optional[date] = None

class Animal(AnimalBase):
    id: int
    mother_breed: Optional[str] = None
    pregnancy_status: Optional[str] = "Sin cargar"
    estimated_birth_date: Optional[date] = None

    class Config:
        from_attributes = True

class SaleBase(BaseModel):
    date: date
    type: str  # "Leche" o "Ganado"
    quantity: float
    price: float
    sector: str = "Ganadería"
    description: Optional[str] = None
    buyer: Optional[str] = None
    paid_amount: Optional[float] = None

class SaleCreate(SaleBase):
    pass

class Sale(SaleBase):
    id: int

    class Config:
        from_attributes = True

class SaleUpdate(BaseModel):
    date: Optional[date] = None
    type: Optional[str] = None
    quantity: Optional[float] = None
    price: Optional[float] = None
    sector: Optional[str] = None
    description: Optional[str] = None
    buyer: Optional[str] = None
    paid_amount: Optional[float] = None

class VaccinationBase(BaseModel):
    animal_id: int
    record_type: str = "Vacuna" # Vacuna, Desparasitante, Medicamento
    treatment_name: str
    date: date
    cost: float = 0.0
    observation: Optional[str] = None
    next_due_date: Optional[date] = None

class VaccinationCreate(VaccinationBase):
    pass

class Vaccination(VaccinationBase):
    id: int

    class Config:
        from_attributes = True

class VaccinationUpdate(BaseModel):
    record_type: Optional[str] = None
    treatment_name: Optional[str] = None
    date: Optional[date] = None
    cost: Optional[float] = None
    observation: Optional[str] = None
    next_due_date: Optional[date] = None

class BulkVaccinationCreate(BaseModel):
    animal_ids: list[int]
    record_type: str = "Vacuna"
    treatment_name: str
    date: date
    cost: float = 0.0
    observation: Optional[str] = None
    next_due_date: Optional[date] = None

class ExpenseBase(BaseModel):
    date: date
    category: str
    amount: float
    sector: str = "Ganadería"
    description: Optional[str] = None

class ExpenseCreate(ExpenseBase):
    pass

class Expense(ExpenseBase):
    id: int

    class Config:
        from_attributes = True

class ExpenseUpdate(BaseModel):
    date: Optional[date] = None
    category: Optional[str] = None
    amount: Optional[float] = None
    sector: Optional[str] = None
    description: Optional[str] = None

class InseminationBase(BaseModel):
    animal_id: int
    date: date
    bull_breed: str
    status: str = "Pendiente"
    estimated_birth_date: Optional[date] = None
    actual_birth_date: Optional[date] = None
    observation: Optional[str] = None

class InseminationCreate(InseminationBase):
    pass

class InseminationUpdate(BaseModel):
    status: Optional[str] = None
    actual_birth_date: Optional[date] = None
    observation: Optional[str] = None

class Insemination(InseminationBase):
    id: int
    animal_name: Optional[str] = None
    animal_breed: Optional[str] = None

    class Config:
        from_attributes = True

class WeightRecordBase(BaseModel):
    animal_id: int
    weight: float
    date: date
    observation: Optional[str] = None

class WeightRecordCreate(WeightRecordBase):
    pass

class WeightRecord(WeightRecordBase):
    id: int

    class Config:
        from_attributes = True

class WeightRecordUpdate(BaseModel):
    weight: Optional[float] = None
    date: Optional[date] = None
    observation: Optional[str] = None

# --- SCHEMAS DE AGRICULTURA ---

class CropBase(BaseModel):
    crop_name: str
    variety: Optional[str] = None
    planting_date: date
    field_or_lot: str
    status: str = "Creciendo"

class CropCreate(CropBase):
    pass

class Crop(CropBase):
    id: int
    class Config:
        from_attributes = True

class CropUpdate(BaseModel):
    crop_name: Optional[str] = None
    variety: Optional[str] = None
    planting_date: Optional[date] = None
    field_or_lot: Optional[str] = None
    status: Optional[str] = None

class IrrigationBase(BaseModel):
    crop_id: int
    irrigation_date: date
    water_amount: float
    irrigation_method: str

class IrrigationCreate(IrrigationBase):
    pass

class Irrigation(IrrigationBase):
    id: int
    class Config:
        from_attributes = True

class IrrigationUpdate(BaseModel):
    irrigation_date: Optional[date] = None
    water_amount: Optional[float] = None
    irrigation_method: Optional[str] = None

class FertilizationBase(BaseModel):
    crop_id: int
    fertilizer_name: str
    quantity: float
    application_date: date
    next_due_date: Optional[date] = None
    products_json: Optional[str] = None

class FertilizationCreate(FertilizationBase):
    pass

class Fertilization(FertilizationBase):
    id: int
    class Config:
        from_attributes = True

class FertilizationUpdate(BaseModel):
    fertilizer_name: Optional[str] = None
    quantity: Optional[float] = None
    application_date: Optional[date] = None
    next_due_date: Optional[date] = None
    products_json: Optional[str] = None

class PestBase(BaseModel):
    crop_id: int
    pest_type: str
    treatment: Optional[str] = None
    report_date: date

class PestCreate(PestBase):
    pass

class Pest(PestBase):
    id: int
    class Config:
        from_attributes = True

class PestUpdate(BaseModel):
    pest_type: Optional[str] = None
    treatment: Optional[str] = None
    report_date: Optional[date] = None

class HarvestBase(BaseModel):
    crop_id: int
    harvest_date: date
    quantity: float
    unit: str = "Unidad"
    unit_cost: float = 0.0
    destination: Optional[str] = None
    buyer: Optional[str] = None
    paid_amount: Optional[float] = None

class HarvestCreate(HarvestBase):
    pass

class Harvest(HarvestBase):
    id: int
    crop_name: Optional[str] = None

    class Config:
        from_attributes = True

class HarvestUpdate(BaseModel):
    harvest_date: Optional[date] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None
    unit_cost: Optional[float] = None
    destination: Optional[str] = None
    buyer: Optional[str] = None
    paid_amount: Optional[float] = None

# --- STAFF SCHEMAS ---

class WorkerBase(BaseModel):
    name: str
    role: str
    daily_rate: float = 0.0
    payment_frequency: str = "Semanal"
    status: str = "Activo"
    sector: str = "Ganadería"
    phone: Optional[str] = None

class WorkerCreate(WorkerBase):
    pass

class Worker(WorkerBase):
    id: int
    class Config:
        from_attributes = True

class WorkerUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    daily_rate: Optional[float] = None
    payment_frequency: Optional[str] = None
    status: Optional[str] = None
    sector: Optional[str] = None
    phone: Optional[str] = None

class WorkLogBase(BaseModel):
    worker_id: int
    date: date
    start_time: str
    end_time: str
    duties: Optional[str] = None
    calculated_cost: float = 0.0

class WorkLogCreate(WorkLogBase):
    pass

class WorkLog(WorkLogBase):
    id: int
    class Config:
        from_attributes = True

class WorkLogUpdate(BaseModel):
    date: Optional[date] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    duties: Optional[str] = None
    calculated_cost: Optional[float] = None

class WorkLogBatchCreate(BaseModel):
    worker_id: int
    dates: List[date]
    start_time: str
    end_time: str
    duties: Optional[str] = None
    calculated_cost: float = 0.0

class UserBase(BaseModel):
    username: str
    full_name: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class User(UserBase):
    id: int
    status: str

    class Config:
        from_attributes = True

class PayrollBase(BaseModel):
    worker_id: int
    amount: float
    payment_date: date
    signature_data: Optional[str] = None
    log_ids: Optional[str] = None

class PayrollCreate(PayrollBase):
    pass

class Payroll(PayrollBase):
    id: int

    class Config:
        from_attributes = True
