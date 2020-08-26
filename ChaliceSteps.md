[Documentation](https://github.com/aws/chalice)

---

### Pricing

[The AWS Lambda free usage tier includes **1M free requests per month and 400,000 GB-seconds of compute time per month.**](https://aws.amazon.com/lambda/pricing/)



### Install

Chalice supports all versions of python supported by AWS Lambda, which includes python2.7, python3.6, python3.7, python3.8.

To install Chalice, we'll first create and activate a virtual environment:

```
python -m venv venv
source venv/bin/activate
```

Next we'll install Chalice using `pip`:

```
pip install chalice
```

### Credentials

Before you can deploy an application, be sure you have credentials configured.  If you have previously configured your machine to run boto3 (the AWS SDK for Python) or the AWS CLI then you can skip this section.

If this is your first time configuring credentials for AWS you can follow these steps to quickly get started:

```
mkdir ~/.aws
cat >> ~/.aws/config
[default]
aws_access_key_id=YOUR_ACCESS_KEY_HERE
aws_secret_access_key=YOUR_SECRET_ACCESS_KEY
region=YOUR_REGION (such as ca-central-1, us-east-1, us-west-1, etc)
```

You can generate a new key [here](https://console.aws.amazon.com/iam/home?#/security_credentials)

### Creating Your Project

The next thing we'll do is use the `chalice` command to create a new project:

```
chalice new-project helloworld
```

This will create a `helloworld` directory.  Cd into this directory.  You'll see several files have been created for you:

```
$ cd helloworld
$ ls -la
drwxr-xr-x   .chalice
-rw-r--r--   app.py
-rw-r--r--   requirements.txt
```

You can ignore the `.chalice` directory for now, the two main files we'll focus on is `app.py` and `requirements.txt`.

Let's take a look at the `app.py` file:

```python
from chalice import Chalice

app = Chalice(app_name='helloworld')

@app.route('/')
def index():
    return {'hello': 'world'}
```

The `new-project` command created a sample app that defines a single view, `/`, that when called will return the JSON body `{"hello": "world"}`.



### Deploying

Let's deploy this app.  Make sure you're in the `helloworld` directory and run `chalice deploy`:

```
$ chalice deploy
Creating deployment package.
Creating IAM role: helloworld-dev
Creating lambda function: helloworld-dev
Creating Rest API
Resources deployed:
  - Lambda ARN: arn:aws:lambda:us-west-2:12345:function:helloworld-dev
  - Rest API URL: https://abcd.execute-api.us-west-2.amazonaws.com/api/
```

You now have an API up and running using API Gateway and Lambda:

```
$ curl https://xses91w2u1.execute-api.ca-central-1.amazonaws.com/api/
{"hello": "world"}
```

Try making a change to the returned dictionary from the `index()` function.  You can then redeploy your changes by running `chalice deploy`.

### Clean up

If you're done experimenting with Chalice and you'd like to cleanup, you can use the `chalice delete` command, and Chalice will delete all the resources it created when running the `chalice deploy` command.

```
$ chalice delete
Deleting Rest API: abcd4kwyl4
Deleting function aws:arn:lambda:region:123456789:helloworld-dev
Deleting IAM Role helloworld-dev
```

###

### Adding Environment Variables

[Source](https://aws.github.io/chalice/topics/configfile.html?highlight=environment#id1)

Adding environment variables to `.chalice/config.json`:

In the following example, environment variables are specified both as top level keys as well as per stage.  This allows us to provide environment variables that all stages should have as well as stage specific environment variables:

```json
{
  "version": "2.0",
  "app_name": "app",
  "environment_variables": {
    "SHARED_CONFIG": "foo",
    "OTHER_CONFIG": "from-top"
  },
  "stages": {
    "dev": {
      "environment_variables": {
        "TABLE_NAME": "dev-table",
        "OTHER_CONFIG": "dev-value"
      }
    },
    "prod": {
      "environment_variables": {
        "TABLE_NAME": "prod-table",
        "OTHER_CONFIG": "prod-value"
      }
    }
  }
}
```



### Adding Rate Schedule

[Source](https://aws.github.io/chalice/api.html?highlight=rate#Rate)

An instance of this class can be used as the `expression` value in the [`Chalice.schedule()`](https://aws.github.io/chalice/api.html?highlight=rate#Chalice.schedule) method:

```
@app.schedule(Rate(5, unit=Rate.MINUTES))
def handler(event):
    pass
```

Examples:

```
# Run every minute.
Rate(1, unit=Rate.MINUTES)

# Run every 2 hours.
Rate(2, unit=Rate.HOURS)
```

`unit`[¶](https://aws.github.io/chalice/api.html?highlight=rate#Rate.unit)

The unit of the provided `value` attribute.  This can be either `Rate.MINUTES`, `Rate.HOURS`, or `Rate.DAYS`.



### Running Now

```python
from chalice import Chalice, Rate
from gazpacho import get, Soup

app = Chalice(app_name='scraper')

@app.route('/')
def index():
    return {'hello': 'world'}

# Automatically runs every 5 minutes
@app.schedule(Rate(5, unit=Rate.MINUTES))
def periodic_task(event):
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
```



### Looking at logs

In the following application, we’re using the application logger to emit two log messages, one at `DEBUG` and one at the `ERROR` level:

```
from chalice import Chalice

app = Chalice(app_name='demolog')


@app.route('/')
def index():
    app.log.debug("This is a debug statement")
    app.log.error("This is an error statement")
    return {'hello': 'world'}
```

If we make a request to this endpoint, and then look at `chalice logs` we’ll see the following log message:

```
2016-11-06 20:24:25.490000 9d2a92 demolog - ERROR - This is an error statement
```

As you can see, only the `ERROR` level log is emitted because the default log level is `ERROR`.  Also note the log message formatting. This is the default format that’s been automatically configured. We can make a change to set our log level to debug:

### Run locally

`chalice local`
