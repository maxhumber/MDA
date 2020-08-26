import json
import os
import sys
from urllib.request import Request, urlopen

import pandas as pd
from slack import WebClient

if sys.platform == 'darwin':
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv())

slack_token = os.environ["SLACK_API_TOKEN"]
client = WebClient(token=slack_token)

def post(url, data):
    data = bytes(json.dumps(data).encode("utf-8"))
    request = Request(url=url, data=data, method="POST")
    request.add_header("Content-type", "application/json; charset=UTF-8")
    with urlopen(request) as response:
        response = json.loads(response.read().decode("utf-8"))
    return response

url = "https://scrape.world/demand"

tomorrow = (pd.Timestamp('today') + pd.Timedelta('1 day')).strftime("%Y-%m-%d %H:00")
temperature = 21
data = {"date": tomorrow, "temperature": temperature}
response = post(url, data)

text = f"{tomorrow=} demand will be ~{response['demand']} MW"

client.chat_postMessage(channel="energy",text=text)
