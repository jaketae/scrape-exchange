# Exchange Web Scraper

This is a simple web scraper that crawls the [PX Exchange](http://www.shopmyexchange.com), a shopping website for U.S. soldiers and veterans. 

## Motivation

The website sporadically offers sales on many items---in most cases without prior notice---which is why it is often difficult for people to purchase items that they want at the cheapest price possible. When people hear about ongoing sales, they often realize that the sale has already expired, and that they are late to the game.

## Functionality

As it stands, the program is able to scrape contents of the Exchange website given a specified keyword. It will return a summary of the items matching the keyword alongside its price, all on a single table. 

Known Bugs:
- The scraper fails when an item is sold out

Features to Come:
- Build a GUI that allows users to input and save items in a wish list
- Inform the user via email whenever a price change occurs for any given item in the wish list

## Usage

As it stands, the application requires the following dependencies:

```
bs4
pandas
requests
```

Clone the repository and first run the following command on the shell to create a Conda virutal environment installed with the dependencies listed above. Then, activate the environment.

```bash
conda env create -f environment.yml
conda activate exchange-scrape
```

The `demo` script can be used to test run the application. To run, type

```bash
python -m demo
```

You will be asked to input a product. The program will print a table listing the first twelve product entries matching your search keyword along with their respective prices. 

