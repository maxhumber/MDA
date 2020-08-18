# https://slack.dev/python-slackclient/basic_usage.html
# https://github.com/slackapi/python-slackclient

import logging
import os
from dotenv import find_dotenv, load_dotenv # pip install python-dotenv
from slack import WebClient # pip install slackclient
from slack.errors import SlackApiError

logging.basicConfig(level=logging.DEBUG)
load_dotenv(find_dotenv())

slack_token = os.environ["SLACK_API_TOKEN"]
client = WebClient(token=slack_token)

try:
    response = client.chat_postMessage(
        channel="bots",
        text="okayokay!!!!!",
        username='switch_bot',
        icon_emoji=':robot_face:'
    )
except SlackApiError as e:
    # You will get a SlackApiError if "ok" is False
    assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
