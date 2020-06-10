from app.tracker import Tracker
from bot import bot, db


def cron_job():
    for item in db.session.query(Item).all():
        tracker = Tracker(item.url)
        if item.price != tracker.price:
            item.price = tracker.price
            url = item.url
            for user in item.users:
                update_user(user.messenger_id, url)


def update_user(messenger_id, url):
    # TODO: show prev_price, new_price
    message = f"Price dropped! Checkout at {url}"
    bot.send_text_message(messenger_id, message)


if __name__ == "__main__":
    cron_job()
