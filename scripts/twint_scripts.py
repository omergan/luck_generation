import twint_api
import database_api
from measuring_tie_strength.models import User
from utils import Logger

logger = Logger()
MAX_DEPTH = 6

# Scrape only not existing users, or those who we could not scrape enough data
def need_to_be_scrap(self, username) -> bool:
    isNotExist = database_api.get_profile(username) is None
    hasEnoughTweets = len(database_api.get_all_tweets_by_username(username)) > 10
    return isNotExist or not hasEnoughTweets

def scrap(self, username, depth=0):
    try:
        if depth == MAX_DEPTH:
            return
        if need_to_be_scrap(self, username):
            twint_api.get_profile_by_username(username)
            twint_api.get_tweets_by_username(username, self.limit)
        user = User(username)
        followers_ids = database_api.get_all_followers_ids(user.id)
        if len(followers_ids) < 10:
            twint_api.get_followers(username, self.limit)
            followers_ids = database_api.get_all_followers_ids(user.id)
        for i, follower_id in enumerate(followers_ids):
            if i == self.limit:
                break
            follower = User(follower_id, is_id=True)
            if need_to_be_scrap(self, follower.username):
                logger.debug(f'Scraping a customer direct follower {follower.username} in depth -> {depth}')
                twint_api.get_profile_by_username(follower.username)
                twint_api.get_tweets_by_username(follower.username, self.limit)

        # Recurrence on followers
        for follower_id in followers_ids:
            follower = User(follower_id, is_id=True)
            scrap(self, follower.username, depth+1)
    except Exception:
        print(Exception)

