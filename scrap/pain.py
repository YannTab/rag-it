import sys
import re
import requests
from urllib.parse import urljoin

from selectolax.parser import HTMLParser
from loguru import logger

"""
## Functions to implement : 
Get url of the next page 
With url of a book, compute its whole value
Get price with HTML
Get quantity with HTML
Get urls of all books of the library
Get url of a specific page

"""


logger.remove()
logger.add("books.log", rotation="500kb", level="WARNING")
logger.add(sys.stderr, level="INFO")

BASE_URL = "https://books.toscrape.com/"

def get_all_books_urls(url:str) -> list[str]:
    """
    Get URLs of the books on every page from an entry URL
    :param url: entry point URL
    :return: List of all URLs of books 
    """
    with requests.Session() as session:
        urls = []
        next_page_url = url
        while True:
            logger.info(f"browse {next_page_url}")
            try:
                response = session.get(next_page_url)
                response.raise_for_status()
            except requests.RequestException as e:
                logger.error(f"HTTP request error on page {next_page_url} : {e}")
                continue

            tree = HTMLParser(response.text)
            books_urls = get_all_books_urls_on_page(next_page_url, tree)
            urls.extend(books_urls)

            next_page_url = get_next_page_url(next_page_url, tree)
            if not next_page_url: 
                break
    return urls
        
def get_next_page_url(url: str, tree:HTMLParser) -> str | None:
    """
    Get URL of the next page given one page
    :param url: URL of the current page
    :param tree: HTMLParser object of the page
    :return: URL of the next page
    """
    next_page_node = tree.css_first("li.next > a")
    if next_page_node and "href" in next_page_node.attributes:
        rel_link = next_page_node.attributes["href"]
        return urljoin(url, rel_link)
    logger.info("No next button found in page")
    return None

def get_all_books_urls_on_page(url:str, tree: HTMLParser) -> list[str]:
    """
    Get URL of books on one page
    :param url: Base URL of page
    :param tree: HTMLParser object of the page
    :return: List of URLs of all books on the page
    """
    try :
        books_links_nodes = tree.css("h3 > a")
        urls = [urljoin(url, link.attributes["href"]) for link in books_links_nodes if "href" in link.attributes]
    except Exception as e:
        logger.error(f"An error happened while extracting URLs : {e}")
        urls = []
    return urls

def get_book_price(url:str, session:requests.Session = None) -> float:
    """
    Computes the book price of a page with given URL
    :param url: URL of the book page
    :return: Book price times quantity 
    """
    try:
        if session:
            response = session.get(url)
        else:
            response = requests.get(url)
        response.raise_for_status()
        tree = HTMLParser(response.text)
        price = extract_price_from_page(tree=tree)
        stock = extract_quantity_from_page(tree=tree)
        price_stock = price * stock
        logger.info(f"Scrappin {url}: {price_stock}")
        return price_stock
    except requests.exceptions.RequestException as e:
        logger.error(f"Error after HTTP request: {e}")
        return 0.0

def extract_price_from_page(tree: HTMLParser) -> float:
    """
    Extracts the price from the HTML code of the page
    :param tree: HTMLParser of the book's page
    :return: Unit price of a book
    """
    price_node = tree.css_first("p.price_color")

    if price_node:
        price_string = price_node.text()
    else:
        logger.error("No node with price found")
        return 0.0
    
    try:
        price = re.findall(r"[0-9.]+", price_string)[0]
    except IndexError as e:
        logger.error(f"No number found : {e}")
        return 0.0
    else:
        return float(price)

def extract_quantity_from_page(tree: HTMLParser) -> int:
    """
    Extracts the quantity from the HTML code of the page
    :param tree: HTMLParser of the book's page
    :return: Quantity of a book in stock
    """

    stock_node = tree.css_first("p.instock.availability")

    if stock_node:
        stock_string = stock_node.text()
    else:
        logger.error("No node with stock found")
        return 0.0
    
    try:
        stock = re.findall(f"\d+", stock_string)[0]
    except IndexError as e:
        logger.error(f"No number found : {e}")
        return 0.0
    else:
        return float(stock)

def main():
    base_url = "https://books.toscrape.com"
    all_books_urls   = get_all_books_urls(url=base_url)
    total_price = 0
    with requests.Session() as session:
        for book_url in all_books_urls:
            price = get_book_price(url=book_url, session=session)
            total_price += price
        print(total_price)
    return total_price

if __name__ == "__main__":
    main()

