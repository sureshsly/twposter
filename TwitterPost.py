# importing the module
from sys import version_info
import requests
import json
import operator
from telegram.ext import Updater, Filters, MessageHandler
from telegram import ParseMode
import tweepy
import random
import time
import os

#getting the Key from outside

consumer_key = os.environ['T_consumer_key']
consumer_secret = os.environ['T_consumer_secret']
access_token = os.environ['T_access_token']
access_token_secret = os.environ['T_access_token_secret']
Token = os.environ['T_Token']


def random_line():

    lines = open('quote.txt', encoding='UTF-8').read().splitlines()
    selected_line = random.choice(lines)

    return selected_line


def post_master():
    try:
        # authentication of consumer key and secret
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        # authentication of access token and secret
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        # get the random line
        post_status = random_line()
        # update the status
        api.update_status(status=post_status)
        proc_stat = 'Msg posted'+ ' '+post_status

    except Exception as errmsg:
        proc_stat = errmsg
    finally:
        pass
    return proc_stat


def main():
    updater = Updater(token=Token, use_context=True)
    while True:
        _currentTime = time.localtime()
        c_time = time.strftime("%S", _currentTime)
        if (c_time == '00') or (c_time == '13:20:00') or (c_time == '13:40:00'):
            msg = post_master()
            updater.bot.send_message(chat_id='890299126', text=msg)
        time.sleep(600)


if __name__ == '__main__':
    main()






