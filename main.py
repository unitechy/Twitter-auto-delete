import tweepy
import datetime
from dateutil import parser

# Set your Twitter API credentials
consumer_key = 'your_consumer_key'
consumer_secret = 'your_consumer_secret'
access_token = 'your_access_token'
access_token_secret = 'your_access_token_secret'

# Authenticate with Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Calculate the date 7 days ago
seven_days_ago = datetime.datetime.now() - datetime.timedelta(days=7)

# Fetch and delete tweets older than 7 days
for tweet in tweepy.Cursor(api.user_timeline).items():
    tweet_date = parser.parse(tweet.created_at)
    
    if tweet_date < seven_days_ago:
        try:
            api.destroy_status(tweet.id)
            print(f"Deleted tweet with ID: {tweet.id}")
        except tweepy.TweepError as e:
            print(f"Failed to delete tweet with ID: {tweet.id}: {e}")
