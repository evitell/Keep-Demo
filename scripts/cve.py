import requests
import xml.etree.ElementTree as ET
import io

URL = "https://cve.circl.lu/recent/cvelistv5.rss"

response = requests.get(URL)

data_s = response.text
title = None
description = None
data = ET.parse(io.StringIO(data_s))
for x in data.findall("./channel/item"):
    for y in x:
        # print(y.tag,y.text)
        if y.tag == "title":
            title = y.text
        elif y.tag == "description":
            description = y.text
    break

print(f"{title}:\t{description}")
