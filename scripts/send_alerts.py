import requests
import uuid
import datetime
import time
import os
import random
import hashlib
import json

KEEP_API_URL = "https://api.keephq.dev/alerts/event"
KEEP_API_KEY = os.getenv("KEEP_API_KEY") 

# sample alerts
alerts = [
    {"name": "CI Job Failed", "message": "Unit tests did not pass", "severity": "critical"},
    {"name": "CI Job Failed", "message": "Unit tests did not pass", "severity": "critical"},  # dupe
    {"name": "Lint Warning", "message": "Trailing whitespace detected", "severity": "info"},
    {"name": "Docker Build Failed", "message": "Image build failed for service api", "severity": "critical"},
    {"name": "Docker Build Failed", "message": "Image build failed for service api v2", "severity": "critical"},
    {"name": "Code Coverage Drop", "message": "Coverage fell below 80%", "severity": "warning"},
    {"name": "Disk Space Low", "message": "Server disk usage above 90%", "severity": "critical"},
    {"name": "Disk Space Low", "message": "Server disk usage above 90%", "severity": "critical"},  # dupe
    {"name": "Memory Usage High", "message": "Pod memory usage above 85%", "severity": "warning"},
    {"name": "New Commit Pushed", "message": "Commit 1a2b3c added to repo", "severity": "info"}
]

# optional fields and labels
sources = ["github-actions", "prometheus", "custom-script", "ci-cd", "kubernetes"]
services = ["backend", "frontend", "database", "cache", "api"]
environments = ["production", "staging", "development"]
labels_template = [
    {"region": "us-east-1", "cpu": "80%", "memory": "512Mi"},
    {"region": "eu-central-1", "cpu": "70%", "memory": "1Gi"},
    {"region": "ap-southeast-1", "cpu": "60%", "memory": "256Mi"}
]

def int_fmt(i):
    s = str(i)
    s = "0"*(2-len(s))+s
    return s

def get_timestr():
    d = datetime.datetime.now()
    t = f"{int_fmt(d.year)}-{int_fmt(d.month)}-{int_fmt(d.day)}T{int_fmt(d.hour)}:{int_fmt(d.minute)}:{int_fmt(d.second)}Z"
    return t

for alert in alerts:
    service = random.choice(services)
    source = random.choice(sources)
    payload = {
        "id": str(uuid.uuid4()),
        "name": alert["name"],
        "message": alert["message"],
        "description": alert["message"],
        "status": "firing",
        "environment": random.choice(environments),
        "service": service,
        "source": [source],
        "severity": alert["severity"],
        "lastReceived": get_timestr(),
        # "fingerprint":
        "labels": random.choice(labels_template),
        "url": "https://www.keephq.dev?alertId=" + str(uuid.uuid4()),
        "ticket_url": "https://www.keephq.dev?enrichedTicketId=" + str(uuid.uuid4()),
        "pushed": True
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-API-KEY": KEEP_API_KEY
    }

    r = requests.post(KEEP_API_URL, headers=headers, json=payload)
    print(f"Sent alert '{payload['name']}' (severity: {payload['severity']}, source: {source}, service: {service}) -> {r.status_code}")
    time.sleep(1)
