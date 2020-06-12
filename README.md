# [PX Exchange Chatbot](https://web.facebook.com/pxpricebot/)

![build](https://github.com/jaketae/scrape-exchange/workflows/build/badge.svg) ![Update database](https://github.com/jaketae/scrape-exchange/workflows/Update%20database/badge.svg)


This is a simple web scraper-turned-chatbot for [PX Exchange](http://www.shopmyexchange.com), a shopping website for U.S. soldiers and veterans. The chatbot, which runs on Facebook's Messenger platform, provides a convenient way for users to inquire about product prices and price changes on a real-time basis.

## Motivation

The Exchange often holds bulk sales on multiple items without prior notice, making it difficult for people to purchase items at their cheapest price points. When people hear about ongoing sales and browse the website, they often realize to their dismay that the sale has already expired. 

## Tech Stack

The application uses the following dependencies:

```
beautifulsoup4
Flask
flask-sqlalchemy
gunicorn
lxml
psycopg2
pymessenger
```

The chatbot is a live web application deployed to Heroku on a PostgreSQL database, with automatic DB updates performed via GitHub Actions.

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

v.2020.06.1X:
* Reorganize DB schema from a single table to a many-to-many model
* Make use of `flask-sqlalchemy` for full-fledged price tracking
* Use GitHub Actions for DB update cron job, linting, and testing
* MVP release!


## Contributing

Please feel free to submit an issue or a pull request. The code style is dictated by [black](https://pypi.org/project/black/#installation-and-usage), and is checked for by the CI.


## Example

Below is a screenshot of the chatbot taken directly from Facebook Messenger. 

![ScreenShot](/images/screenshot.png)

More demos and documentations to come.
