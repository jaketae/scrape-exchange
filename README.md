# PX Exchange Chatbot

This is a simple web scraper-turned-chatbot for [PX Exchange](http://www.shopmyexchange.com), a shopping website for U.S. soldiers and veterans. The chatbot, which runs on Facebook's Messenger platform, provides a convenient way for users to inquire about product prices and price changes on a real-time basis.

## Motivation

The Exchange often holds bulk sales on multiple items without prior notice, making it difficult for people to purchase items at their cheapest price points. When people hear about ongoing sales and browse the website, they often realize to their dismay that the sale has already expired. 

# Setup

The application requires the following dependencies:

```
beautifulsoup4==4.8.2
Flask==1.1.1
flask-sqlalchemy==2.4.1
gunicorn==20.0.4
lxml==4.5.0
psycopg2==2.8.4
pymessenger==0.0.7.0
```

To clone the repository, navigate into a directory and run

```bash
git clone https://github.com/jaketae/scrape-exchange.git
```

## Release Notes

As it stands, users are able to use the chatbot to obtain a price summary of items given a keyword (demo screenshot shown below), and also ask the chatbot to track a specific product given a URL. If the price changes, the bot will send a text message to the user.


v.2020.03.2X:
* Initialize the repository
* Implement basic price scraping functionality via `scraper.py`
* Attempt email updates to users via `smtp`

v.2020.03.3X:
* Add `tracker.py` for price tracking
* Use `Flask` and `pymessenger` to shift the project to a chatbot
* Deploy application to Heroku 
* Attempt database initialization and integration with PostgreSQL

v.2020.06.0X:
* Reorganize DB schema from a single table to a many-to-many model
* Make full use of `flask-sqlalchemy` for full-fledged price tracking
* Use GitHub Actions for DB update cron job


## Contributing

Please feel free to submit an issue or a pull request, should you find any bugs or rooms for improvement. The code style is dictated by [black](https://pypi.org/project/black/#installation-and-usage). 


## Example

Below is a screenshot of the chatbot taken directly from Facebook Messenger. 

![ScreenShot](/images/screenshot.png)

The end goal is to provide a user-friendly interface through this platform. However, for simpler beta-testing and debugging purposes, the `demo.py` script can be used. To run this script, type

```bash
python -m demo
```

You will be asked to input a product. The program will print a table listing the first twelve product entries matching your search keyword along with their respective prices. Below is a simple demonstration of the application using the keyword `ipad pro`. 

```bash
Which product are you interested in? ipad pro
                                                names                       prices
0              Apple iPad Pro 11 in. 512GB with WiFi                   Coming Soon
1           Apple iPad Pro 12.9 in. 512GB  with WiFi                   Coming Soon
2            Apple iPad Pro 12.9 in. 256GB with WiFi                   Coming Soon
3          Apple iPad Pro 12.9 in. 128GB  with Wi-Fi                   Coming Soon
4              Apple iPad Pro 11 in. 128GB with WiFi                   Coming Soon
5   Tucano 11 in. Guscio Military Grade Protective...  Log in for Exchange pricing
6              Apple iPad Pro 12.9 in. 1TB with WiFi                   Coming Soon
7              Apple iPad Pro 11 in. 256GB with WiFi                   Coming Soon
8   Twelve South BookBook Vol. 2 for  iPad Pro 12....  Log in for Exchange pricing
9                Apple iPad Pro 11 in. 1TB with WiFi                   Coming Soon
10                 UAG Metropolis iPad Pro 10.5 Case   Log in for Exchange pricing
11             Apple iPad Pro 11 in. 256GB with WiFi                       $938.00
12             Apple iPad Pro 11 in. 512GB with WiFi                     $1,139.00
13               Apple iPad Pro 11 in. 1TB with WiFi                     $1,349.00
14         Apple Smart Keyboard for 10.5 in iPad Pro                       $158.00
15             Apple iPad Pro 12.9 in. 1TB with WiFi                     $1,549.00
16            Apple iPad Pro 12.9 in. Leather Sleeve                       $148.00
17       Apple iPad Pro 12.9 in. Leather Smart Cover                        $78.00
18  Twelve South BookBook Hard Leather Case for iP...                       $69.95
19              Apple iPad Pro 11 in. 64GB with WiFi                       $739.00
20  Gadget Guard - Black Ice Glass Screen Protecto...                       $38.95
21       Apple iPad Pro 10.5 in. Leather Smart Cover                        $68.00
22          Apple iPad Pro 12.9 in. 256GB with Wi-Fi                     $1,139.00
23           Apple iPad Pro 12.9 in. 64GB with Wi-Fi                       $989.00
24           Apple Smart Cover for iPad Pro 12.9 in.                        $58.00
25  Case-Mate Venture Folio for Apple iPad Pro 12....                       $42.95
26  Case-Mate - Edition Folio For Apple iPad Pro 1...                       $42.95
27  Apple Smart Keyboard Folio for 12.9 in. iPad P...                      $198.00
28               Catalyst Case for iPad 12.9 in. Pro                       $110.00
29            Apple iPad Pro 10.5 in. Leather Sleeve                       $128.00
30  Brydge 9.7 Bluetooth Keyboard For Apple iPad 9...                       $99.99
31           Apple iPad Pro 12.9 in. 512GB with WiFi                     $1,339.00
32           Apple Smart Cover for iPad Pro 10.5 in.                        $48.00
33    Twelve South Compass Pro for iPad Tablet Stand                        $55.00
34  Targus Pro-Tek Case for Apple iPad (7th gen.) ...  Log in for Exchange pricing
35                                 Apple AirPods Pro                       $248.00
```
