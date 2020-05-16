import database_api
import twint_api
from utils import Logger

from measuring_tie_strength.models import User, Tweet
from measuring_tie_strength.graph import Network
import networkx as nx

logger = Logger()
logger.disabled = False

# Contextual Tie Strength Measuring Tool
class TieStrengthTool:
    def __init__(self, is_online=False, limit=100, username=None):
        self.online = is_online
        self.limit = limit
        self.customer_data = self.load_user_data(username)
        self.network = None
        self.create_network()

    def load_user_data(self, user):
        if self.online:
            twint_api.get_profile_by_username(user)
        user_profile = database_api.get_profile(user)
        data = {'tweets': [], 'favorites': [], 'relevance': {}, 'profile': user_profile}
        data['tweets'] += database_api.get_all_tweets_by_username(user_profile[3])
        # logger.tie(f'{user} has {len(data["tweets"])} tweets')
        data['favorites'] += database_api.get_favorites_by_context(user_profile[0], "")
        # logger.tie(f'{user} has {len(data["favorites"])} favorites')
        return data

    def keywords_frequency(self, user_data, keywords):
        total_tweets = user_data['tweets'] + user_data['favorites']
        for keyword in keywords:
            for tweet in total_tweets:
                if keyword in tweet[2]:
                    user_data['relevance'][keyword] = tweet[2].count(keyword)

    def measure_relevance(self, customer_data, candidate_data, keywords):
        customer_relevance = customer_data['relevance']
        candidate_relevance = candidate_data['relevance']

        relevance = 0
        for keyword in keywords:
            if keyword in candidate_relevance and keyword in customer_relevance:
                relevance += candidate_relevance[keyword] + customer_relevance[keyword]

        # Communication relevance
        # Topology relevance
        # Likeness relevance
        return relevance

    def measure_surprise(self, customer_data, candidate_data, keywords):
        customer_relevance = customer_data['relevance']
        candidate_relevance = candidate_data['relevance']

        surprise = 0
        for keyword in keywords:
            if keyword in candidate_relevance and keyword not in customer_relevance:
                surprise += candidate_relevance[keyword]
            elif keyword not in candidate_relevance and keyword in customer_relevance:
                surprise += customer_relevance[keyword]

        # Communication surprise
        # Topology surprise
        # Likeness surprise
        return surprise

    def measure_tie_strength(self, user, candidate, keywords):
        logger.tie(f'Measuring tie strength for {user} and {candidate}')
        candidate_data = self.load_user_data(candidate)
        self.keywords_frequency(self.customer_data, keywords)
        self.keywords_frequency(candidate_data, keywords)
        relevance_unity = self.measure_relevance(candidate_data, self.customer_data, keywords)
        symmetric_diff = self.measure_surprise(candidate_data, self.customer_data, keywords)
        return relevance_unity, symmetric_diff, candidate_data

    def create_network(self, directed=False):
        network = Network(directed=directed)
        self.network = network

    def measure_topology(self, candidate, target):
        logger.debug(f'Measuring topology for {candidate.username} and {target.username}')
        # Common neighbours
        # common_neighbours = self.network.get_common_neighbours(candidate.id, target.id)
        # logger.tie(f'Common neighbours: {[str(x) for x in common_neighbours]}')

        # Shortest path
        shortest_path = self.network.get_shortest_path(candidate.id, target.id)
        logger.tie(f'Shortest path: {[str(x) for x in shortest_path]}')
        return len(shortest_path)

    def apply_topology(self, user, luck_list):
        topology_factors = []
        for follower in luck_list:
            follower_obj = User(follower['follower'])
            factor = self.measure_topology(user, follower_obj)
            topology_factors.append(factor)
            follower['topology'] = factor
        average = sum(topology_factors) / len(luck_list)
        for follower in luck_list:
            follower['luck'] *= abs(self.measure_topology(user, follower_obj) - average)


