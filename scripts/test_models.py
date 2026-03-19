import sys
import os
sys.path.append(os.getcwd())

try:
    from models.database import engine, Base
    from models.models import Animal, Sale, Vaccination, Expense, Insemination, Crop, Irrigation, Fertilization, Pest, Harvest, Worker, WorkLog, User, Payroll
    
    print("All models imported successfully.")
    print("Tables registered in metadata:", Base.metadata.tables.keys())
    
    print("Starting create_all()...")
    Base.metadata.create_all(bind=engine)
    print("create_all() finished successfully.")
    
    from sqlalchemy import inspect
    inspector = inspect(engine)
    print("Tables in DB:", inspector.get_table_names())
    
    for table_name in Base.metadata.tables:
        table = Base.metadata.tables[table_name]
        print(f"Checking table: {table_name}")
        for fk in table.foreign_keys:
            print(f"  FK: {fk.column} -> {fk.target_fullname}")
            
except Exception as e:
    print(f"Error caught: {e}")
    import traceback
    traceback.print_exc()
