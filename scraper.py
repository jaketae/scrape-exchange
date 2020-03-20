import bs4
import requests
import pandas as pd
from utils import parse

class Scraper:

	def __init__(self, keyword):
		keyword = parse(keyword)
		url ='https://www.shopmyexchange.com/s?Dy=1&Nty=1&Ntt=' + keyword
		page = requests.get(url)
		self.soup = bs4.BeautifulSoup(page.text)
		# self.soup = bs4.BeautifulSoup(page.text, 'lxml')

	def _scrape_names(self):
		self.names = []
		for div in self.soup.findAll("div", {"class": "aafes-item-name"}):
			self.names.append(div.find('a').contents[0])

	def _scrape_prices(self):
		self.prices = self.soup.findAll(
			"div", {"class": ["aafes-price", "aafes-price-sale"]})
		self.prices = list(filter(None, 
			[element.text.strip().replace(' Sale', '') for element in self.prices]))

	def scrape(self):
		self._scrape_names()
		self._scrape_prices()
		self.summary = pd.DataFrame({"names": self.names, "prices": self.prices})
