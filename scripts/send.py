#!/usr/bin/env python3

import requests
import os
import datetime
import json


def send(
        name,
        message,
        description,
        service="backend",
        source=None,
        severity="critical",
        alert_url="https://www.keephq.dev?alertId=1235",
        status="firing",
        labels=None,
        ticket_url="https://www.keephq.dev?enrichedTicketId=456",
    # id="deea4282-2e8f-4418-822e-7012fa147aee",
    # fingerprint="eb3e9e19-91d1-4110-a79a-9f586adcdf24",
    last_received=None,
        keep_api_key=None):

    if last_received is None:
        last_received = get_timestr()

    if keep_api_key is None:
        keep_api_key = os.getenv("KEEP_API_KEY")
        if len(keep_api_key) != 36:
            print(f"WARNING: keep api key has {len(keep_api_key)} characters")

    if labels is None:
        labels = {
            "pod": "api-service-production",
            "region": "us-east-1",
            "cpu": "88",
            "memory": "100Mi"
        }

    if source is None:
        source = [
            "backend"
        ]

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
        "service": service,
        "source": source,

        "message": message,
        "description": description,
        "severity": severity,
        "pushed": True,
        "url": alert_url,
        "labels": labels,
        "ticket_url": ticket_url,
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


def get_timestr():
    d = datetime.datetime.now()
    t = f"{int_fmt(d.year)}-{int_fmt(d.month)}-{int_fmt(d.day)}T{int_fmt(d.hour)}:{int_fmt(d.minute)}:{int_fmt(d.second)}Z"
    return t


if __name__ == "__main__":

    send(name=f"TEST send", message="test",
         description="test")
