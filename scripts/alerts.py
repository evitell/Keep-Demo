import requests
import uuid
import time

KEEP_API_URL  = "https://api.keephq.dev/alerts/event"
API_KEY = "65135605-d74e-44d5-a53b-ba5286c4662b"

alerts = [
    {"name": "Test alert 1", "message": "Something failed", "severity": "critical"},
    {"name": "Test alert 2", "message": "Something failed", "severity": "critical"}, 
    {"name": "Test alert 3", "message": "Minor warning", "severity": "info"}
]

for alert in alerts:
    payload = {
        "id": str(uuid.uuid4()),
        "name": alert["name"],
        "status": "firing",
        "environment": "demo",
        "source": ["python-script"],
        "message": alert["message"],
        "description": alert["message"],
        "severity": alert["severity"],
        "fingerprint": alert["message"]  # same fingerprint?
    }
    r = requests.post(KEEP_API_URL , headers={"Content-Type": "application/json","X-API-KEY": API_KEY}, json=payload)
    print(f"Sent {alert['name']} -> {r.status_code}")
    time.sleep(1)


