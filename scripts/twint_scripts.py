import twint_api
import database_api
from utils import Logger

logger = Logger()

# Scrape only not existing users, or those who we could not scrape enough data
def need_to_be_scrap(self, username) -> bool:
    isNotExist = database_api.get_profile(username) is None
    hasEnoughTweets = len(database_api.get_all_tweets_by_username(username)) > 30
    return isNotExist or not hasEnoughTweets

def scrap(self, username):
    while True:
        try:
            if database_api.get_profile(username) is None:
                twint_api.get_profile_by_username(username)
            customer_profile = database_api.get_profile(username)
            twint_api.get_followers(username, self.limit)
            followers = self.get_candidates(self.strict_set, customer_profile)
            for i, follower in enumerate(followers):
                logger.debug(f'Scraping a customer direct follower {follower["username"]}')
                if need_to_be_scrap(self, follower['username']):
                    twint_api.get_profile_by_username(follower['username'])
                    twint_api.get_tweets_by_username(follower['username'], self.limit)

            # Recurrence on followers
            for follower in followers:
                scrap(self, follower["username"])

        except Exception:
            print(Exception)

