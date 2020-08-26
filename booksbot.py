
import os
import sqlite3

from gazpacho import get, Soup
from dotenv import find_dotenv, load_dotenv # pip install python-dotenv
import pandas as pd
from slack import WebClient # pip install slackclient

load_dotenv(find_dotenv())

con = sqlite3.connect("data/books.db")
cur = con.cursor()

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
books['date'] = pd.Timestamp("now")

books.to_sql('books', con, if_exists='append', index=False)
average = pd.read_sql("select title, round(avg(price),2) as average from books group by title", con)
df = pd.merge(books[['title', 'price']], average)

string = f"Current Prices:```\n{df.to_markdown(index=False, tablefmt='grid')}\n```"

response = client.chat_postMessage(
    channel="books",
    text=string
)
