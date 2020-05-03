import requests
import random
from lxml.html import fromstring


def get_proxies():
    url = "https://free-proxy-list.net/"
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = []
    for i in parser.xpath("//tbody/tr")[:10]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            # Grabbing IP and corresponding PORT
            proxy = ":".join([i.xpath(".//td[1]/text()")[0], i.xpath(".//td[2]/text()")[0]])
            proxies.append(proxy)
    return proxies


if __name__ == "__main__":
    proxies = get_proxies()

    print(proxies)
