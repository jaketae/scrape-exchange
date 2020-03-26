import bs4
import requests
from app.utils import floatify


class Tracker:

    def __init__(self, url):
        page = requests.get(url)
        self.soup = bs4.BeautifulSoup(page.text, 'lxml')

    @property
    def price(self):
        items = self.soup.find_all(
            "div", {"class": "aafes-pdp-price mt-1 jsRenderedPrice"})
        for item in items:
            try:
                price = ''.join(item.find(
                    "div", {"class": "aafes-price-sale"}).text.strip().replace(' Sale', '').split())
            except:
                try:
                    price = item.find(
                        "div", {"class": "aafes-price"}).text.strip()
                except:
                    try:
                        price = item.find(
                            "div", {"class": "aafes-price-sm"}).text.strip()
                    except:
                        price = 'None'
        return floatify(price)

    def check_price(self, old_price):
        return old_price > self.price
