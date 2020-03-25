import os
import requests
from flask import Flask, request, redirect
from pymessenger.bot import Bot
from app.scraper import Scraper


app = Flask(__name__)
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
bot = Bot(ACCESS_TOKEN)
request_endpoint = f'{bot.graph_url}/me/messenger_profile'
gs_obj = {"get_started": {"payload": "get started"}}
_ = requests.post(request_endpoint, params=bot.auth_args, json=gs_obj)
flag_email = None
flag_messenger = None
email = None


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
                received_text(message, recipient_id)
    return 'Message processed'


def received_postback(message, recipient_id):
    global email
    global flag_email
    global flag_messenger
    postback = message['postback']['payload']
    if postback == 'get started':
        welcome_text = 'Hey there! I\'m PX bot. How can I help you?'
        buttons = [
            {"type": "web_url", "url": "https://www.shopmyexchange.com",
                "title": "Browse the Exchange"},
            {"type": "postback", "title": "Checkout item price",
                "payload": "price summary"},
            {"type": "postback", "title": "Setup price alert",
                "payload": "price alert"}
        ]
        bot.send_button_message(recipient_id, welcome_text, buttons)
    elif postback == 'price summary':
        summary_prompt = 'Type the name of a product you\'re interested in.'
        bot.send_text_message(recipient_id, summary_prompt)
    elif postback == 'price alert':
        alert_prompt = 'What is your preferred way of receiving notifications?'
        buttons = [
            {"type": "postback", "title": "Email",
                "payload": "email"},
            {"type": "postback", "title": "Facebook Messenger",
                "payload": "messenger"}
        ]
        bot.send_button_message(recipient_id, alert_prompt, buttons)
    elif postback == "email":
        email_prompt = 'What is your email address?'
        bot.send_text_message(recipient_id, email_prompt)
        flag_email = True
    elif postback == "messenger":
        confirm_text = 'Got it! I\'ll shoot you a message when there\'s an update.'
        bot.send_text_message(recipient_id, confirm_text)
    else:
        bot.send_text_message(recipient_id, 'Sorry, I don\'t recognize that.')


def received_text(message, recipient_id):
    keyword = message['message']['text']
    if flag_email:
        if '@' not in keyword:
            error_message = 'Please enter a valid email address.'
            bot.send_text_message(recipient_id, error_message)
        else:
            confirm_message = 'Email saved!'
            bot.send_text_message(recipient_id, confirm_message)
            email = keyword
    else:
        scraper = Scraper(keyword)
        wait_text = 'One mike...'
        bot.send_text_message(recipient_id, wait_text)
        summary, _ = scraper.scrape()
        bot.send_text_message(recipient_id, summary)


if __name__ == '__main__':
    app.run(threaded=True)
