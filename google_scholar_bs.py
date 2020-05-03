import time
import json
import requests
from bs4 import BeautifulSoup

sleep_time = 0.2


class GoogleScholarBS:
    def __init__(self, main_url, headers, proxy):
        self.main_url = main_url
        self.headers = headers

        if proxy is None:
            self.proxies = None
            page = requests.get(main_url, headers=headers)
        else:
            self.proxies = {
                "http": f"{proxy}",
                "https": f"{proxy}",
            }

            page = requests.get(main_url, headers=headers, proxies=self.proxies)

        soup = BeautifulSoup(page.content, "html.parser")

        main_table = soup.find("tbody", {"id": "gsc_a_b"})
        entries = main_table.find_all("tr")
        num_papers = len(entries)
        self.title_texts = [None] * num_papers
        self.title_urls = [None] * num_papers
        self.citation_urls = [None] * num_papers
        self.papers = [None] * num_papers

        self.scrape_main_page(entries)

        self.citation_titles = []

        time.sleep(sleep_time)

    def scrape_main_page(self, entries):
        for index, entry in enumerate(entries):

            title_tag = entry.find("a", {"class": "gsc_a_at"})
            title_text = title_tag.text

            # year = int(entry.find("td", {"class": "gsc_a_y"}).find("span").text)

            citation_tag = entry.find("td", {"class": "gsc_a_c"})
            # citation_num = int(citation_tag.find("a").text)
            citation_url = citation_tag.find("a").get("href")

            self.title_texts[index] = title_text
            self.citation_urls[index] = citation_url
            self.papers[index] = {"Title": title_text, "Citation URL": citation_url}

        # with open('title_texts.json', 'w') as json_file:
        #     json.dump(self.title_texts, json_file, indent=4)

        # with open('citation_urls.json', 'w') as json_file:
        #     json.dump(self.citation_urls, json_file, indent=4)

    def scrape_citation_page(self, index, page_url):
        page = requests.get(page_url, headers=self.headers)
        soup = BeautifulSoup(page.content, "html.parser")

        url_list = []
        citation_titles = []

        print(page_url)

        with open("output1.html", "w") as file:
            file.write(str(soup))

        # get all pages first
        # navigation = soup.find('div', {"id": "gs_n"})
        # if navigation is not None:
        #     print("Navigation pane found")
        #     sub_urls = navigation.find_all("td")

        #     for sub_url in sub_urls:
        #         url = sub_url.find("a")
        #         if url is not None:
        #             url_list.append("https://scholar.google.com" + url.get("href"))

        #     for url in url_list[1:-2]:
        #         print(url)
        #         time.sleep(sleep_time)
        #         page = requests.get(url, headers=self.headers)
        #         soup = BeautifulSoup(page.content, "html.parser")

        citations_all = soup.find_all("h3", {"class": "gs_rt"})

        for citation in citations_all:
            citation_title = citation.find("a").text
            citation_titles.append(citation_title)

        self.papers[index]["Citations"] = citation_titles

        # with open('citation_titles.json', 'w') as json_file:
        #     json.dump(self.citation_titles, json_file, indent=4)

    def scrape_all(self):
        for index, citation_url in enumerate(self.citation_urls):
            time.sleep(sleep_time)
            self.scrape_citation_page(index, citation_url)
            if index == 1:
                break

        with open("papers.json", "w") as json_file:
            json.dump(self.papers, json_file, indent=4)
