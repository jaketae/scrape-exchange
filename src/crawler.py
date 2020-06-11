import requests

import bs4
from src.utils import floatify, parse, redirect, stringify


def get_item_info(url):
    url = redirect(url)
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.text, "lxml")
    title = soup.find("h1", class_="aafes-page-head mb-0").text
    item = soup.find("div", {"class": "aafes-pdp-price mt-1 jsRenderedPrice"})
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
    return title, floatify(price), url


def scrape_names(soup):
    names = []
    for div in soup.find_all("div", {"class": "aafes-item-name"}):
        names.append(div.find("a").contents[0])
    return names


def scrape_prices(soup):
    items = soup.find_all("div", {"class": "item-pricing mt-1"})
    prices = []
    for item in items:
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
                    price = "None"
        prices.append(price)
    return prices


def get_summary(keyword):
    url = f"https://www.shopmyexchange.com/s?Dy=1&Nty=1&Ntt={parse(keyword)}"
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.text, "lxml")
    names = scrape_names(soup)
    prices = scrape_prices(soup)
    return stringify(names, prices)
