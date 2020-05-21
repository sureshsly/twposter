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
import os, math



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
    

def post_master():
    try:
        # authentication of consumer key and secret
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        # authentication of access token and secret
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        # get the random line
        opn_f = open('yarl.txt','r', encoding='UTF-8')
        sel_line = opn_f.read().splitlines()
        post_status =random.choice(sel_line)
        opn_f.close()
        messages = format_msg(post_status)
        is_thread = (len(messages) > 1)
        reply_id = 0
        for index, msg in enumerate(messages, start=1):
            if(is_thread):
                msg += ' ('+str(index)+'/'+ str(len(messages)) + ')'
            #print(msg)
            status = api.update_status(status=msg, in_reply_to_status_id = reply_id)
            if(is_thread and reply_id == 0 and hasattr(status, 'id')):
                reply_id = status.id
            if(is_thread and index != len(messages)):
                #I've tried add delay so replies are order in thread but somehow order is messed in bigger threads
                delay = math.pow(2, index - 1) * .01 #exponential delay 0.1, 0.2, 0.4, 0.8, 1.6, 3.2
                time.sleep(delay)

    except Exception as errmsg:
        telmsg(str(errmsg))
    finally:
        messag = 'Quote is executed successfully!!'
        telmsg(messag)
        
def format_msg(msg):
    message = []
    splited = msg.split(' ')
    length = 260 #max 280 and 20 buffer to add string like (1/2)
    str = ''
    for index, string in enumerate(splited, start=1):
        striped = string.strip()
        if len(striped) == 0:
            continue
        if(len(striped) + len(str) <= length ):
            if str == '':
                str = striped
            else:
                str += ' ' + striped
            if(len(str) > 0 and index == len(splited)):
                message.append(str)    
        else:
            message.append(str)
            str = striped
    return message

def main():
    post_master()
    while True:
        _currentTime = time.localtime()
        c_time = time.strftime("%H:%M:%S", _currentTime)
        if (c_time == '00:30:00') or (c_time == '07:30:00') or (c_time == '12:30:00') or (c_time == '16:30:00'):
            post_master()
        time.sleep(1)


if __name__ == '__main__':
    main()
