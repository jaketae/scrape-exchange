import os
import requests
from flask import Flask, request, redirect
from pymessenger.bot import Bot
from app.scraper import Scraper
from app.tracker import Tracker


app = Flask(__name__)
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
bot = Bot(ACCESS_TOKEN)

request_endpoint = f'{bot.graph_url}/me/messenger_profile'
gs_obj = {"get_started": {"payload": "get started"}}
_ = requests.post(request_endpoint, params=bot.auth_args, json=gs_obj)

default_prompt = 'What next?'
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

old_price = None


@app.route('/', methods=['GET'])
def verify():
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    else:
        return 'Invalid verification token'


@app.route('/', methods=['POST'])
def respond():
    global flag_email
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
    postback = message['postback']['payload']
    if postback == 'get started':
        welcome_text = 'Hey there! I\'m PX bot. How can I help you?'
        bot.send_button_message(recipient_id, welcome_text, buttons[:-1])
    elif postback == 'price summary':
        summary_prompt = 'Type the name of a product you\'re interested in.'
        bot.send_text_message(recipient_id, summary_prompt)
    elif postback == 'price alert':
        alert_prompt = 'What is the URL of the product you want me to track?'
        bot.send_text_message(recipient_id, alert_prompt)
    else:
        exit_message = 'If you need me next time, simply type \'Hey\' to wake me up.'
        bot.send_text_message(recipient_id, exit_message)


def received_text(message, recipient_id):
    keyword = message['message']['text']
    if keyword == 'Hey':
        bot.send_button_message(recipient_id, default_prompt, buttons[:-1])
    elif 'www' in keyword:
        if 'shopmyexchange' not in keyword:
            error_message = 'Please enter a valid URL.'
            bot.send_text_message(recipient_id, error_message)
        else:
            global old_price
            confirmation = 'Got it! I\'ll shoot you a message when there\'s an update.'
            bot.send_text_message(recipient_id, confirmation)
            bot.send_button_message(recipient_id, default_prompt, buttons[1:])
            old_price = Tracker(keyword).price
            log(f'Old price recorded as {old_price}')
    else:
        scraper = Scraper(keyword)
        summary, _ = scraper.scrape()
        bot.send_text_message(recipient_id, keyword)
        bot.send_button_message(recipient_id, default_prompt, buttons[1:])


if __name__ == '__main__':
    app.run(threaded=True)
