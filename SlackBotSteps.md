# SlackBot

### Installing slackclient

The name of the package we'll use is called `slackclient`, and it can be installed using [pip](https://howchoo.com/g/mze4ntbknjk/install-pip-python). To install locally you can run:

```python
pip install slackclient
```

### Generate a Slack API token 

To generate a Slack API token, you'll need to run do the following:

1. Create a new Slack App
2. Add permissions
3. Copy the token URL

### Create a new Slack App

To start, you'll need to create a [Slack App](https://api.slack.com/apps). Follow the link, and click **Create New App**. The process is fairly self-explanatory.

### Add permissions

In the menu on the left, find **OAuth and Permissions**. Click it, and scroll down to the **Scopes** section. Click **Add an OAuth Scope**.

Search for the **chat:write** and **chat:write.public** scopes, and add them. At this point, you'll need to re-install the app in your workspace for the permissions to take effect.

### Copy the token URL

On the same page you'll find your access token under the label **Bot User OAuth Access Token**. Copy this token, and save it for later.

### Send a message

At this point, we have everything we need to send a message. Below is a simple example to get you started:

```python
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
        text="It works",
        username='Bot2',
        icon_emoji=':robot:'
    )
except SlackApiError as e:
    # You will get a SlackApiError if "ok" is False
    assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
```