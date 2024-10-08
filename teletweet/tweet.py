#!/usr/local/bin/python3
# coding: utf-8

# TeleTweet - tweet.py
# 10/22/20 16:18

__author__ = "jp0id <jp@8void.com>"

import logging
import re
import time
import traceback
from typing import Union

import tweepy

from config import CONSUMER_KEY, CONSUMER_SECRET
from helper import get_auth_data

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(filename)s [%(levelname)s]: %(message)s")


def __connect_twitter(chat_id: int):
    auth_data = get_auth_data(chat_id)
    logging.info("Connecting to twitter api...")
    client = tweepy.Client(
        consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET,
        access_token=auth_data["ACCESS_KEY"],
        access_token_secret=auth_data["ACCESS_SECRET"],
    )
    api = tweepy.API(
        tweepy.OAuth1UserHandler(
            consumer_key=CONSUMER_KEY,
            consumer_secret=CONSUMER_SECRET,
            access_token=auth_data["ACCESS_KEY"],
            access_token_secret=auth_data["ACCESS_SECRET"],
        )
    )
    return client, api


def upload_media(api, pic) -> Union[list, None]:
    if pic is None:
        return None
    ids = []
    for item in pic:
        item.seek(0)
        mid = api.media_upload(item.name, file=item)
        ids.append(mid)
    return [i.media_id for i in ids]


def send_tweet(message, pics: Union[list, None] = None) -> dict:
    twitter_character_limit = 137
    logging.info("Preparing tweet for...")
    chat_id = message.chat.id
    text = message.text or message.caption
    text_tmp = text
    tweet_id = __get_tweet_id_from_reply(message)
    client, api = __connect_twitter(chat_id)

    if not text:
        text = ""
        text_tmp = ""

    logging.info("Tweeting...")
    ids = upload_media(api, pics)
    response = dict()
    response_tmp = dict()
    i = 0

    if text == "":
        status = client.create_tweet(text=text, media_ids=ids, in_reply_to_tweet_id=tweet_id)
        response.update(status.data)
        return response

    while len(text) > 0:
        try:
            if len(text) <= twitter_character_limit:
                status = client.create_tweet(text=text, media_ids=ids, in_reply_to_tweet_id=tweet_id)
                text = ""
                response.update(status.data)
            else:
                split_point = text.rfind('。', 0, twitter_character_limit)
                if split_point == -1:
                    split_point = text.rfind('.', 0, twitter_character_limit)
                    if split_point == -1:
                        split_point = twitter_character_limit
                status = client.create_tweet(text=text[:split_point + 1], media_ids=ids, in_reply_to_tweet_id=tweet_id)
                i += 1
                if i == 1:
                    response_tmp.update(status.data)
                text = text[split_point + 1:].lstrip()
                ids = None
                time.sleep(1)
            logging.info("Tweeted")
            tweet_id = status.data['id']
        except Exception as e:
            logging.error(traceback.format_exc())
            response.update({"error": str(e)})
            break
    if len(text_tmp) <= twitter_character_limit:
        return response
    else:
        return response_tmp


def get_me(chat_id) -> str:
    logging.info("Get me!")
    try:
        client, api = __connect_twitter(chat_id)
        me = client.get_me().data
        name = me["name"]
        user_id = me["username"]
        response = f"[{name}](https://x.com/{user_id})"
    except Exception as e:
        logging.error(traceback.format_exc())
        response = {"error": str(e)}

    return response


def delete_tweet(message) -> dict:
    logging.info("Deleting tweet for someone...")
    chat_id = message.chat.id
    tweet_id = __get_tweet_id_from_reply(message)
    if not tweet_id:
        return {"error": "Which tweet do you want to delete? This does not seem like a valid tweet message."}

    try:
        client, api = __connect_twitter(chat_id)
        logging.info("Deleting......")
        response = client.delete_tweet(tweet_id).data
    except Exception as e:
        logging.error(traceback.format_exc())
        response = {"error": str(e)}

    return response


def __get_tweet_id_from_reply(message) -> int:
    reply_to = message.reply_to_message
    if reply_to:
        tweet_id = __get_tweet_id_from_url(reply_to.entities[0].url or "")
    else:
        tweet_id = None
    logging.info("Replying to %s", tweet_id)
    return tweet_id


def __get_tweet_id_from_url(url) -> int:
    try:
        # https://x.com/williamwoo7/status/1326147700425809921?s=20
        tweet_id = re.findall(r"https?://x\.com/.+/status/(\d+)", url)[0]
    except IndexError:
        tweet_id = None
    return tweet_id


def get_video_download_link(chat_id, tweet_id):
    client, api = __connect_twitter(chat_id)
    logging.info("Getting video tweets......")
    status = client.get_tweet(tweet_id).data
    return __get_video_url(status.AsDict())


def is_video_tweet(chat_id, text) -> str:
    # will return an id
    tweet_id = __get_tweet_id_from_url(text)
    logging.info("tweet id is %s", tweet_id)
    client, api = __connect_twitter(chat_id)
    logging.info("Getting video tweets......")
    try:
        # TODO I don't have permission to this. Thank you Elon Musk.
        status = client.get_tweet(tweet_id)
        if __get_video_url(status.data):
            return str(tweet_id)
    except Exception as e:
        logging.debug(traceback.format_exc())


def __get_video_url(json_dict: dict) -> str:
    logging.info("Downloading video...")
    # video/gif is the first one. photo could be four
    media = json_dict.get("media")
    if media:
        media = media[0]
        if media["type"] == "video":
            variants = media["video_info"]["variants"]
            rates = [i.get("bitrate", 0) for i in variants]
            index = rates.index(max(rates))
            url = variants[index]["url"]
            logging.info("Real download url found.")
            return url


if __name__ == "__main__":
    print(__get_tweet_id_from_url("https://x.com/williamwoo7/status/1326147700425809921?s=20"))
    print(__get_tweet_id_from_url("http://x.com/nixcraft/status/1326077772117078018?s=09"))
