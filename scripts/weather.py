import requests
import send
import time
import random

STOCKHOLM = (59.329444, 18.068611)

GOTHENBURG = (57.7075, 11.9675)

KARLSRUHE = (49.00921, 8.403951)


def get_weather(lat_long):

    params = (
        ('latitude', lat_long[0]),
        ('longitude', lat_long[1]),
        ('current', 'temperature_2m,relative_humidity_2m,wind_speed_10m'),
        # ('hourly', 'temperature_2m,relative_humidity_2m,wind_speed_10m'),
        ('hourly', ''),
    )

    response = requests.get(
        'https://api.open-meteo.com/v1/forecast',  params=params, timeout=10)
    if not response.ok:
        raise Exception(response.text, response.status_code, response.reason)

    return response.json()


def main():
    for loc_name, loc in [("Stockholm", STOCKHOLM), ("Gothenburg", GOTHENBURG), ("Karlsruhe", KARLSRUHE)]:
        try:
            w = get_weather(loc)
        except requests.exceptions.ReadTimeout:
            time.sleep(1)
            w = get_weather(loc)
        except:
            print(f"Skipping {loc_name} due to timeout reached")
            continue

        current = w["current"]
        t = current["time"]
        temperature = current["temperature_2m"]
        rel_hum = current["relative_humidity_2m"]
        ws = current["wind_speed_10m"]
        s_temp = f"{loc_name} {t}: temperature is {temperature} °C"
        s_rh = f"{loc_name} {t}: relative humidity is {rel_hum} %"
        s_ws = f"{loc_name} {t}: wind speed is is {ws} km/h"

        for s_desc, s in [("Temperature", s_temp), ("Relative humidity", s_rh), ("Wind speed", s_ws)]:
            print(f"Sending {s_desc.lower()} update for {loc_name}")
            send.send(
                name=s,
                message=f"{s_desc} update in {loc_name}",
                description="",
                source=["weather gods"],
                labels={
                    "weather": "true",
                    "weather_type": s_desc.lower().replace(" ", "_"),
                    "location": loc_name
                },
                alert_url=f"https://en.wikipedia.org/{loc_name}",
            )
            time.sleep(1)

        time.sleep(random.randint(1, 3))


if __name__ == "__main__":
    main()
