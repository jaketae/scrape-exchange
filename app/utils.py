import requests


def parse(keyword):
    return str(keyword).replace(" ", "+")


def stringify(names, prices):
    if len(prices) == 0:
        return "There are no results to show."
    summary = ""
    for name, price in zip(names, prices):
        try:
            assert price[0] == "$"
        except AssertionError:
            price = "Price not available"
        summary += f"{name}: {price}\n\n"
    if len(summary) == 0:
        return "There are no results to show."
    return summary[:-1]


def floatify(price):
    # price starts with a dollar sign
    if price == "None":
        return 0
    try:
        return int(float(price[1:].replace(",", "")))
    except:
        try:
            # price can take the form of "{}"
            return int(float(price[price.index("-") + 2 :].replace(",", "")))
        except:
            return price


def redirect(raw_url):
    replace = {
        "https://l.messenger.com/l.php?u=": "",
        "https://l.facebook.com/l.php?u=": "",
        "%3A": ":",
        "%2F": "/",
        "%3F": "?",
        "%3D": "=",
    }
    if not ("messenger.com" in raw_url or "facebook.com" in raw_url):
        return raw_url
    for key, value in replace.items():
        raw_url = raw_url.replace(key, value)
    return raw_url[: raw_url.index("&h")]


def check_num(raw_price):
    if len(set("0123456789") - set(raw_price)) != 10:
        return raw_price
    raise ValueError
