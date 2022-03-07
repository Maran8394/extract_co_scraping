from bs4 import BeautifulSoup
import requests


class LinksFetch(object):
    def __init__(self, url):
        self.url = url
        self.raw_html = requests.get(self.url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4)'
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}
                                     )

    def getter_links(self, cls_name):
        soup = BeautifulSoup(self.raw_html.content, "html.parser")
        links = soup.find_all(attrs={"class": cls_name}, href=True)
        LINKS_LIST = []
        for li in links:
            link = "https://extract.co" + li.get("href")
            LINKS_LIST.append(link)
        return LINKS_LIST

