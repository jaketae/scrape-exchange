import os

import requests

from app.scraper import Scraper
from app.tracker import Tracker
from flask import Flask, redirect, request
from flask_sqlalchemy import SQLAlchemy
# from models import *
from pymessenger.bot import Bot

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
    {"type": "postback", "title": "Exit conversation", "payload": "exit"},
]


db = SQLAlchemy(app)
db.drop_all()

track = db.Table(
    "track",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("item_id", db.Integer, db.ForeignKey("item.id")),
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    messenger_id = db.Column(db.String(200), nullable=False)
    items = db.relationship("Item", secondary="track", backref="users", lazy="True")


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
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
                bot.send_button_message(recipient_id, error_message, buttons[1:])
    return "Message processed"


def received_postback(message, recipient_id):
    payload = message["postback"]["payload"]
    if payload == "get started":
        welcome_text = "Hey there! I'm PX bot. How can I help you?"
        bot.send_button_message(recipient_id, welcome_text, buttons[:-1])
    elif payload == "price summary":
        summary_prompt = "Type the name of a product you're interested in."
        bot.send_text_message(recipient_id, summary_prompt)
    elif payload == "price alert":
        alert_prompt = "Which product do you want me to track?\n\nPro tip: Browse the Exchange and share the link with me via Messenger."
        bot.send_button_message(recipient_id, alert_prompt, [buttons[0]])
    else:
        exit_message = "If you need me again, simply type 'Hey' to wake me up!"
        bot.send_text_message(recipient_id, exit_message)


def received_text(message, recipient_id):
    text = message["message"]["text"]
    if "hey" in text.lower():
        bot.send_button_message(recipient_id, return_prompt, buttons[:-1])
    else:
        scraper = Scraper(text)
        summary = scraper.scrape()
        bot.send_text_message(recipient_id, summary)
        bot.send_button_message(recipient_id, default_prompt, buttons[1:])


def received_link(message, recipient_id):
    url = message["message"]["attachments"][0]["payload"]["url"]
    confirmation = "I'll let you know when the price drops!"
    bot.send_button_message(recipient_id, confirmation, buttons[1:])
    item = get_item(url)
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
    tracker = Tracker(url)
    item = Item(price=tracker.price, url=url)
    db.session.add(item)
    db.session.commit()
    return item


if __name__ == "__main__":
    app.run()
