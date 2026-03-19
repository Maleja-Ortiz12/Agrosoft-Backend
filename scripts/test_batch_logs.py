import requests
import json
from datetime import date, timedelta

BASE_URL = "http://127.0.0.1:8000"

def test_batch_work_logs():
    # 1. Get a worker ID
    workers = requests.get(f"{BASE_URL}/workers/").json()
    if not workers:
        print("No workers found to test.")
        return
    
    worker_id = workers[0]['id']
    daily_rate = workers[0]['daily_rate']
    
    # 2. Prepare batch data (next 3 days)
    today = date.today()
    dates = [(today + timedelta(days=i)).isoformat() for i in range(3)]
    
    payload = {
        "worker_id": worker_id,
        "dates": dates,
        "start_time": "07:30",
        "end_time": "16:30",
        "duties": "Prueba de registro semanal batch",
        "calculated_cost": daily_rate
    }
    
    print(f"Sending batch request for worker {worker_id}...")
    response = requests.post(f"{BASE_URL}/work-logs/batch/", json=payload)
    
    if response.status_code == 200:
        logs = response.json()
        print(f"Successfully created {len(logs)} work logs.")
        for l in logs:
            print(f" - ID: {l['id']}, Date: {l['date']}")
    else:
        print(f"Error ({response.status_code}): {response.text}")

if __name__ == "__main__":
    test_batch_work_logs()
