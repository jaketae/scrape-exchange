import bs4
import requests
import pandas as pd
from app.utils import parse



class Scraper:


	def __init__(self, keyword):
		keyword = parse(keyword)
		url ='https://www.shopmyexchange.com/s?Dy=1&Nty=1&Ntt=' + keyword
		page = requests.get(url)
		self.soup = bs4.BeautifulSoup(page.text, 'html.parser')
		# self.soup = bs4.BeautifulSoup(page.text, 'lxml')


	def _scrape_names(self):
		self.names = []
		for div in self.soup.find_all("div", {"class": "aafes-item-name"}):
			self.names.append(div.find('a').contents[0])


	def _scrape_prices(self):
		items = self.soup.find_all("div", {"class":"item-pricing mt-1"})
		self.prices = []
		for item in items:
			try:
				price = item.find("div", {"class": "aafes-price-sale"}).text.strip().replace(' Sale', '')
			except:
				try:
					price = item.find("div", {"class": "aafes-price"}).text.strip()
				except:
					price = item.find("div", {"class": "aafes-price-sm"}).text.strip()
			self.prices.append(price)


	def scrape(self):
		self._scrape_names()
		self._scrape_prices()
		assert len(self.names) == len(self.prices)
		# self.prices = [price for price in self.prices if price[0] == '$']
		# n_valid = len(self.prices)
		self.summary = pd.DataFrame({"names": self.names, "prices": self.prices})