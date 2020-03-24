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
        messaging = event['messaging']
        for message in messaging:
            recipient_id = message['sender']['id']
            if message.get('postback') and message["postback"]["payload"] == "get started":
                message = 'Welcome! To begin, type the name of a product you\'re interested in.'
                bot.send_text_message(recipient_id, message)
            elif message.get('message'):
                keyword = message['message']['text']
                scraper = Scraper(keyword)
                wait_text = 'One mike...'
                bot.send_text_message(recipient_id, wait_text)
                summary, _ = scraper.scrape()
                bot.send_text_message(recipient_id, summary)
    return 'Message processed'


if __name__ == '__main__':
    app.run()
