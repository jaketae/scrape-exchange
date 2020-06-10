import requests

import bs4


def parse(keyword):
    keyword = str(keyword).replace(" ", "+")
    return keyword


def stringify(names, prices):
    summary = ""
    if len(prices) == 0:
        summary = "There are no results to show."
    else:
        for name, price in zip(names, prices):
            if price[0] == "$":
                name = name[:-1]
                summary += f"{name}: {price}\n\n"
        if len(summary) == 0:
            summary = "There are no results to show."
        else:
            summary = summary[:-1]
    return summary


def floatify(price):
    try:
        price = float(price[1:].replace(",", ""))
    except:
        try:
            price = float(price[price.index("-") + 2 :].replace(",", ""))
        except:
            pass
    return price


# def redirect(url):
#     page = requests.get(replace_all(url))
#     soup = bs4.BeautifulSoup(page.content, "lxml")
#     url = soup.find("span", class_="_5slv").text
#     return url


def redirect(raw_url):
    replace = {
        "https://l.messenger.com/l.php?u=": "",
        "%3A": ":",
        "%2F": "/",
        "%3F": "?",
        "%3D": "=",
    }
    for key, value in replace.items():
        raw_url = raw_url.replace(key, value)
    return raw_url[: raw_url.index("&h")]
