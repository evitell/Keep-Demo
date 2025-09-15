import send
import cve
import time


def main():
    cves = cve.fetch_cves()
    for c in cves:
        send.send(
            name=c["title"],
            message="a CVE",
            description=c["description"],
            source="CVE:s",
            labels={
                "label": "security"
            },
            alert_url=c["link"]
        )
        time.sleep(1)


if __name__ == "__main__":
    main()
