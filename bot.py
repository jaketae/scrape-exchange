import os
from flask import Flask, request
from pymessenger.bot import Bot
from app.scraper import Scraper

app = Flask(__name__)
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
bot = Bot(ACCESS_TOKEN)


@app.route('/', methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        else:
            return 'Invalid verification token'
    else:
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('message'):
                    recipient_id = message['sender']['id']
                    keyword = message['message']['text']
                    scraper = Scraper(keyword)
                    summary = scraper.scrape()
                    bot.send_recipient(recipient_id, summary)
        return "Message Processed"


if __name__ == "__main__":
    app.run()