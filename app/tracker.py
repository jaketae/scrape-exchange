import bs4
import requests
from app.utils import floatify


class Tracker:

    def __init__(self, url):
        page = requests.get(url)
        self.soup = bs4.BeautifulSoup(page.text, 'lxml')

    @property
    def price(self):
        soup = self.soup
        item = soup.find(
            "div", {"class": "aafes-pdp-price mt-1 jsRenderedPrice"})
        assert item is not None
        try:
            price = ''.join(item.find(
                "div", {"class": "aafes-price-sale"}).text.strip().replace(' Sale', '').split())
        except:
            try:
                price = item.find(
                    "div", {"class": "aafes-price"}).text.strip()
            except:
                price = item.find(
                    "div", {"class": "aafes-price-sm"}).text.strip()
        return floatify(price)

    def check_price(self, old_price):
        return old_price > self.price
