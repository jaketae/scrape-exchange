from app import Item, User, bot, db
from crawler import get_price


def cron_job():
    for item in db.session.query(Item).all():
        current_price, _ = get_price(item.url)
        if item.price != current_price:
            item.price = current_price
            db.session.commit()
            for user in item.users:
                alert_user(user.messenger_id, item.url, current_price)
        else:
            for user in item.users:
                inform_user(user.messenger_id)


def alert_user(messenger_id, url, price):
    message = f"Price dropped to ${price}! Checkout at {url}."
    bot.send_text_message(messenger_id, message)


def inform_user(messenger_id):
    message = "No price changes for now!"
    bot.send_text_message(messenger_id, message)


if __name__ == "__main__":
    cron_job()
    print("Done!")
