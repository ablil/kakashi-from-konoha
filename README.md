# Kakashi - Clone twitter user profile

Create a private twitter list filled with all following of a twitter user and enjoy spying on his timeline :eyes:

## Get Started

## Pre-requisties

1. Create twitter app [here](https://developer.twitter.com)
2. set redirect url to: http://localhost:5000/authorized
3. Enable oauth2
4. Set the following env variale from your twitter app
```
    export TWITTER_API_KEY=<api key>
    export TWITTER_API_SECRET_KEY=<api secret>
    export TWITTER_API_ACCESS_TOKEN=<access token>
    export TWITTER_API_ACCESS_TOKEN_SECRET=<access token secret>
    export TWITTER_CLIENT_ID=<client id>
    export TWITTER_CLIENT_SECRET=<client secret>
```
5. Install requirements: `pip3 install -r requirements.txt`

## Usage

1. Get access token
2. Run auth server `export FLASK_APP=auth-server; flask run`
3. Visit http://localhost:5000/login and get access token
4. Set access token as env variable `export TWITTER_BEARER_TOKEN=<access token>`
5. Run `python3 app.py -n <listname> <username>`
