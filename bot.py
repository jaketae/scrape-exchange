import os
import atexit
import requests
from pymessenger.bot import Bot
from app.scraper import Scraper
from app.tracker import Tracker
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, redirect
from apscheduler.schedulers.background import BackgroundScheduler


dev = False
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
db = SQLAlchemy(app)
bot = Bot(ACCESS_TOKEN, api_version=6.0)
request_endpoint = f'{bot.graph_url}/me/messenger_profile'
gs_obj = {"get_started": {"payload": "get started"}}
_ = requests.post(request_endpoint, params=bot.auth_args, json=gs_obj)

recipient_id = ''
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


class Price(db.Model):
    __tablename__ = 'price'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(200))
    price = db.Column(db.Float)
    url = db.Column(db.String(200))

    def __init__(self, user, price, url):
        self.user = user
        self.price = price
        self.url = url


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
            global recipient_id
            recipient_id = message['sender']['id']
            if message.get('postback'):
                received_postback(message, recipient_id)
            elif message.get('message'):
                if message['message'].get('text'):
                    received_text(message, recipient_id)
                else:
                    received_link(message, recipient_id)
            else:
                error_message = 'Sorry, I don\'t understand that. Other way I can help?'
                bot.send_button_message(
                    recipient_id, error_message, buttons[1:])
    return 'Message processed'


def received_postback(message, recipient_id):
    payload = message['postback']['payload']
    if payload == 'get started':
        welcome_text = 'Hey there! I\'m PX bot. How can I help you?'
        bot.send_button_message(recipient_id, welcome_text, buttons[:-1])

    elif payload == 'price summary':
        summary_prompt = 'Type the name of a product you\'re interested in.'
        bot.send_text_message(recipient_id, summary_prompt)

    elif payload == 'price alert':
        alert_prompt = 'Which product do you want me to track?\n\nPro tip: Browse the Exchange and share the link with me via Messenger.'
        bot.send_button_message(recipient_id, alert_prompt, [buttons[0]])
    else:
        exit_message = 'If you need me again, simply type \'Hey\' to wake me up!'
        bot.send_text_message(recipient_id, exit_message)


def received_text(message, recipient_id):
    text = message['message']['text']
    if 'hey' in text.lower():
        bot.send_button_message(recipient_id, return_prompt, buttons[:-1])
    else:
        scraper = Scraper(text)
        summary = scraper.scrape()
        bot.send_text_message(recipient_id, summary)
        bot.send_button_message(recipient_id, default_prompt, buttons[1:])


def received_link(message, recipient_id):
    link = message['message']['attachments'][0]['payload']['url']
    price = Tracker(link).price
    confirmation = f'I\'ll let you know when price falls below the current ${price}. {default_prompt}'
    bot.send_button_message(recipient_id, confirmation, buttons[1:])
    data = Price(recipient_id, price, link)
    db.session.add(data)
    db.session.commit()



# def check_price(recipient_id):
#     message = 'Price dropped! Check out this link.'
#     target = Price.query.filter_by(user=recipient_id).all()
#     for entry in target:
#         url = entry.url
#         old_price = entry.price
#         if old_price > Tracker(url).price:
#             button = [{"type": "web_url", "url": url,
#                        "title": "Check out item"}]
#             bot.send_button_message(recipient_id, message, button)


# cron = BackgroundScheduler(daemon=True)
# cron.add_job(check_price, 'cron', args=[recipient_id], hour=8, timezone='UTC')
# cron.start()
# atexit.register(lambda: cron.shutdown())


if __name__ == '__main__':
    app.run(threaded=True)
