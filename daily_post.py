import os
import time
import math
import random
import tweepy
from telegram.ext import Updater
from telegram import ParseMode

# ====== Load Environment Variables (from GitHub Secrets) ======
consumer_key = os.environ['T_consumer_key']
consumer_secret = os.environ['T_consumer_secret']
access_token = os.environ['T_access_token']
access_token_secret = os.environ['T_access_token_secret']
telegram_token = os.environ['T_Token']
telegram_chat_id = os.environ['T_chatid']


# ====== Telegram Notification Function ======
def send_telegram_message(message):
    updater = Updater(token=telegram_token, use_context=True)
    updater.bot.send_message(chat_id=telegram_chat_id, text=message)


# ====== Format Long Tweets into Threaded Messages ======
def format_tweet_message(raw_text):
    messages = []
    words = raw_text.split()
    max_length = 260  # Keep buffer for thread numbering (e.g., "(1/3)")
    current_msg = ''

    for index, word in enumerate(words, start=1):
        word = word.strip()
        if not word:
            continue

        # Check if appending exceeds limit
        if len(current_msg) + len(word) + 1 <= max_length:
            current_msg = f"{current_msg} {word}".strip()
        else:
            messages.append(current_msg)
            current_msg = word

        # Add last message
        if index == len(words):
            messages.append(current_msg)

    return messages


# ====== Post to Twitter (Main Logic) ======
def post_to_twitter():
    try:
        # Authenticate with Twitter API
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)

        # Read a random quote or message
        with open('yarl.txt', 'r', encoding='utf-8') as file:
            lines = file.read().splitlines()
            selected_text = random.choice(lines)

        messages = format_tweet_message(selected_text)
        is_thread = len(messages) > 1
        reply_to_id = None

        # Post each part of the thread
        for i, msg in enumerate(messages, start=1):
            if is_thread:
                msg += f" ({i}/{len(messages)})"

            tweet = api.update_status(status=msg, in_reply_to_status_id=reply_to_id)
            if is_thread and reply_to_id is None:
                reply_to_id = tweet.id

            # Exponential delay to maintain order in threads
            if is_thread and i < len(messages):
                time.sleep(math.pow(2, i - 1) * 0.01)

        send_telegram_message("✅ Twitter bot executed successfully!")

    except Exception as error:
        send_telegram_message(f"❌ Error occurred:\n{str(error)}")


# ====== Entry Point ======
if __name__ == '__main__':
    post_to_twitter()
