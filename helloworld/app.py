from chalice import Chalice, Rate
from gazpacho import get, Soup

app = Chalice(app_name='scraper')

@app.route('/')
def index():
    return {'hello': 'world'}

# Automatically runs every 1 minutes
@app.schedule(Rate(1, unit=Rate.MINUTES))
def periodic_task(event):
    print("Run 1 minute")
    app.log.debug("This is a debug statement")
    return {"hello": "world"}


@app.route('/scrape')
def scrape():
    url = "https://scrape.world/soup"
    html = get(url)
    soup = Soup(html)
    fos = soup.find("div", {"class": "section-speech"})
    links = []
    for a in fos.find("a"):
        try:
            link = a.attrs["href"]
            links.append(link)
        except AttributeError:
            pass
    links = [l for l in links if "wikipedia.org" in l]
    return {'links': links}
