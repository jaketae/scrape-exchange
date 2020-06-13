import requests

import bs4
from app.utils import check_num, floatify, parse, redirect, stringify


def make_soup(url):
    url = redirect(url)
    page = requests.get(url)
    return bs4.BeautifulSoup(page.text, "lxml")


def get_item_info(url):
    soup = make_soup(url)
    title = get_title(soup)
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
            price = check_num(item.find("div", {"class": "aafes-price"}).text.strip())
        except:
            try:
                price = check_num(
                    item.find("div", {"class": "aafes-price-sm"}).text.strip()
                )
            except:
                raw_price = item.find(
                    "span", {"class": "aafes-price-list"}
                ).text.strip()
                price = check_num(raw_price[raw_price.find("$") :])
    return title, floatify(price), redirect(url)


def get_title(soup):
    try:
        return soup.find("h1", class_="aafes-page-head mb-0").text.strip()
    except AttributeError:
        try:
            return soup.find("h1", class_="aafes-page-head").text.strip()
        except AttributeError:
            return soup.find("h1", class_="mb-0").text.strip()


def scrape_names(soup):
    return [
        div.find("a").contents[0].strip()
        for div in soup.find_all("div", {"class": "aafes-item-name"})
    ]


def scrape_prices(soup):
    items = soup.find_all("div", {"class": "item-pricing mt-1"})
    prices = []
    for item in items:
        try:
            price = check_num(
                "".join(
                    item.find("div", {"class": "aafes-price-sale"})
                    .text.strip()
                    .replace(" Sale", "")
                    .split()
                )
            )
        except:
            try:
                price = check_num(
                    item.find("div", {"class": "aafes-price"}).text.strip()
                )
            except:
                try:
                    price = check_num(
                        item.find("div", {"class": "aafes-price-sm"}).text.strip()
                    )
                except:
                    price = "None"
        prices.append(price)
    return prices


def get_summary(keyword):
    soup = make_soup(
        f"https://www.shopmyexchange.com/s?Dy=1&Nty=1&Ntt={parse(keyword)}"
    )
    names = scrape_names(soup)
    prices = scrape_prices(soup)
    return stringify(names, prices)
