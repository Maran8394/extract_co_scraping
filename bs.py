from bs4 import BeautifulSoup
import requests
from itertools import chain
import logging


def page_loggers(log_name, text):
    logging.basicConfig(filename=f"logs/{log_name}.log", filemode="a", format='%(asctime)s - %(message)s',
                        datefmt='%d-%b-%y %H:%M:%S')
    l = logging.getLogger()
    l.setLevel(logging.INFO)
    l.info(text)


class Bs4_Scaping(object):
    def __init__(self, url):
        self.reviews_url = ""
        self.wap = ""
        self.url = url
        self.raw_html = requests.get(self.url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4)'
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}
                                     )

    def check_hired_products(self):
        hired = False

        soup = BeautifulSoup(self.raw_html.content, "html.parser")
        des = soup.find(attrs={"class": "projectdetails"})
        com_name = ""
        if des:
            com_name = des.find("h1", class_="").text
            com_name = com_name
            if "hired" in des.text or "HIRED" in des.text or "Hired" in des.text:
                hired = True
        else:
            hired = None

        clients = soup.find(attrs={"class": "client"})
        if clients:
            client_name = clients.find(attrs={"property": "name"}).text
            add = clients.find("address").text
            address_str = " ".join(add.split()).strip()
            comp_size = clients.find(attrs={"class": "info"}).text

            desg = clients.find_all("p")

            return [hired, com_name, client_name, desg[1].text, address_str, comp_size]
        else:
            return [None, None, None, None, None, None]

    def get_reviews_works(self):
        soup = BeautifulSoup(self.raw_html.content, "html.parser")
        reviews_url = soup.find_all("div", class_="viewall")
        review_url, wap = "", ""
        if len(reviews_url) == 2:
            review_url = "https://extract.co" + reviews_url[0].find("a").get('href')
            wap = "https://extract.co" + reviews_url[1].find("a").get('href')
            review_url = review_url
            wap = wap
            return [review_url, wap]
        else:
            review_url = "https://extract.co" + reviews_url[0].find("a").get('href')
            review_url = review_url
            return [review_url]

    def get_breif(self, cls_name, element):
        l = []
        soup = BeautifulSoup(self.raw_html.content, "html.parser")
        s = soup.find_all(element, class_=cls_name)

        for i in s:
            data = i.find_all(attrs={"class": "col-sm-8"})
            for j in data:
                removed_space_str = " ".join(j.text.split())
                l.append(removed_space_str)
        return l

    def get_name(self):

        soup = BeautifulSoup(self.raw_html.content, "html.parser")
        s = soup.find(attrs={"property": "name"})
        str_name = " ".join(s.text.split())

        address_locality = soup.find(attrs={"property": "addressLocality"})
        str_address_locality = " ".join(address_locality.text.split())

        country = soup.find(attrs={"property": "addressCountry"})
        str_country = " ".join(country.text.split())

        return {"name": str_name, "company_url": self.url, "state": str_address_locality, "country": str_country}

    def expertise(self):
        ratings = []
        expertise = []

        soup = BeautifulSoup(self.raw_html.content, "html.parser")
        s = soup.find_all("div", class_="skillbar")
        for c, i in enumerate(s):
            space_str = str(i.text).replace('\n', ' ').replace('\r', '').strip()
            if c >= 4:
                expertise.append(space_str)
            else:
                ratings.append(space_str)

        return expertise

    def industry_focus(self):
        soup = BeautifulSoup(self.raw_html.content, "html.parser")
        s = soup.find("ul", class_="pietag")
        space_str = str(s.text).replace('\n', ',').replace('\r', '').strip()
        return [space_str]

    def reviews_reader(self):
        self.url = self.reviews_url
        soup = BeautifulSoup(self.raw_html.content, "html.parser")
        s = soup.find_all("div", "reviewitem")

        l = []

        for i in s:
            comp_name = i.find(attrs={"property": "name"}).text
            client = i.find("div", "client")
            name = client.find(attrs={"property": "name"}).text

            address = client.find("address").text
            address_str = " ".join(address.split()).strip()

            company_size = client.find(attrs={"class": "info"}).text

            desg = client.find_all("p")
            fine_list = [comp_name, name, desg[1].text, address_str, company_size]

            l.append(fine_list)

        return list(chain(l))
