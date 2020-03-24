import bs4
import requests
from collections import OrderedDict
from app.utils import parse, concatenate


class Scraper:

    def __init__(self, keyword):
        keyword = parse(keyword)
        url = f'https://www.shopmyexchange.com/s?Dy=1&Nty=1&Ntt={keyword}'
        page = requests.get(url)
        self.soup = bs4.BeautifulSoup(page.text, 'lxml')

    def _scrape_names(self):
        names = []
        for div in self.soup.find_all("div", {"class": "aafes-item-name"}):
            names.append(div.find('a').contents[0])
        return names

    def _scrape_prices(self):
        items = self.soup.find_all("div", {"class": "item-pricing mt-1"})
        prices = []
        for item in items:
            try:
                price = item.find(
                    "div", {"class": "aafes-price-sale"}).text.strip().replace(' Sale', '')
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
            prices.append(price)
        return prices

    def scrape(self):
        names = self._scrape_names()
        prices = self._scrape_prices()
        summary = concatenate(names, prices)
        return summary
