import requests
import json

BASE_URL = "http://localhost:8000"

def test_alerts():
    print("Testing alerts endpoints...")
    
    # Test health alerts
    try:
        res = requests.get(f"{BASE_URL}/health-alerts/")
        print(f"Health alerts status: {res.status_code}")
        print(f"Health alerts: {res.json()}")
    except Exception as e:
        print(f"Health alerts failed: {e}")

    # Test fertilization alerts
    try:
        res = requests.get(f"{BASE_URL}/fertilization-alerts/")
        print(f"Fertilization alerts status: {res.status_code}")
        print(f"Fertilization alerts: {res.json()}")
    except Exception as e:
        print(f"Fertilization alerts failed: {e}")

def test_create_fertilization():
    print("\nTesting fertilization creation with multiple products...")
    
    # First get a crop id
    try:
        crops = requests.get(f"{BASE_URL}/crops/").json()
        if not crops:
            print("No crops found to test fertilization.")
            return
        crop_id = crops[0]['id']
    except Exception as e:
        print(f"Failed to get crops: {e}")
        return

    data = {
        "crop_id": crop_id,
        "fertilizer_name": "Mezcla Especial",
        "quantity": 50.0,
        "application_date": "2026-03-19",
        "next_due_date": "2026-03-25",
        "products_json": json.dumps([
            {"name": "Urea", "qty": "30"},
            {"name": "Potasio", "qty": "20"}
        ])
    }

    try:
        res = requests.post(f"{BASE_URL}/fertilizations/", json=data)
        print(f"Create fertilization status: {res.status_code}")
        print(f"Response: {res.json()}")
    except Exception as e:
        print(f"Create fertilization failed: {e}")

if __name__ == "__main__":
    test_alerts()
    test_create_fertilization()
    # Check alerts again to see the new one
    test_alerts()
