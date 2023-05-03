import tweepy
import json
import random
import time
import logging

# Load settings from the config file
with open('settings.json', 'r') as f:
    settings = json.load(f)

# Configure logging
logging.basicConfig(
    filename=settings['log_file'],
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Authenticate with Twitter API using Tweepy
auth = tweepy.OAuth1UserHandler(
    settings['consumer_key'],
    settings['consumer_secret'],
    settings['access_token'],
    settings['access_token_secret']
)
api = tweepy.API(auth)

# Get the latest status from the user's timeline
latest_status = api.user_timeline(id=settings['twitter_username'], count=1)[0]

# Iterate through the statuses
for status in tweepy.Cursor(api.user_timeline, id=settings['twitter_username']).items():
    try:
        # Like and retweet the status
        api.create_favorite(status.id)
        api.retweet(status.id)

        # Comment on the status with a random choice from the list of comment wordings
        comment_wording = random.choice(settings['comment_wordings'])
        comment_tweet = comment_wording.format(status.author.screen_name)
        api.update_status(comment_tweet, in_reply_to_status_id=status.id, auto_populate_reply_metadata=True)

        # Quote tweet the status with a random choice from the list of quote wordings
        quote_wording = random.choice(settings['quote_wordings'])
        quote_tweet = quote_wording.format(status.author.screen_name, status.text)
        api.update_status(quote_tweet, in_reply_to_status_id=status.id, auto_populate_reply_metadata=True)

        # Log success message
        logging.info(f'Successfully interacted with status: {status.id}')

    except Exception as e:
        # Log error message
        logging.error(f'Error interacting with status {status.id}: {e}')

    # Wait for the specified interval time before moving to the next status
    time.sleep(settings['interval_time'])
