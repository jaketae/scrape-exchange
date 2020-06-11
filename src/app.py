import os

import requests

from flask import Flask, redirect, request
from flask_sqlalchemy import SQLAlchemy
from pymessenger.bot import Bot
from src.crawler import *

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]

bot = Bot(os.environ["ACCESS_TOKEN"], api_version=6.0)
request_endpoint = f"{bot.graph_url}/me/messenger_profile"
gs_obj = {"get_started": {"payload": "get started"}}
_ = requests.post(request_endpoint, params=bot.auth_args, json=gs_obj)

default_prompt = "What next?"
return_prompt = "Welcome back! How can I help?"
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


db = SQLAlchemy(app)

track = db.Table(
    "track",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("item_id", db.Integer, db.ForeignKey("item.id"), primary_key=True),
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    messenger_id = db.Column(db.BigInteger, nullable=False)
    items = db.relationship(
        "Item", cascade="all,delete", secondary="track", backref="users"
    )


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    url = db.Column(db.String(500), nullable=False)


db.create_all()


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
        welcome_text = "Hey there! I'm PX bot. How can I help you? (To exit, you can type 'Bye' anytime.)"
        bot.send_button_message(recipient_id, welcome_text, buttons[:-1])
    elif payload == "price summary":
        summary_prompt = "Type the name of a product you're interested in."
        bot.send_text_message(recipient_id, summary_prompt)
    elif payload == "price alert":
        alert_prompt = "Which product do you want me to track?\n\nPro tip: Browse the Exchange and share the link with me via Messenger."
        bot.send_button_message(recipient_id, alert_prompt, [buttons[0]])
    # elif payload == "exit":
    #     exit_message = "If you need me again, simply type 'Hey' to wake me up!"
    #     bot.send_text_message(recipient_id, exit_message)
    elif payload == "stop track":
        send_item_buttons(recipient_id)
        # stop_message = "Which item(s) do you want me to stop tracking?"
        # bot.send_button_message(recipient_id, stop_message, make_buttons(recipient_id))
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
            print(item.title)
            buttons.append(
                {"type": "postback", "title": item.title, "payload": item.title}
            )
            if i % 3 == 2:
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
        bot.send_button_message(recipient_id, return_prompt, buttons[:-1])
    elif "bye" in text.lower():
        exit_message = "If you need me again, simply type 'Hey' to wake me up!"
        bot.send_text_message(recipient_id, exit_message)
    else:
        bot.send_text_message(recipient_id, get_summary(text))
        bot.send_button_message(recipient_id, default_prompt, buttons[1:])


def received_link(message, recipient_id):
    url = message["message"]["attachments"][0]["payload"]["url"]
    print(url)
    item = get_item(url)
    confirmation = f"I'll let you know when {item.title} get's cheaper!"
    bot.send_button_message(recipient_id, confirmation, buttons[1:])
    user = get_user(recipient_id)
    item.users.append(user)
    db.session.commit()


def test_received_link(url, recipient_id):
    item = get_item(url)
    confirmation = f"I'll let you know when {item.title} get's cheaper!"
    bot.send_button_message(recipient_id, confirmation, buttons[1:])
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


if __name__ == "__main__":
    app.run()
