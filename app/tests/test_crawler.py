import pytest
import requests

import bs4


def test_get_item_info():
    from app.crawler import get_item_info

    result_1 = get_item_info(
        "https://www.shopmyexchange.com/apple-ipad-pro-11-in-1tb-with-wifi/1726802"
    )
    result_2 = get_item_info(
        "https://www.shopmyexchange.com/microsoft-surface-laptop-3-15-in-amd-ryzen-5-2-1ghz-16gb-ram-256gb-ssd/2152860"
    )
    result_3 = get_item_info(
        "https://www.shopmyexchange.com/omega-men-s-seamaster-300m-diver-s-stainless-steel-42mm-watch-o210304220030/1480816"
    )
    assert list(map(type, result_1)) == [str, int, str]
    assert list(map(type, result_2)) == [str, int, str]
    assert list(map(type, result_2)) == [str, int, str]
    title_result, _, url_result = zip(result_1, result_2, result_3)
    assert title_result == (
        "Apple iPad Pro 11 in. 1TB with WiFi",
        "Microsoft Surface Laptop 3 15 in. AMD Ryzen 5 2.1GHz 16GB RAM 256GB SSD",
        "Omega Men's Seamaster 300m Diver's  Stainless Steel 42mm Watch O210304220030",
    )
    for url in url_result:
        assert "https://www.shopmyexchange.com/" in url


def _build_soup(url):
    page = requests.get(url)
    return bs4.BeautifulSoup(page.text, "lxml")


soup_1 = _build_soup("https://www.shopmyexchange.com/s?Dy=1&Nty=1&Ntt=iPad+pro")
soup_2 = _build_soup("https://www.shopmyexchange.com/s?Dy=1&Nty=1&Ntt=samsung+tv")
soup_3 = _build_soup("https://www.shopmyexchange.com/s?Dy=1&Nty=1&Ntt=rolex")


def test_scrape_names():
    from app.crawler import scrape_names

    names_1 = scrape_names(soup_1)
    names_2 = scrape_names(soup_2)
    names_3 = scrape_names(soup_3)
    assert len(names_1) == sum(list(map(bool, names_1)))
    assert len(names_2) == sum(list(map(bool, names_2)))
    assert len(names_3) == sum(list(map(bool, names_3)))
    assert len(names_1) and len(names_2) and len(names_3)


def test_scrape_prices():
    from app.crawler import scrape_prices

    prices_1 = scrape_prices(soup_1)
    prices_2 = scrape_prices(soup_2)
    prices_3 = scrape_prices(soup_3)
    for prices in (prices_1, prices_2, prices_3):
        for price in prices:
            assert "$" in price or price == "None"
