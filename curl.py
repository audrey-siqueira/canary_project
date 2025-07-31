import requests
import time

URL = "http://0.0.0.0:8000"  # FastAPI server URL

def deploy_canary():
    print("Deploying canary model...")
    payload = {"model_path": "models/model_v2.joblib"}
    response = requests.post(f"{URL}/admin/deploy-canary", json=payload)
    print(response.json())
    print()

def generate_traffic(n=300):
    print(f"Generating {n} prediction requests...")
    payload = {"features": [0.5, 1.2, 0.8, 0.3, 1.1]}
    for _ in range(n):
        response = requests.post(f"{URL}/predict", json=payload)
        # Uncomment to see each response
        # print(response.json())
    print("Traffic generation done.\n")

def check_health():
    print("Performing health check...")
    response = requests.get(f"{URL}/admin/check-canary-health")
    print(response.json())
    print()

def toggle_slowdown():
    print("Toggling slowdown...")
    response = requests.post(f"{URL}/admin/toggle-slowdown")
    print(response.json())
    print()

def rollback_canary():
    print("Rolling back canary...")
    response = requests.post(f"{URL}/admin/rollback-canary")
    print(response.json())
    print()

def confirm_rollback():
    print("Confirming rollback with one prediction...")
    payload = {"features": [0.5, 1.2, 0.8, 0.3, 1.1]}
    response = requests.post(f"{URL}/predict", json=payload)
    print(response.json())
    print()

def power_analysis():
    print("What is the minimum number of samples we need to collect for both the stable and canary models to give us an 80% chance of detecting a 10ms latency increase?")
    params = { "effect_size": 0.666, "alpha": 0.05, "power": 0.8}
    response = requests.get(f"{URL}/admin/power-analysis", params=params)
    print(response.json())
    print()

def main():
    deploy_canary()
    generate_traffic()
    check_health()
    toggle_slowdown()
    generate_traffic()
    check_health()
    rollback_canary()
    confirm_rollback()
    power_analysis()
    print("Test flow complete.")

if __name__ == "__main__":
    main()
