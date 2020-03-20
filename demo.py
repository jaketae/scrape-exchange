from app.scraper import Scraper

def main():
	keyword = input("Which product are you interested in? ")
	scraper = Scraper(keyword)
	scraper.scrape()
	print(scraper.summary)

if __name__ == '__main__':
	main()