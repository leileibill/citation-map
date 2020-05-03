import requests
from bs4 import BeautifulSoup

proxies = {
  'http': 'http://178.128.53.246:8080',
  'https': 'http://178.128.53.246:8080',
}

page = requests.get('http://example.org', proxies=proxies)
soup = BeautifulSoup(page.content, "html.parser")

with open("output1.html", "w") as file:
            file.write(str(soup).replace(u'\xa0', u''))