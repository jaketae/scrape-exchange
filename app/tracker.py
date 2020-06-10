import requests

import bs4
from app.utils import floatify, redirect


class Tracker:
    def __init__(self, url):
        self.url = redirect(url)
        page = requests.get(self.url)
        self.soup = bs4.BeautifulSoup(page.text, "lxml")

    @property
    def price(self):
        item = self.soup.find("div", {"class": "aafes-pdp-price mt-1 jsRenderedPrice"})
        try:
            price = "".join(
                item.find("div", {"class": "aafes-price-sale"})
                .text.strip()
                .replace(" Sale", "")
                .split()
            )
        except:
            try:
                price = item.find("div", {"class": "aafes-price"}).text.strip()
            except:
                try:
                    price = item.find("div", {"class": "aafes-price-sm"}).text.strip()
                except:
                    price = 0
        return floatify(price)
