from twitterscraper import *
from twitter_profile import *
import datetime as dt

begin = dt.date(2019, 12, 28)
end = dt.date(2019, 12, 29)
limit = 10
lang = 'english'

def get_random_tweets():
    return query_tweets("google hiring", begindate=begin, enddate=end, limit=limit, lang=lang)

def get_twitter_profile(profile_name):
    return Profile(profile_name)