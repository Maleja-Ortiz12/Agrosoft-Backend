import urllib.request
import json

url = "http://127.0.0.1:8000/vaccinations/"
data = json.dumps({
    "animal_id": 1,
    "record_type": "Vacuna",
    "treatment_name": "Test",
    "date": "2023-10-10",
    "next_due_date": "2023-11-10",
    "cost": 0.0,
    "observation": "Test"
}).encode("utf-8")

try:
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as response:
        print("SUCCESS:", response.read().decode())
except urllib.error.HTTPError as e:
    print("HTTP ERROR:", e.code, e.reason)
    print(e.read().decode())
except Exception as e:
    print("ERROR:", e)
