from datetime import datetime

def parse(keyword):
	keyword = str(keyword).replace(' ', '+')
	return keyword


def stringify(names, prices):
	result = ''
	if len(prices) == 0:
		result = 'There are no results to show.'
	else:
		for name, price in zip(names, prices):
			if price[0] == '$':
				result += f'{name}: {price}\n'
		if len(result) == 0:
			result = 'There are no results to show.'
	return result

def priceTracker(summary):
    price_record = []
    current_date = datetime.now();
    price_record.append({'date': current_date, 'info': summary});
    
                         
