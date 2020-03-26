import os
import requests
from flask import Flask, request, redirect
# from flask_sqlalchemy import SQLAlchemy
from pymessenger.bot import Bot
from app.scraper import Scraper
from app.tracker import Tracker


dev = False
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

if dev:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost/pricebot'
    ACCESS_TOKEN = 'EAADgVEsrncIBAMYo5ZByh97atuawSDMucDv7Ql9kZA1pbPTpviZCxf65QDEgwCZAeYTMSfRD0UWddkRHUDMZBg8imFh04ZAQycRQt3KOtC047pWRqjoGnrzwj6i0Swer6GGQ0TU3J3p8ttKCoR89ZAMZAdaitTwItYjsnnNd7dhxwtYb97doKj2QlgQhcYG8ZBEcZD'
    VERIFY_TOKEN = 'UNIQUE TOKEN'
else:
    # app.config['SQLALCHEMY_DATABASE_URI'] = ''
    ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
    VERIFY_TOKEN = os.environ['VERIFY_TOKEN']

# db = SQLAlchemy(app)
bot = Bot(ACCESS_TOKEN, api_version=6.0)
request_endpoint = f'{bot.graph_url}/me/messenger_profile'
gs_obj = {"get_started": {"payload": "get started"}}
_ = requests.post(request_endpoint, params=bot.auth_args, json=gs_obj)

flag = None
default_prompt = 'What next?'
return_prompt = 'Welcome back! How can I help?'
buttons = [
    {"type": "web_url", "url": "https://www.shopmyexchange.com",
     "title": "Browse the Exchange"},
    {"type": "postback", "title": "Check out item price",
     "payload": "price summary"},
    {"type": "postback", "title": "Set up price alert",
     "payload": "price alert"},
    {"type": "postback", "title": "Exit conversation",
     "payload": "exit"}
]


# class Price(db.Model):
#     __tablename__ = 'price'
#     id = db.Column(db.Integer, primary_key=True)
#     user = db.Column(db.String(200))
#     price = db.Column(db.Float)
#     url = db.Column(db.String(200))

#     def __init__(self, price, url):
#         self.user = user
#         self.price = price
#         self.url = url


@app.route('/', methods=['GET'])
def verify():
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    else:
        return 'Invalid verification token'


@app.route('/', methods=['POST'])
def respond():
    output = request.get_json()
    for event in output['entry']:
        for message in event['messaging']:
            recipient_id = message['sender']['id']
            if message.get('postback'):
                received_postback(message, recipient_id)
            elif message.get('message'):
                if message['message'].get('text'):
                    received_text(message, recipient_id)
                else:
                    received_link(message, recipient_id)
    return 'Message processed'


def received_postback(message, recipient_id):
    global flag
    flag = False
    payload = message['postback']['payload']
    if payload == 'get started':
        welcome_text = 'Hey there! I\'m PX bot. How can I help you?'
        bot.send_button_message(recipient_id, welcome_text, buttons[:-1])

    elif payload == 'price summary':
        summary_prompt = 'Type the name of a product you\'re interested in.'
        bot.send_text_message(recipient_id, summary_prompt)

    elif payload == 'price alert':
        flag = True
        alert_prompt = 'What is the URL of the product you want me to track?'
        bot.send_button_message(recipient_id, alert_prompt, [buttons[0]])
    else:
        exit_message = 'If you need me again, simply type \'Hey\' to wake me up!'
        bot.send_text_message(recipient_id, exit_message)


def received_text(message, recipient_id):
    # bot.send_text_message(recipient_id, str(message['message']))
    global flag
    text = message['message']['text']
    if 'Hey' in text:
        bot.send_button_message(recipient_id, return_prompt, buttons[:-1])

    elif flag:
        if 'shopmyexchange.com' not in text:
            error_message = 'Please enter a valid URL.'
            bot.send_text_message(recipient_id, error_message)
        else:
            flag = False
            price = Tracker(text).price
            if price:
                confirmation = 'Got it! I\'ll shoot you a message when there\'s an update.'
                bot.send_text_message(recipient_id, confirmation)
                bot.send_button_message(
                    recipient_id, default_prompt, buttons[1:])
            else:
                error_message = 'Sorry, I can\'t track that URL.'
                bot.send_text_message(recipient_id, error_message)
                bot.send_button_message(
                    recipient_id, default_prompt, buttons[1:])
    else:
        scraper = Scraper(text)
        summary = scraper.scrape()
        bot.send_text_message(recipient_id, summary)
        bot.send_button_message(recipient_id, default_prompt, buttons[1:])


def received_link(message, recipient_id):
    # bot.send_text_message(recipient_id, str(message))
    link = message['message']['attachments'][0]['payload']['url']
    price = Tracker(link).price
    bot.send_text_message(recipient_id, price)


# def notify(recipient_id):


if __name__ == '__main__':
    app.run(threaded=True)
