import re

import requests
from bs4 import BeautifulSoup

def get_all_articles(threshold:int = 5):
    with requests.Session() as session:
        url = "https://books.toscrape.com/"
        response  = session.get(url)

        # Parse the html output of the request
        soup = BeautifulSoup(response.text, "html.parser")

        # Get links of all categories
        category_links = [(category.text.strip(), category.get("href")) for category in soup.find("div", class_="side_categories").find_all("a")]
        for cat in category_links:
            new_url = url + cat[-1] # Base + href
            response = session.get(new_url)
            sub_soup = BeautifulSoup(response.text, "html.parser")
            articles = sub_soup.find("section").find_all("article", class_="product_pod")
            n_articles = len(articles)
            if n_articles <= threshold:
                print(cat[0])

with requests.Session() as session:
    url = "https://books.toscrape.com/"
    try:
        response = session.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Error")
        raise requests.exceptions.RequestException from e

    soup = BeautifulSoup(response.text, "html.parser")

    products = [product for product in soup.find_all("article", class_="product_pod")]
    for product in products:
        try :
            stars = product.find("p").get("class")[-1]
            product_desc = product.find("h3").find("a")
            name = product_desc.get("title")
            index = product_desc.get("href").split("/")[1].split("_")[-1]
        except Exception as e:
            raise Exception from e
        if stars == "One":
            print(name, index)

