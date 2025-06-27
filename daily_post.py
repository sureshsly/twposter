import os
import time
import math
import random
import tweepy
from telegram.ext import Updater

# ========== Load Environment Variables ==========
TWITTER_CONSUMER_KEY = os.environ['T_consumer_key']
TWITTER_CONSUMER_SECRET = os.environ['T_consumer_secret']
TWITTER_ACCESS_TOKEN = os.environ['T_access_token']
TWITTER_ACCESS_SECRET = os.environ['T_access_token_secret']
TELEGRAM_TOKEN = os.environ['T_Token']
TELEGRAM_CHAT_ID = os.environ['T_chatid']


# ========== Telegram Notification ==========
def send_telegram_message(message):
    try:
        updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
        updater.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    except Exception as e:
        print(f"Failed to send Telegram message: {e}")


# ========== Format Long Messages into Tweet Threads ==========
def format_tweet_message(raw_text):
    messages = []
    words = raw_text.split()
    max_length = 260  # Keep buffer for "(1/2)" style thread numbering
    current_msg = ''

    for i, word in enumerate(words, start=1):
        word = word.strip()
        if not word:
            continue

        if len(current_msg) + len(word) + 1 <= max_length:
            current_msg = f"{current_msg} {word}".strip()
        else:
            messages.append(current_msg)
            current_msg = word

        if i == len(words):
            messages.append(current_msg)

    return messages


# ========== Initialize Tweepy Client for API v2 ==========
def get_twitter_client():
    return tweepy.Client(
        consumer_key=TWITTER_CONSUMER_KEY,
        consumer_secret=TWITTER_CONSUMER_SECRET,
        access_token=TWITTER_ACCESS_TOKEN,
        access_token_secret=TWITTER_ACCESS_SECRET
    )


# ========== Post to Twitter ==========
def post_to_twitter():
    try:
        client = get_twitter_client()

        # Read a random tweet from file
        with open('yarl.txt', 'r', encoding='utf-8') as file:
            lines = file.read().splitlines()
            selected_text = random.choice(lines)

        messages = format_tweet_message(selected_text)
        is_thread = len(messages) > 1
        reply_to_id = None

        for i, msg in enumerate(messages, start=1):
            if is_thread:
                msg += f" ({i}/{len(messages)})"

            tweet = client.create_tweet(
                text=msg,
                in_reply_to_tweet_id=reply_to_id
            )
            reply_to_id = tweet.data['id'] if is_thread else None

            # Delay to help preserve thread order
            if is_thread and i < len(messages):
                time.sleep(math.pow(2, i - 1) * 0.01)

        send_telegram_message("✅ Tweet posted successfully!")

    except Exception as e:
        send_telegram_message(f"❌ Error occurred:\n{str(e)}")


# ========== Entry Point ==========
if __name__ == '__main__':
    post_to_twitter()
