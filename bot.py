import os
from flask import Flask, request, redirect
from pymessenger.bot import Bot
from app.scraper import Scraper


app = Flask(__name__)
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
bot = Bot(ACCESS_TOKEN)


@app.route('/')
def get_started():
    gs_obj = {"get_started": {
        "payload": "Welcome! Please type the name of a product you're interested in."}}
    bot.set_get_started(gs_obj)
    bot.remove_get_started()
    return redirect('/summary')


@app.route('/summary', methods=['GET', 'POST'])
def send_summary():
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
                    prompt = 'Choose from the following options.'
                    buttons = [{
                        "type": "postback",
                        "title": "Send me the price!",
                        "payload": "<STRING_SENT_TO_WEBHOOK>"
                    }]
                    bot.send_button_message(recipient_id, prompt, buttons)
                    # scraper = Scraper(keyword)
                    # summary, _ = scraper.scrape()
                    # bot.send_text_message(recipient_id, summary)
        return 'Message Processed'


if __name__ == '__main__':
    app.run()
