from app import db
from app.crawler import get_item_info
from app.models import *
from app.routes import bot


def cron_job():
    for item in db.session.query(Item).all():
        _, current_price, _ = get_item_info(item.url)
        if item.price != current_price:
            item.price = current_price
            db.session.commit()
            for user in item.users:
                alert_user(user.messenger_id, item)
        else:
            for user in item.users:
                inform_user(user.messenger_id, item.title)


def alert_user(messenger_id, item):
    message = (
        f"Price of {item.title} has dropped to ${item.price}! Checkout at {item.url}."
    )
    bot.send_text_message(messenger_id, message)


def inform_user(messenger_id, item_title):
    message = f"No price changes for {item_title} for now!"
    bot.send_text_message(messenger_id, message)


if __name__ == "__main__":
    print("Start!")
    cron_job()
    print("Done!")
