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
from configparser import ConfigParser


#getting the Key from outside

consumer_key = os.environ['T_consumer_key']
consumer_secret = os.environ['T_consumer_secret']
access_token = os.environ['T_access_token']
access_token_secret = os.environ['T_access_token_secret']
Token = os.environ['T_Token']
Chat_id = os.environ['T_chatid']

def telmsg(fmsg):
    updater = Updater(token=Token, use_context=True)
    updater.bot.send_message(chat_id=Chat_id, text=fmsg)
    

def post_master(i):
    try:
        # authentication of consumer key and secret
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        # authentication of access token and secret
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        # get the random line
        parser = ConfigParser()
        parser.read('simple.ini')
        i = parser.get('line_details', 'last')
        i = int(i)
        i=i+1
        opn_f = open('Periyar.txt','r', encoding='UTF-8')
        sel_line = opn_f.read().splitlines()
        post_status = sel_line[i]
        opn_f.close()
        telmsg(post_status)
        # update the status  
        # api.update_status(status=post_status)
        parser.set('line_details', 'last', str(i))
        configfile = open('simple.ini', 'w')
        parser.write(configfile)
        configfile.close()
    except Exception as errmsg:
        telmsg(str(errmsg))
    finally:
        messag = 'Quote number '+ str(i)+ ' is executed successfully!!'
        telmsg(messag)


def main():
    global i
    i=1
    post_master(i)
    while True:
        _currentTime = time.localtime()
        c_time = time.strftime("%H:%M:%S", _currentTime)
        if (c_time == '00:30:00') or (c_time == '07:30:00') or (c_time == '12:30:00') or (c_time == '16:30:00'):
            post_master(i)
        time.sleep(1)


if __name__ == '__main__':
    main()






