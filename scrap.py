from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


class Scraping:
    def __init__(self, url):
        self.url = url
        self.service = Service(executable_path="C:/SeleniumDrivers/chromedriver.exe")
        self.driver = webdriver.Chrome(service=self.service)
        self.driver.minimize_window()

    def get_link(self, cls_name):
        self.driver.get(self.url)
        da = self.driver.find_elements(By.CLASS_NAME, cls_name)
        links_list = []
        for i in da:
            a = i.get_attribute('href')
            links_list.append(a)
        self.driver.quit()
        return links_list

    def single_page_scrap(self, url):
        self.driver.get(self.url)


