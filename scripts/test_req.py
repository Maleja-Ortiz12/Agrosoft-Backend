import requests
import json
from datetime import date

url = "http://127.0.0.1:8000/vaccinations/"
data = {
    "animal_id": 1,
    "record_type": "Vacuna",
    "treatment_name": "Test Vaccine",
    "date": date.today().isoformat(),
    "next_due_date": date.today().isoformat(),
    "cost": 50.0,
    "observation": "Test"
}

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")
except Exception as e:
    print(f"Request failed: {e}")
