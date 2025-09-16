import send
import weather
import random
import json
import requests
import time


def send_incomplete(loc_name, lat_long):
    try:
        w = weather.get_weather(lat_long)
    except requests.exceptions.ReadTimeout:
        time.sleep(1)
        w = weather.get_weather(loc)
    except:
        return

    current = w["current"]
    t = current["time"]

    data = {
        "time": t,
        "location": loc_name,
    }
    for k in ["temperature_2m", "relative_humidity_2m", "wind_speed_10m", " precipitation_probability", "precipitation"]:
        if random.choice([True, False]):
            data[k] = current[k]

    send.send(
        name=f"Weather in {loc_name}",
        message=json.dumps(data),
        description='',
        source=["incomplete_weather_source"],
        alert_url=f"https://en.wikipedia.org/{loc_name}",
        labels={}
    )


if __name__ == "__main__":
    for loc_name, loc in [("Stockholm", weather.STOCKHOLM), ("Gothenburg", weather.GOTHENBURG), ("Karlsruhe", weather.KARLSRUHE)]:
        send_incomplete(loc_name, loc)
