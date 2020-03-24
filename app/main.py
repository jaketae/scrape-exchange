import time
from app.scraper import Scraper
from app.utils import send_alert, check_price

# keyword = input("Which product are you interested in? ")
# threshold = input("At what price to you want to be notified? ")
# receiver_email = input("What is your email address? ")
# print("Got it!")

while True:
    scraper = Scraper(keyword)
    scraper.scrape()
    table = scraper.summary