import twint_api
import database_api
from utils import Logger

logger = Logger()


def scrap(self, username):
    while True:
        try:
            # twint_api.get_profile_by_username(username)
            customer_profile = database_api.get_profile(username)
            print(followers)
            # twint_api.get_followers(customer_profile[0], self.limit)
            followers = self.get_candidates(self.strict_set, customer_profile)
            for i, follower in enumerate(followers):
                logger.debug(f'Scraping a customer direct follower {follower["username"]}')
                if len(database_api.get_all_tweets_by_username(follower['username'])) < 30:
                    twint_api.get_profile_by_username(follower['username'])
                    twint_api.get_tweets_by_username(follower['username'], self.limit)

                follower_profile = database_api.get_profile(follower['username'])
                followers_of_followers = twint_api.get_followers(follower_profile[0], 5)
                followers_of_followers = self.get_candidates(self.strict_set, follower_profile)
                for j, x in enumerate(followers_of_followers):
                    logger.debug(f'{i}.{j} : {x["username"]}')
                    if len(database_api.get_all_tweets_by_username(x['username'])) < 30:
                        twint_api.get_profile_by_username(x['username'])
                        twint_api.get_tweets_by_username(x['username'], self.limit)
                        # twint_api.get_favorites_by_username(x['username'], self.limit)
        except Exception:
            print(Exception)