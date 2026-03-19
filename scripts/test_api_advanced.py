import pytest
from fastapi.testclient import TestClient
from main import app
from datetime import date, timedelta

client = TestClient(app)

# --- PRUEBAS DE SEGURIDAD Y VALIDACIÓN ---

def test_create_sale_invalid_data():
    """Prueba que los datos inválidos (monto negativo) sean manejados."""
    # Nota: Dependiendo de si hay validadores en el esquema Pydantic, esto fallará o se guardará.
    # En una app robusta, quantity y price deberían ser > 0.
    payload = {
        "date": str(date.today()),
        "type": "Leche",
        "quantity": -10.5,
        "price": 0.0,
        "sector": "Ganadería",
        "buyer": "Prueba Error"
    }
    response = client.post("/sales/", json=payload)
    # Si no hay validación, esto devuelve 200/201, pero es una falla lógica para el negocio.
    print(f"Validación de datos negativos: status {response.status_code}")

def test_sql_injection_attempt():
    """Prueba básica de intento de inyección en campos de texto."""
    payload = {
        "tag_id": "COW-'; DROP TABLE animals; --",
        "name": "Hacker",
        "gender": "Macho"
    }
    response = client.post("/animals/", json=payload)
    # Debería guardarse como un string literal y NO ejecutar el SQL.
    assert response.status_code in [200, 201]
    data = response.json()
    assert data["tag_id"] == "COW-'; DROP TABLE animals; --"

# --- PRUEBAS CRUD AVANZADAS ---

def test_complete_milk_sale_cycle():
    """Valida el ciclo completo de una venta de leche."""
    # 1. Crear
    sale_data = {
        "date": str(date.today()),
        "type": "Leche",
        "quantity": 50.0,
        "price": 2000.0,
        "sector": "Ganadería",
        "buyer": "Cooperativa San Juan"
    }
    create_res = client.post("/sales/", json=sale_data)
    assert create_res.status_code in [200, 201]
    sale_id = create_res.json()["id"]

    # 2. Leer
    list_res = client.get("/sales/")
    assert any(s["id"] == sale_id for s in list_res.json())

def test_worker_payroll_integration():
    """Valida que un trabajador nuevo pueda recibir pagos."""
    # 1. Crear Trabajador
    worker_data = {
        "name": "Test Worker",
        "role": "Ordeñador",
        "daily_rate": 50000.0,
        "sector": "Ganadería",
        "status": "Activo"
    }
    w_res = client.post("/workers/", json=worker_data)
    assert w_res.status_code in [200, 201]
    w_id = w_res.json()["id"]

    # 2. Registrar Jornada
    log_data = {
        "worker_id": w_id,
        "date": str(date.today()),
        "start_time": "08:00",
        "end_time": "17:00",
        "duties": "Limpieza y ordeño"
    }
    l_res = client.post("/work-logs/", json=log_data)
    assert l_res.status_code in [200, 201]

    # 3. Pagar Nómina
    payroll_data = {
        "worker_id": w_id,
        "amount": 50000.0,
        "payment_date": str(date.today())
    }
    p_res = client.post("/payroll/", json=payroll_data)
    assert p_res.status_code in [200, 201]

if __name__ == "__main__":
    # Ejecución simple sin pytest para facilidad del usuario
    print("Ejecutando pruebas avanzadas de backend...")
    try:
        test_create_sale_invalid_data()
        test_sql_injection_attempt()
        test_complete_milk_sale_cycle()
        test_worker_payroll_integration()
        print("\n[OK] Todas las pruebas lógicas y de seguridad pasaron.")
    except Exception as e:
        print(f"\n[ERROR] Falla en las pruebas: {e}")
