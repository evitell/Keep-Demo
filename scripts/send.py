#!/usr/bin/env python3

import requests
import os
import datetime
import json


def send(
        name,
        message,
        description,
        status="firing",

    # id="deea4282-2e8f-4418-822e-7012fa147aee",
    # fingerprint="eb3e9e19-91d1-4110-a79a-9f586adcdf24",
    last_received="2025-09-14T15:57:26.353Z",
        keep_api_key=None):
    if keep_api_key is None:
        keep_api_key = os.getenv("KEEP_API_KEY")
        if len(keep_api_key) != 36:
            print(f"WARNING: keep api key has {len(keep_api_key)} characters")

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-API-KEY": keep_api_key
    }
    data = {
        # "id": id,
        "name": name,
        "status": status,
        "lastReceived": last_received,
        "environment": "production",
        "duplicateReason": None,
        "service": "backend",
        "source": [
            "prometheus"
        ],

        "message": message,
        "description": description,
        "severity": "critical",
        "pushed": True,
        "url": "https://www.keephq.dev?alertId=1235",
        "labels": {
            "pod": "api-service-production",
            "region": "us-east-1",
            "cpu": "88",
            "memory": "100Mi"
        },
        "ticket_url": "https://www.keephq.dev?enrichedTicketId=456",
        # "fingerprint": fingerprint
    }
    response = requests.post("https://api.keephq.dev/alerts/event",
                             headers=headers,
                             data=json.dumps(data))

    if not response.ok:

        raise Exception("request failed", response.status_code,
                        response.reason, response.text)
    print(response.json())


def int_fmt(i):
    s = str(i)
    s = "0"*(2-len(s))+s
    return s


if __name__ == "__main__":
    # t = f"{str(datetime.datetime.now())}Z"
    d = datetime.datetime.now()
    t = f"{int_fmt(d.year)}-{int_fmt(d.month)}-{int_fmt(d.day)}T{int_fmt(d.hour)}:{int_fmt(d.minute)}:{int_fmt(d.second)}Z"
    send(name=f"TEST send:{t}", message="test",
         description="test", last_received=t)
