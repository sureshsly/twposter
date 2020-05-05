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

def telmsg(fmsg):
    updater = Updater(token=Token, use_context=True)
    updater.bot.send_message(chat_id='890299126', text=fmsg)
    

def post_master():
    try:
        # authentication of consumer key and secret
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        # authentication of access token and secret
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        # get the random line
        lines = open('quote.txt', encoding='UTF-8').read().splitlines()
        post_status = random.choice(lines)
        # update the status  
        api.update_status(status=post_status)
    except Exception as errmsg:
        telmsg(str(errmsg))
    finally:
        telmsg('Executed')


def main():

    while True:
        _currentTime = time.localtime()
        c_time = time.strftime("%H:%M:%S", _currentTime)
        if (c_time == '12:45:00') or (c_time == '11:45:00') or (c_time == '13:55:00'):
            post_master()
        time.sleep(1)


if __name__ == '__main__':
    main()






