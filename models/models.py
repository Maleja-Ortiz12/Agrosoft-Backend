from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float, Text, Boolean
from sqlalchemy.orm import relationship, backref
from .database import Base

class Animal(Base):
    __tablename__ = "animals"

    id = Column(Integer, primary_key=True, index=True)
    tag_id = Column(String, unique=True, index=True)  # Chapeta/ID visual
    name = Column(String, nullable=True)
    species = Column(String, default="Bovino")
    breed = Column(String, nullable=True)
    birth_date = Column(Date, nullable=True)
    age = Column(Integer, nullable=True)
    gender = Column(String, nullable=True)
    category = Column(String, default="Ternera")  # Ternera, Novilla, Vaca, Toro
    status = Column(String, default="Activo")  # Activo, Vendido, Muerto
    image_path = Column(String, nullable=True)
    removal_date = Column(Date, nullable=True)
    
    # Genealogía
    mother_id = Column(Integer, ForeignKey("animals.id"), nullable=True)
    father_id = Column(Integer, ForeignKey("animals.id"), nullable=True)
    father_breed = Column(String, nullable=True)
    
    # Relationships for Genealogy
    mother = relationship("Animal", remote_side="Animal.id", foreign_keys="Animal.mother_id", backref="offspring_from_mother")
    father = relationship("Animal", remote_side="Animal.id", foreign_keys="Animal.father_id", backref="offspring_from_father")
    weight_records = relationship("WeightRecord", backref=backref("animal"), cascade="all, delete-orphan")

class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    type = Column(String, nullable=False) # Leche o Ganado
    quantity = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    sector = Column(String, default="Ganadería") # Ganadería o Agricultura
    description = Column(String, nullable=True)
    buyer = Column(String, nullable=True)
    paid_amount = Column(Float, nullable=True)

class Vaccination(Base):
    __tablename__ = "vaccinations"

    id = Column(Integer, primary_key=True, index=True)
    animal_id = Column(Integer, ForeignKey("animals.id"))
    record_type = Column(String, default="Vacuna") # Vacuna, Desparasitante, Medicamento
    treatment_name = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    cost = Column(Float, default=0.0)
    observation = Column(String, nullable=True)
    next_due_date = Column(Date, nullable=True)

    animal = relationship("Animal", backref=backref("vaccinations"), foreign_keys="Vaccination.animal_id")

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    category = Column(String, nullable=False) # Alimento, Medicinas, Transporte, Jornales, etc.
    amount = Column(Float, nullable=False)
    sector = Column(String, default="Ganadería") # Ganadería o Agricultura
    description = Column(String, nullable=True)

class Insemination(Base):
    __tablename__ = "inseminations"

    id = Column(Integer, primary_key=True, index=True)
    animal_id = Column(Integer, ForeignKey("animals.id"))
    date = Column(Date, nullable=False)
    bull_breed = Column(String, nullable=False)
    status = Column(String, default="Pendiente") # Pendiente, Confirmada (Cargada), Fallida, Parto Exitoso
    estimated_birth_date = Column(Date, nullable=True)
    actual_birth_date = Column(Date, nullable=True)
    observation = Column(String, nullable=True)

    cow = relationship("Animal", backref=backref("inseminations"), foreign_keys="Insemination.animal_id")

class WeightRecord(Base):
    __tablename__ = "weight_records"

    id = Column(Integer, primary_key=True, index=True)
    animal_id = Column(Integer, ForeignKey("animals.id"))
    weight = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    observation = Column(String, nullable=True)

# --- MÓDULO DE AGRICULTURA ---

class Crop(Base):
    __tablename__ = "crops"

    id = Column(Integer, primary_key=True, index=True)
    crop_name = Column(String, nullable=False) # Lechuga, Tomate, etc.
    variety = Column(String, nullable=True)
    planting_date = Column(Date, nullable=False)
    field_or_lot = Column(String, nullable=False)
    status = Column(String, default="Creciendo") # Creciendo, Cosechado, Enfermo, etc.

class Irrigation(Base):
    __tablename__ = "irrigations"

    id = Column(Integer, primary_key=True, index=True)
    crop_id = Column(Integer, ForeignKey("crops.id"))
    irrigation_date = Column(Date, nullable=False)
    water_amount = Column(Float, nullable=False) # Litros o m3
    irrigation_method = Column(String, nullable=False) # Goteo, Aspersión, Manual

    crop = relationship("Crop", backref="irrigations")

class Fertilization(Base):
    __tablename__ = "fertilizations"

    id = Column(Integer, primary_key=True, index=True)
    crop_id = Column(Integer, ForeignKey("crops.id"))
    fertilizer_name = Column(String, nullable=False)
    quantity = Column(Float, nullable=False)
    application_date = Column(Date, nullable=False)
    next_due_date = Column(Date, nullable=True)
    products_json = Column(Text, nullable=True)

    crop = relationship("Crop", backref="fertilizations")

class Pest(Base):
    __tablename__ = "pests"

    id = Column(Integer, primary_key=True, index=True)
    crop_id = Column(Integer, ForeignKey("crops.id"))
    pest_type = Column(String, nullable=False)
    treatment = Column(String, nullable=True)
    report_date = Column(Date, nullable=False)

    crop = relationship("Crop", backref="pests")

class Harvest(Base):
    __tablename__ = "harvests"

    id = Column(Integer, primary_key=True, index=True)
    crop_id = Column(Integer, ForeignKey("crops.id"))
    harvest_date = Column(Date, nullable=False)
    quantity = Column(Float, nullable=False) # Cantidad en la unidad seleccionada
    unit = Column(String, default="Unidad") # Unidad, Docena, Kg, etc.
    unit_cost = Column(Float, default=0.0)
    destination = Column(String, nullable=True) # Venta, Consumo, etc.
    buyer = Column(String, nullable=True)
    paid_amount = Column(Float, nullable=True)

    crop = relationship("Crop", backref="harvests")

class Worker(Base):
    __tablename__ = "workers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    daily_rate = Column(Float, default=0.0)
    payment_frequency = Column(String, default="Semanal") # Semanal, Quincenal, Mensual
    status = Column(String, default="Activo") # Activo, Inactivo
    sector = Column(String, default="Ganadería") # Ganadería o Agricultura
    phone = Column(String, nullable=True)

class WorkLog(Base):
    __tablename__ = "work_logs"

    id = Column(Integer, primary_key=True, index=True)
    worker_id = Column(Integer, ForeignKey("workers.id"))
    date = Column(Date, nullable=False)
    start_time = Column(String, nullable=False) # HH:MM
    end_time = Column(String, nullable=False) # HH:MM
    duties = Column(String, nullable=True)
    calculated_cost = Column(Float, default=0.0)

    worker = relationship("Worker", backref="work_logs")
    paid = Column(Boolean, default=False)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    status = Column(String, default="Activo")

class Payroll(Base):
    __tablename__ = "payroll"

    id = Column(Integer, primary_key=True, index=True)
    worker_id = Column(Integer, ForeignKey("workers.id"))
    amount = Column(Float, nullable=False)
    payment_date = Column(Date, nullable=False)
    signature_data = Column(Text, nullable=True) # Base64 string of the signature
    log_ids = Column(String, nullable=True) # Comma separated IDs of work logs paid

    worker = relationship("Worker", backref="payroll_records")
