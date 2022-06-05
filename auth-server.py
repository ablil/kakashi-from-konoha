#!/usr/bin/env python3

import os
import tweepy
from flask import Flask, redirect, request

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

app = Flask(__name__)

oauth2_user_handler = tweepy.OAuth2UserHandler(
    client_id=os.environ["TWITTER_CLIENT_ID"],
    redirect_uri="http://localhost:5000/authorized",
    scope=["tweet.read", "users.read", "follows.read", "list.read", "list.write"],
    client_secret=os.environ["TWITTER_CLIENT_SECRET"],
)


@app.route("/")
def index():
    return "Visit <b>/login</b> to authenticate and get access token"


@app.route("/login")
def login():
    return redirect(oauth2_user_handler.get_authorization_url())


@app.route("/authorized")
def authorized():
    return oauth2_user_handler.fetch_token(request.url)
