import os
from flask import Flask, request
from pymessenger.bot import Bot
from app.scraper import Scraper
from app.utils import send_alert, check_price

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
					table = scraper.bank()
					bot.send_text_message(recipient_id, summary)
					#Allows user to choose specific item 
					specific_item = input("Which specific product are you interested in? ")
					#Enter email address for future price drops
					receiver_email = input("What is your email address? ")
					#Weekly check to see if the price for that specific item dropped
					while True:
						price = check_price(specific_item)
						if price < table[specific_item]: 
							send_alert(receiver_email)
						time.sleep(7 * 24 * 60 * 60)
					
		return "Message Processed"
	
if __name__ == "__main__":
	app.run()
