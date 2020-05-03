from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class GoogleScholarElenium:
    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Chrome()
        self.driver.get(url)

    def click_title_on_main_page(self, title_text):
        elem = self.driver.find_element_by_link_text(title_text)
        elem.click()

    def click_cancel_on_paper_page(self):
        close_button = self.driver.find_element_by_id("gs_md_cita-d-x")
        close_button.click()
