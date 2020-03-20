# Exchange Web Scraper

This is a simple web scraper that crawls the [PX Exchange](http://www.shopmyexchange.com), a shopping website for U.S. soldiers and veterans. 

## Motivation

The Exchange often holds bulk sales on multiple items without prior notice, making it difficult for people to purchase items at their cheapest price points. When people hear about ongoing sales and browse the website, they often realize to their dismay that the sale has already expired. 

## Functionality

As it stands, the program is able to scrape contents of the Exchange website given a specified keyword. It will return a summary of the items matching the keyword alongside its price, all on a single table. 

Known Bugs:
- The scraper fails when an item is sold out
- "Log in for Exchange pricing" hinders scraping

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

The `demo.py` script can be used to test run the application. To run, type

```bash
python -m demo
```

You will be asked to input a product. The program will print a table listing the first twelve product entries matching your search keyword along with their respective prices. 

## Example

Below is a sample demonstration of the application using the keyword `ipad pro`. 

```bash
Which product are you interested in? ipad pro
                                        names     prices
0    Apple iPad Pro 12.9 in. 512GB with WiFi   $1,339.00
1      Apple iPad Pro 12.9 in. 1TB with WiFi   $1,549.00
2       Apple iPad Pro 11 in. 64GB with WiFi     $739.00
3      Apple iPad Pro 11 in. 256GB with WiFi     $938.00
4        Apple iPad Pro 11 in. 1TB with WiFi   $1,349.00
5   Apple iPad Pro 12.9 in. 256GB with Wi-Fi   $1,139.00
6    Apple iPad Pro 12.9 in. 64GB with Wi-Fi     $989.00
7      Apple iPad Pro 11 in. 512GB with WiFi   $1,139.00
8    Apple iPad Air 10.5 in. 256GB with WiFi     $549.00
9            Apple iPad mini 256GB with WiFi     $499.00
10            Apple iPad mini 64GB with WiFi     $389.00
11    Apple iPad Air 10.5 in. 64GB with WiFi     $399.00
```

