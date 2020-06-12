import os

import requests

from app import app
from app.crawler import get_item_info, get_summary
from app.models import Item, User, db, track
from flask import request
from pymessenger.bot import Bot

bot = Bot(os.environ["ACCESS_TOKEN"], api_version=6.0)
request_endpoint = f"{bot.graph_url}/me/messenger_profile"
gs_obj = {"get_started": {"payload": "get started"}}
_ = requests.post(request_endpoint, params=bot.auth_args, json=gs_obj)


buttons = [
    {
        "type": "web_url",
        "url": "https://www.shopmyexchange.com",
        "title": "Browse the Exchange",
    },
    {"type": "postback", "title": "Check out item price", "payload": "price summary"},
    {"type": "postback", "title": "Set up price alert", "payload": "price alert"},
    # {"type": "postback", "title": "Exit conversation", "payload": "exit"},
    {"type": "postback", "title": "Stop price tracking", "payload": "stop track"},
]

dev = True


@app.route("/", methods=["GET"])
def verify():
    if request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
        return request.args.get("hub.challenge")
    else:
        return "Invalid verification token"


@app.route("/", methods=["POST"])
def respond():
    output = request.get_json()
    for event in output["entry"]:
        for message in event["messaging"]:
            recipient_id = message["sender"]["id"]
            if message.get("postback"):
                received_postback(message, recipient_id)
            elif message.get("message"):
                if message["message"].get("text"):
                    received_text(message, recipient_id)
                else:
                    received_link(message, recipient_id)
            else:
                error_message = "Sorry, I don't understand that. Other way I can help?"
                bot.send_button_message(recipient_id, error_message, buttons[:-1])
    return "Message processed"


def received_postback(message, recipient_id):
    payload = message["postback"]["payload"]
    if payload == "get started":
        bot.send_button_message(
            recipient_id,
            "Hey there! I'm PX bot. How can I help you? (To exit, you can type 'Bye' anytime.)",
            buttons[:-1],
        )
    elif payload == "price summary":
        bot.send_text_message(
            recipient_id, "Type the name of a product you're interested in."
        )
    elif payload == "price alert":
        bot.send_button_message(
            recipient_id,
            """Which product do you want me to track?\n\n
            Pro tip: Browse the Exchange and share the link with me via Messenger.""",
            [buttons[0]],
        )
    elif payload == "stop track":
        send_item_buttons(recipient_id)
    else:
        bot.send_text_message(
            recipient_id, f"I'll stop tracking {payload} as requested!"
        )
        stop_track(recipient_id, payload)


def send_item_buttons(messenger_id):
    items = db.session.query(User).filter_by(messenger_id=messenger_id).first().items
    if len(items) == 0:
        bot.send_text_message(
            messenger_id, "You haven't asked me to track anything yet."
        )
    else:
        buttons = []
        message = "Which item(s) do you want me to stop tracking?"
        for i, item in enumerate(items):
            if dev:
                print(item.title)
            buttons.append(
                {"type": "postback", "title": item.title, "payload": item.title}
            )
            if i % 3 == 2:
                if dev:
                    print(buttons)
                bot.send_button_message(messenger_id, message, buttons)
                buttons = []
                message = ""
        if buttons:
            bot.send_button_message(messenger_id, message, buttons)


def stop_track(messenger_id, item_title):
    user = User.query.filter_by(messenger_id=messenger_id).first()
    if item_title == "all items":
        user.items = []
    else:
        item = Item.query.filter_by(title=item_title)
        user.items.remove(item.first())
        if len(item.first().users) == 0:
            item.delete()
    db.session.commit()


def received_text(message, recipient_id):
    text = message["message"]["text"]
    if "hey" in text.lower():
        bot.send_button_message(
            recipient_id, "Welcome back! How can I help?", buttons[:-1]
        )
    elif "bye" in text.lower():
        exit_message = "If you need me again, simply type 'Hey' to wake me up!"
        bot.send_text_message(recipient_id, exit_message)
    else:
        bot.send_text_message(recipient_id, get_summary(text))
        bot.send_button_message(recipient_id, "What next?", buttons[1:])


def received_link(message, recipient_id):
    url = message["message"]["attachments"][0]["payload"]["url"]
    if dev:
        print(url)
    item = get_item(url)
    bot.send_button_message(
        recipient_id, f"I'll let you know when {item.title} gets cheaper!", buttons[1:]
    )
    user = get_user(recipient_id)
    item.users.append(user)
    db.session.commit()


def get_user(messenger_id):
    query_result = db.session.query(User).filter_by(messenger_id=messenger_id).first()
    if query_result:
        return query_result
    user = User(messenger_id=messenger_id)
    db.session.add(user)
    db.session.commit()
    return user


def get_item(url):
    query_result = db.session.query(Item).filter_by(url=url).first()
    if query_result:
        return query_result
    title, price, url = get_item_info(url)
    item = Item(title=title, price=price, url=url)
    db.session.add(item)
    db.session.commit()
    return item
