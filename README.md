# PX Exchange Chatbot

This is a simple web scraper-turned-chatbot for [PX Exchange](http://www.shopmyexchange.com), a shopping website for U.S. soldiers and veterans. The chatbot, which runs on Facebook's Messenger platform, provides a convenient way for users to inquire about product prices and price changes on a real-time basis.

## Motivation

The Exchange often holds bulk sales on multiple items without prior notice, making it difficult for people to purchase items at their cheapest price points. When people hear about ongoing sales and browse the website, they often realize to their dismay that the sale has already expired. 

## Functionality

As it stands, the program is able to scrape contents of the Exchange website given a specified keyword. It will return a summary of the items matching the keyword alongside its price, all on a single table. 

Known Bugs:
- None at the moment, please feel free to file an issue or a PR

Fixed Bugs (v.2020.03.21):
- The scraper fails when an item is sold out
- "Log in for Exchange pricing" hinders scraping

Features to Come:
- Inform the user via email whenever a price change occurs for any given item in the wish list
- Allow users to narrow down their search (*e.g.* prevent airpods cases from showing up)

## Setup

As it stands, the application requires the following dependencies:

```
bs4
flask
requests
pymessenger
```

To clone the repository, navigate into a directory and run

```bash
git clone https://github.com/jaketae/scrape-exchange.git
```

## Example

With valid Facebook account credentials, anyone can test out the bot through Messenger by following [this link](m.me/pxpricebot). Below is a screenshot of the chatbot taken directly from Facebook Messenger. 

![ScreenShot](/images/screenshot.png)

The end goal is to provide a user-friendly interface through this platform. However, for simpler beta-testing and debugging purposes, the `demo.py` script can be used. To run this script, type

```bash
python -m demo
```

You will be asked to input a product. The program will print a table listing the first twelve product entries matching your search keyword along with their respective prices. Below is a simple demonstration of the application using the keyword `ipad`. 

```bash
Which product are you interested in? ipad
Apple iPad Pro 11 in. 1TB with WiFi (Latest Model): $1,299.00

Apple iPad Pro 11 in. 256GB with WiFi (Latest Model): $899.00

Apple iPad Pro 11 in. 512GB with WiFi (Latest Model): $1,099.00

Apple iPad Pro 12.9 in. 128GB with Wi-Fi (Latest Model): $999.00

Apple iPad Pro 12.9 in. 512GB with WiFi: $1,199.00

Apple iPad Pro 12.9 in. 1TB with WiFi: $1,399.00

Apple iPad Pro 11 in. 64GB with WiFi: $699.00

Apple iPad Pro 11 in. 256GB with WiFi: $788.00

Apple iPad Pro 11 in. 1TB with WiFi: $1,199.00

Apple iPad Pro 12.9 in. 256GB with Wi-Fi: $999.00

Apple iPad Pro 12.9 in. 64GB with Wi-Fi: $899.00

Apple iPad Pro 11 in. 512GB with WiFi: $999.00

Apple iPad Air 10.5 in. 256GB with WiFi: $549.00

Apple iPad mini 256GB with WiFi: $499.00

Apple iPad Air 10.5 in. 64GB with WiFi: $399.00

Apple iPad mini 64GB with WiFi: $389.00

```
