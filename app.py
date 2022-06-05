#!/usr/bin/env python3

import tweepy
import argparse
import os
import logging
from time import sleep


logging.basicConfig(level=logging.INFO)


def get_access_token():
    try:
        return {
            "consumer_key": os.environ["TWITTER_API_KEY"],
            "consumer_secret": os.environ["TWITTER_API_SECRET_KEY"],
            "access_token": os.environ["TWITTER_API_ACCESS_TOKEN"],
            "access_token_secret": os.environ["TWITTER_API_ACCESS_TOKEN_SECRET"],
            "bearer_token": os.environ["TWITTER_BEARER_TOKEN"],
        }
    except Exception:
        logging.error("Failed to get env variable TWITTER_BEARER_TOKEN")
        exit(1)


def create_cli():
    parser = argparse.ArgumentParser()


if __name__ == "__main__":
    # credentials
    credentials = get_access_token()

    # parser
    parser = argparse.ArgumentParser()
    parser.add_argument("username", nargs=1, help="twitter username")
    parser.add_argument("-n", "--name", help="list name")
    parser.add_argument("-d", "--description", help="List description")
    args = parser.parse_args()
    username = args.username[0]

    # Twitter client and api
    client = tweepy.Client(
        bearer_token=credentials["bearer_token"], wait_on_rate_limit=True
    )
    auth = tweepy.OAuthHandler(
        credentials["consumer_key"], credentials["consumer_secret"]
    )
    auth.set_access_token(
        credentials["access_token"], credentials["access_token_secret"]
    )
    api = tweepy.API(auth, wait_on_rate_limit=True)

    # Fetch twitter user
    user = client.get_user(username=username, user_auth=False)
    if user.errors:
        logging.error(f"Failed to find username {username}")
        exit(2)
    user_id = user.data["id"]
    logging.info(f"Username: {username}, id: {user_id}")

    # get user followings
    following_ids = api.get_friend_ids(screen_name=username)

    # create list
    lst = client.create_list(
        name=args.name or username,
        private=True,
        description=args.description or "",
        user_auth=False,
    )
    if lst.errors:
        logging.error("Failed to create list")
    lst_id = lst.data["id"]

    # fill list with members
    if len(following_ids) < 300:
        count = 0
        failed = 0

        logging.info(f"Adding {len(following_ids)} members ...")
        for following_id in following_ids:
            try:
                member = client.add_list_member(
                    lst_id, user_id=following_id, user_auth=False
                )
                if member.errors:
                    logging.error(f"Failed to add member {following_id}")
                else:
                    count += 1
            except tweepy.errors.Forbidden:
                logging.warn(f"Failed to add member {following_id}, forbidden")
                failed += 1
                continue
            except tweepy.errors.TooManyRequests:
                logging.warn("Waiting for 10s before doing another api call")
                sleep(10)

        logging.info(f"Added {count} / {len(following_ids)} members")
        logging.warn(f"Failed to add {failed} / {len(following_ids)} members")
        logging.info(f"Twitter list: https://twitter.com/i/lists/{lst_id}")
    else:
        logging.warn(
            "300 Request allowed in 15 min, and user has more thant 300 following"
        )
