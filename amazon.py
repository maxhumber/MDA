from gazpacho import get, Soup
from rich import print
from selenium.webdriver import Firefox, FirefoxProfile
from selenium.webdriver.firefox.options import Options

options = Options()
options.headless = True
browser = Firefox(executable_path='/usr/local/bin/geckodriver', options=options)

url = "https://www.amazon.ca/dp/B07VGRJDFY/"
browser.get(url)
html = browser.page_source
soup = Soup(html)

product = soup.find('span', {'id': 'productTitle'}).text
price = float(soup.find('span', {'id': 'priceblock_ourprice'}).text.split('$ ')[-1])
