
from gazpacho import get, Soup
import pandas as pd

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

string = f"Current Prices:\n```\n{books.to_markdown(index=False, tablefmt='grid')}\n```"

print(string)
