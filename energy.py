import json
from urllib.request import Request, urlopen
import pandas as pd
from slack import WebClient
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

SLACK_API_TOKEN = os.environ.get("SLACK_API_TOKEN")
client = WebClient(token=SLACK_API_TOKEN)
url = "https://scrape.world/demand"

def post(url, data):
    data = bytes(json.dumps(data).encode("utf-8"))
    request = Request(url=url, data=data, method="POST")
    request.add_header("Content-type", "application/json; charset=UTF-8")
    with urlopen(request) as response:
        response = json.loads(response.read().decode("utf-8"))
    return response

tomorrow = pd.Timestamp("now") + pd.Timedelta('1 day')
tomorrow = tomorrow.strftime("%Y-%m-%d %H:00")

response = post(url, {"date": tomorrow, "temperature": 21})
text = f"{tomorrow=} demand will be ~{response.get('demand')} MW"

client.chat_postMessage(channel="energy", text=text)
