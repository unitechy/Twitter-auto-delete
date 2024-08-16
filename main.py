import tweepy
import datetime
from dateutil import parser
import time
import logging
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set your Twitter API credentials
consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

# Authenticate with Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

def delete_old_tweets(days=7, max_tweets=3200):
    # Calculate the date 'days' ago
    cutoff_date = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=days)
    
    deleted_count = 0
    
    try:
        for tweet in tweepy.Cursor(api.user_timeline).items(max_tweets):
            if tweet.created_at < cutoff_date:
                try:
                    api.destroy_status(tweet.id)
                    logging.info(f"Deleted tweet with ID: {tweet.id}")
                    deleted_count += 1
                except tweepy.TweepError as e:
                    logging.error(f"Failed to delete tweet with ID: {tweet.id}: {e}")
            else:
                # If we've reached tweets newer than the cutoff date, we can stop
                break
            
            # Add a small delay to avoid hitting rate limits
            time.sleep(1)
    
    except tweepy.TweepError as e:
        logging.error(f"Error fetching tweets: {e}")
    
    logging.info(f"Deleted {deleted_count} tweets")

if __name__ == "__main__":
    delete_old_tweets()