#!/usr/bin/env python3

import tweepy
import argparse
import os
import logging
from time import sleep


logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")


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

def initialize():
    if not os.path.exists(os.path.join(os.path.expanduser('~'), '.kakashi/followings')):
        os.makedirs(os.path.join(os.path.expanduser('~'), '.kakashi/followings'))

    if not os.path.exists(os.path.join(os.path.expanduser('~'), '.kakashi/lists')):
        os.makedirs(os.path.join(os.path.expanduser('~'), '.kakashi/lists'))

def create_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("username", nargs=1, help="twitter username")
    parser.add_argument("-n", "--name", help="list name")
    parser.add_argument('-l', '--list', help='list id (use this to updated an existing list)', type=int)
    parser.add_argument("-d", "--description", help="List description")
    return parser

class Kakashi:
    def __init__(self, credentials):
        self.client = tweepy.Client(
            bearer_token=credentials["bearer_token"], wait_on_rate_limit=True
        )
        self.auth = tweepy.OAuthHandler(
            credentials["consumer_key"], credentials["consumer_secret"]
        )
        self.auth.set_access_token(
            credentials["access_token"], credentials["access_token_secret"]
        )
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True)
        self.cachepath = os.path.join(os.path.expanduser('~'), '.kakashi')

    def spy_on_user(self, username, listname, description, create=True):
        list_id = self.create_lst(listname or username, description)
        following_ids = self.fetch_user_following(username)

        count = 0
        failed = 0

        logging.info(f"Adding {len(following_ids)} members ...")
        for following_id in following_ids:
            sleep(1)
            try:
                member = self.add_member(following_id, list_id)
                if member.errors:
                    logging.error(f"Failed to add member {following_id}")
                else:
                    count += 1
            except tweepy.errors.Forbidden:
                logging.warn(f"Failed to add member {following_id}, forbidden")
                failed += 1
                continue

        logging.info(f"Added {count} / {len(following_ids)} members")
        logging.warn(f"Failed to add {failed} / {len(following_ids)} members")
        logging.info(f"Twitter list: https://twitter.com/i/lists/{lst_id or None}")
        

    def fetch_userid(self, username):
        user = self.client.get_user(username=username, user_auth=False)
        if user.errors:
            logging.error(f"Failed to find username {username}")
            exit(2)
        user_id = user.data["id"]
        logging.info(f"Username: {username}, id: {user_id}")

        return user_id

    def fetch_user_following(self, username):
        cachepath = os.path.join(self.cachepath, 'followings', username)

        # load from cache
        if os.path.exists(cachepath):
            with open(cachepath, 'r') as c:
                data = [int(userid) for userid in c.readlines()]
                logging.info("Loaded user following from cache")
                return data

        following_ids = self.api.get_friend_ids(screen_name=username)

        # save to cache
        with open(cachepath, 'w+') as c:
            c.write('\n'.join([str(userid) for userid in following_ids]))

        return following_ids

    def create_lst(self, name, description):
        cachepath = os.path.join(self.cachepath, 'lists', username)

        # load from cache
        if os.path.exists(cachepath):
            with open(cachepath, 'r') as c:
                data = [int(listid) for listid in c.readlines()]
                if len(data) > 0:
                    logging.info("Loaded list from cache")
                    return data[0]
        
        lst = self.client.create_list(
            name=args.name,
            private=True,
            description=args.description or "",
            user_auth=False,
        )
        if lst.errors:
            logging.error("Failed to create list")
            exit(2)
        lst_id = lst.data["id"]
        logging.info(f"Created list, name={name}, id={lst_id}")

        # save to cache
        with open(cachepath, 'w+') as c:
            c.write(lst_id)

        return lst_id

    def add_member(self, user_id, lst_id):
        member = self.client.add_list_member(
            lst_id, user_id=user_id, user_auth=False
        )

        print(user_id)
        return member

if __name__ == "__main__":
    initialize()

    # credentials
    credentials = get_access_token()

    # parser
    parser = create_cli()
    args = parser.parse_args()
    username = args.username[0]
    listid = args.list

    # Twitter client and api
    kakashi = Kakashi(credentials)
    kakashi.spy_on_user(username, username, '', create=True)
