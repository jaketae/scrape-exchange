from app.scraper import Scraper


def main():
    keyword = input("Which product are you interested in? ")
    scraper = Scraper(keyword)
    summary, price_record = scraper.scrape()
    print(summary)


if __name__ == '__main__':
    main()
