import os

from gazpacho import get, Soup
from dotenv import find_dotenv, load_dotenv # pip install python-dotenv
import pandas as pd

load_dotenv(find_dotenv())

slack_token = os.environ["SLACK_API_TOKEN"]
client = WebClient(token=slack_token)

def parse(book):
    name = book.find("h4").text
    price = float(book.find("p").text[1:].split(" ")[0])
    return name, price

def fetch_books():
    url = "https://scrape.world/books"
    html = get(url)
    soup = Soup(html)
    books = soup.find("div", {"class": "book-"})
    return [parse(book) for book in books]

data = fetch_books()
books = pd.DataFrame(data, columns=["title", "price"])
