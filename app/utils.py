import bs4


def parse(keyword):
    keyword = str(keyword).replace(' ', '+')
    return keyword


def stringify(names, prices):
    summary = ''
    if len(prices) == 0:
        summary = 'There are no results to show.'
    else:
        for name, price in zip(names, prices):
            if price[0] == '$':
                name = name[:-1]
                summary += f'{name}: {price}\n\n'
        if len(summary) == 0:
            summary = 'There are no results to show.'
        else:
            summary = summary[:-1]
    return summary, price_record


def floatify(price):
    try:
        price = float(price[1:].replace(',', ''))
    except:
        price = float(price[price.index('-') + 2:].replace(',', ''))
    return price
