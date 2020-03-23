import bs4
import requests
import json
from collections import OrderedDict
from app.utils import parse



class Scraper:


	def __init__(self, keyword):
		keyword = parse(keyword)
		url ='https://www.shopmyexchange.com/s?Dy=1&Nty=1&Ntt=' + keyword
		page = requests.get(url)
		self.soup = bs4.BeautifulSoup(page.text, 'lxml')


	def _scrape_names(self):
		names = []
		for div in self.soup.find_all("div", {"class": "aafes-item-name"}):
			names.append(div.find('a').contents[0])
		return names


	def _scrape_prices(self):
		items = self.soup.find_all("div", {"class":"item-pricing mt-1"})
		prices = []
		for item in items:
			try:
				price = item.find("div", {"class": "aafes-price-sale"}).text.strip().replace(' Sale', '')
			except:
				try:
					price = item.find("div", {"class": "aafes-price"}).text.strip()
				except:
					price = item.find("div", {"class": "aafes-price-sm"}).text.strip()
			prices.append(price)
		return prices

	# To-do: Only show valid entries
	# (i.e. Exclude "Coming soon")
	def scrape(self):
		names = self._scrape_names()
		prices = self._scrape_prices()
		summary = [OrderedDict([('Name', name), ('Price', price)]) for name, price in zip(names, prices)]
		json_summary = json.dumps(summary)
		return json_summary
