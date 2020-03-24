def parse(keyword):
    keyword = str(keyword).replace(' ', '+')
    return keyword


def concatenate(names, prices):
    summary = ''
    if len(prices) == 0:
        summary = 'There are no results to show.'
    else:
        for name, price in zip(names, prices):
            if price[0] == '$':
                summary += f'{name}: {price}\n'
        if len(summary) == 0:
            summary = 'There are no results to show.'
    return summary