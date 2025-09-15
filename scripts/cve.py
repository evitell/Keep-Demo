import requests
import xml.etree.ElementTree as ET
import io

URL = "https://cve.circl.lu/recent/cvelistv5.rss"
KEYS = ["guid", "title", "link", "description"]


def fetch_cves():
    response = requests.get(URL)

    data_s = response.text
    data = ET.parse(io.StringIO(data_s))

    cves = []
    for x in data.findall("./channel/item"):
        cve = {}

        for y in x:
            for key in KEYS:
                if y.tag == key:
                    cve[key] = y.text

        cves.append(cve)
    return cves


if __name__ == "__main__":
    cves = fetch_cves()
    for cve in cves:
        print(cve)
