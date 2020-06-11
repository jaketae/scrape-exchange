import requests

import bs4

replace = {
    "https://l.messenger.com/l.php?u=": "",
    "https://l.facebook.com/l.php?u=": "",
    "%3A": ":",
    "%2F": "/",
    "%3F": "?",
    "%3D": "=",
}


def parse(keyword):
    return str(keyword).replace(" ", "+")


def stringify(names, prices):
    if len(prices) == 0:
        return "There are no results to show."
    summary = ""
    for name, price in zip(names, prices):
        if price[0] == "$":
            name = name[:-1]
            summary += f"{name}: {price}\n\n"
    if len(summary) == 0:
        return "There are no results to show."
    return summary[:-1]


def floatify(price):
    try:
        return float(price[1:].replace(",", ""))
    except:
        try:
            return float(price[price.index("-") + 2 :].replace(",", ""))
        except:
            return price


def redirect(raw_url):
    if not ("messenger.com" in raw_url or "facebook.com" in raw_url):
        return raw_url
    for key, value in replace.items():
        raw_url = raw_url.replace(key, value)
    return raw_url[: raw_url.index("&h")]
