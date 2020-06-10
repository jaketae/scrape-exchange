from app.tracker import Tracker
from bot import Item, User, bot, db


def cron_job():
    for item in db.session.query(Item).all():
        current_price = Tracker(item.url).price
        if item.price != current_price:
            item.price = current_price
            db.session.commit()
            for user in item.users:
                update_user(user.messenger_id, item.url, current_price)


def update_user(messenger_id, url, price):
    message = f"Price dropped to ${price}! Checkout at {url}."
    bot.send_text_message(messenger_id, message)


if __name__ == "__main__":
    cron_job()
    print("Done!")
