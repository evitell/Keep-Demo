import send


def main():
    t = send.get_timestr()

    loc_name = "Stockholm"
    s = f"Stockholm {t}: temperature is -12.3 °C"
    s_desc = f"Temperature update in {loc_name}"
    send.send(
        name=s,
        message=f"{s_desc} update in {loc_name}",
        description=s_desc,
        source=["weather_gods"],
        labels={
            "weather": "true",
            "weather_type": s_desc.lower().replace(" ", "_"),
            "location": "Stockholm"
        },
        alert_url=f"https://en.wikipedia.org/{loc_name}",
    )


if __name__ == "__main__":
    main()
