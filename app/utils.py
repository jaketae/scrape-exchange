from collections import defaultdict



def parse(keyword):
    keyword = str(keyword).replace(' ', '+')
    return keyword


def concatenate(names, prices):
    summary = ''
    price_record = defaultdict()
    if len(prices) == 0:
        summary = 'There are no results to show.'
    else:
        for name, price in zip(names, prices):
            if price[0] == '$':
                summary += f'{name}: {price}\n'
                price_record[name] = price
        if len(summary) == 0:
            summary = 'There are no results to show.'
    return summary, price_record


def send_alert(receiver_email):
    port = 587
    smtp_server = "smtp.gmail.com"
    # To-do: Create bot email account
    sender_email = "some_email@gmail.com"
    sender_password = "some_password"
    # To-do: Add more info to email
    message = """\
    Subject: Price alert
    The price of a product on your wish list has dropped.""" 
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls(context=context)
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message)
        print("==========Email sent!==========")
    except Exception as e:
        print(e)


# To-do: Convert string to float for price comparison
# NEED TO MODIFY SO THAT IT CAN CHECK CURRENT PRICE OF AN ITEM 
def check_price(table, threshold):
    bool_idx = table['price'] < threshold
    if sum(bool_idx):
        lowered_table = table[bool_idx]
        return lowered_table
    else:
        return False
