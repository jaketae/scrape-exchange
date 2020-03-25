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

email, temp_email, flag_email, flag_messenger = None, None, None, None


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
    global email
    global flag_email
    global temp_email
    global flag_messenger
    postback = message['postback']['payload']
    if postback == 'get started':
        welcome_text = 'Hey there! I\'m PX bot. How can I help you?'
        bot.send_button_message(recipient_id, welcome_text, buttons[:-1])
    elif postback == 'price summary':
        summary_prompt = 'Type the name of a product you\'re interested in.'
        bot.send_text_message(recipient_id, summary_prompt)
    elif postback == 'price alert':
        alert_prompt = 'How do you want to receive notifications?'
        notification = [
            {"type": "postback", "title": "Email",
                "payload": "email"},
            {"type": "postback", "title": "Facebook Messenger",
                "payload": "messenger"}
        ]
        bot.send_button_message(recipient_id, alert_prompt, notification)
    elif postback == "email":
        email_prompt = 'What\'s your email address?'
        bot.send_text_message(recipient_id, email_prompt)
        flag_email = True
    elif postback == "messenger":
        confirm_text = 'Got it! I\'ll shoot you a message when there\'s an update.'
        bot.send_text_message(recipient_id, confirm_text)
        bot.send_button_message(recipient_id, default_prompt, buttons)
        flag_messenger = True
    elif postback == 'yes':
        override_text = 'Roger. I\'ve updated your email information!'
        bot.send_text_message(recipient_id, override_text)
        bot.send_button_message(recipient_id, default_prompt, buttons)
        email = temp_email
    elif postback == 'no':
        keep_text = 'I\'ll keep the email address I have.'
        bot.send_text_message(recipient_id, keep_text)
        bot.send_button_message(recipient_id, default_prompt, buttons)
    elif postback == 'exit':
        exit_message = 'Glad I could help. If you need me next time, send me any text!'
        bot.send_text_message(recipient_id, exit_message)
    else:
        welcome_text = 'Hey there! I\'m PX bot. How can I help you?'
        bot.send_button_message(recipient_id, welcome_text, buttons[:-1])


def received_text(message, recipient_id):
    global email
    global flag_email
    global temp_email
    keyword = message['message']['text']
    if flag_email:
        if email is None:
            if not ('@' in keyword and '.' in keyword):
                error_message = 'Please enter a valid email address.'
                bot.send_text_message(recipient_id, error_message)
            else:
                confirm_message = 'Email saved!'
                bot.send_text_message(recipient_id, confirm_message)
                email = keyword
                flag_email = False
                bot.send_button_message(
                    recipient_id, default_prompt, buttons)
        else:
            temp_email = keyword
            override_message = 'I already have your email. Override?'
            yes_no = [
                {"type": "postback", "title": "Yes",
                 "payload": "yes"},
                {"type": "postback", "title": "No",
                 "payload": "no"}
            ]
            bot.send_button_message(recipient_id, override_message, yes_no)
            flag_email = False
    else:
        scraper = Scraper(keyword)
        wait_text = 'One mike...'
        bot.send_text_message(recipient_id, wait_text)
        summary, _ = scraper.scrape()
        bot.send_text_message(recipient_id, summary)
        bot.send_button_message(
            recipient_id, default_prompt, buttons)


if __name__ == '__main__':
    app.run(threaded=True)