"""
    ANYTHING BELOW THIS SECTION IS DEPRECATED.
    CODE FOUND BELOW MAY BE USEFUL AT SOME POINT.
    FOR NOW, WE TRY TO AVOID IT.
"""
    # def communication(self, data):
    #     # Unpack data
    #     user_profile = data['user_profile']
    #     user_id = user_profile[0]
    #     all_user_tweets = data['all_user_tweets']
    #     candidate_profile = data['candidate_profile']
    #     candidate_id = candidate_profile[0]
    #     filtered_user_favorites = data['filtered_user_favorites']
    #     logger.tie(f'Calculating communication for {user_profile[2]} --> {candidate_profile[2]}')
    #
    #     # Favorites
    #     all_favorites = database_api.get_favorites(user_profile[0])
    #
    #     # Retweets
    #     all_retweets = list(filter(lambda x: x[0] != user_id, all_user_tweets))
    #     retweets = list(filter(lambda x: x[0] == candidate_id, all_retweets))
    #
    #     # Mentions
    #     mentioned_in = list(filter(lambda x: x[0] == user_id and candidate_profile[3].lower() in x.mentions, all_user_tweets))
    #
    #     logger.debug(f'{user_profile[2]} liked a total of {len(all_favorites)} tweets.')
    #     logger.debug(f'{user_profile[2]} liked {len(filtered_user_favorites)} of {candidate_profile[2]} tweets.')
    #     logger.debug(f'{user_profile[2]} tweeted a total of {len(all_user_tweets)} times.')
    #     logger.debug(f'{user_profile[2]} retweeted a total of {len(all_retweets)} times.')
    #     logger.debug(f'{user_profile[2]} retweeted {len(retweets)} of {candidate_profile[2]} tweets.')
    #     logger.debug(f'{user_profile[2]} mentioned {candidate_profile[2]} in {len(mentioned_in)} tweets.')
    #
    #     retweet_score = (len(retweets) * (len(all_retweets) - len(retweets) / len(all_retweets)))
    #     mention_score = (len(mentioned_in) * (len(all_user_tweets) - len(mentioned_in) / len(all_user_tweets)))
    #     favorite_score = (len(filtered_user_favorites) * (len(all_favorites) - len(filtered_user_favorites)) / len(all_favorites))
    #     return mention_score + retweet_score + favorite_score
    #
    # def likeness(self, data):
    #
    #     # Unpack data
    #     user_profile = data['user_profile']
    #     candidate_profile = data['candidate_profile']
    #
    #     logger.tie(f'Calculating likeness for {user_profile[2]} --> {candidate_profile[2]}')
    #
    #     user_favorites = []
    #     candidate_favorites = []
    #     # Common * Non common / total
    #     # How many common likes user and candidate have
    #     user_favorites += database_api.get_favorites(user_profile[0])
    #     candidate_favorites += database_api.get_favorites(candidate_profile[0])
    #     total_favorites = len(user_favorites + candidate_favorites)
    #     common_favorites = len(database_api.get_common_favorites(user_profile[0], candidate_profile[0]))
    #     favorite_score = common_favorites * (total_favorites - common_favorites) / total_favorites
    #
    #     logger.tie(f'Likeness Score : {favorite_score}')
    #     return favorite_score
    #
    # def topology(self, data):
    #     # TODO: Fix query for followers list
    #     # Unpack data
    #     user_profile = data['user_profile']
    #     user_id = user_profile[0]
    #     candidate_profile = data['candidate_profile']
    #     candidate_id = candidate_profile[0]
    #
    #     logger.tie(f'Calculating topology for {user_profile[2]} --> {candidate_profile[2]}')
    #
    #     if self.online:
    #         twint_api.get_followers(user_profile, self.limit)
    #     user_followers = database_api.get_all_followers_ids(user_id)
    #     if candidate_id in user_followers:
    #         logger.tie(f'{user_profile[2]} and {candidate_profile[2]} have a direct connection')
    #         return 1
    #
    #     if self.online:
    #         twint_api.get_following(candidate_id, self.limit)
    #
    #     candidate_following = database_api.get_all_following(candidate_id)
    #     intersection = [follower for follower in user_followers if follower in candidate_following]
    #     if len(user_followers) != 0:
    #         logger.debug(f'{candidate_profile[2]} follows {len(intersection)} of {user_profile[2]} followers')
    #         logger.tie(f'Topology Score : {len(intersection) / len(user_followers)}')
    #         return len(intersection) / len(user_followers)
    #     return 1
