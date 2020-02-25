import database_api
import twint_api
from enums import Strength
from measuring_tie_strength import measure_tie_strength as tsm
from measuring_luck_generation import datamuse_api
from utils import Logger
logger = Logger()

class LuckGenerator:
    def __init__(self, is_online=False, limit=100):
        self.online = is_online
        self.limit = limit
        self.strict_set = ['software', 'engineering', 'developer', 'devops', 'computers', 'algorithm', 'TechOps',
                           'python', 'programmer', 'java', 'computer science', 'data science', 'data analyze', 'c++',
                           'web', 'framework', 'embedded', 'alpha version', 'API', 'api', 'app', 'application', 'beta',
                           'version', 'bios', 'qa', 'automation', 'agile', 'scrum', 'demo', 'development', 'device',
                           'emulator', 'freeware', 'open source', 'interface', 'operating systems', 'workflow',
                           'machine learning', 'deep learning', 'startup']

    def generating_luck(self, user, context):
        logger.luck(f'Generating_luck for a given user : {user} in context of : {context}')

        if self.online:
            twint_api.get_profile_by_username(user)

        customer_profile = database_api.get_profile(user)

        strong_set = self.generate_strong_set(context)
        logger.luck(f'Strong keywords length {len(strong_set)}, Strong keywords: {strong_set}')

        followers = self.get_candidates(strong_set, customer_profile)
        logger.luck(f'Candidates length {len(followers)} ,Candidates are : {followers}')

        # The candidates with their score against weak keywords
        luck = []

        # Tie strength tool (By Omer Ganon)
        tie_strength_tool = tsm.TieStrengthTool(is_online=self.online, limit=self.limit, username=user)

        for follower in followers:
            # The connection between the customer and given context -> Match,
            # The connection between the customer and given candidate -> Mismatch
            relevance, surprise = tie_strength_tool.measure_tie_strength(user, follower['username'], strong_set)
            if relevance == 0:
                followers_of_followers = database_api.get_all_followers_ids(follower['id'])
                for follower_of_follower in followers_of_followers:
                    luck.append({'candidate': follower_of_follower, 'surprise': surprise, 'relevance': relevance})
                    logger.luck(f'Relevance between {user} -> {follower_of_follower} is {relevance}')
                    logger.luck(f'Surprise between {user} -> {follower_of_follower} is {surprise}')
            luck.append({'candidate': follower, 'surprise': surprise, 'relevance': relevance})
            logger.luck(f'Relevance between {user} -> {follower} is {relevance}')
            logger.luck(f'Surprise between {user} -> {follower} is {surprise}')

        luck.sort(key=lambda x: x['relevance'], reverse=True)
        logger.debug(f'\nFinished calculating per candidate total results are:')
        logger.luck(f'Weak ties scores : {luck}')

        # TODO: Get the highest score candidate: Weak * Strong

        return 0

    def get_candidates(self, keywords, client_twitter_profile):
        if self.online:
            twint_api.get_followers(client_twitter_profile[0], self.limit)
        followers_ids = database_api.get_all_followers_ids(client_twitter_profile[0])
        candidates = []
        # for follower_id in followers_ids:
        #     for keyword in keywords:
        #         if database_api.get_user_tweets_by_context(follower_id, keyword):
        #             candidates.append(database_api.id_to_username(follower_id))
        for follower_id in followers_ids:
            follower = {'id': follower_id, 'username': database_api.id_to_username(follower_id)}
            candidates.append(follower)
        return candidates

    def generate_strong_set(self, context):
        # TODO: Create dictionary to support complex queries
        strong_set = []
        # if self.online:
        #     strong_set = datamuse_api.generate_strong_set(context)
        #     database_api.insert_datamuse_set(context, strong_set, [])
        # else:
        #     strong_set = database_api.get_datamuse_set(context, "strong_set")
        #     if len(strong_set) == 0:
        #         strong_set = datamuse_api.generate_strong_set(context)
        #         database_api.insert_datamuse_set(context, strong_set, [])
        #     else:
        #         strong_set = strong_set.split(";")
        return self.strict_set

    def store_sets(self, context, strong_set, weak_set):
        # Update DB when new set is generated
        strong_merged_list = []
        for set in strong_set:
            strong_merged_list += set

        weak_merged_list = []
        for set in weak_set:
            weak_merged_list += set
        database_api.insert_datamuse_set(context, strong_merged_list, weak_merged_list)

    def scrap(self, username):
        customer_profile = database_api.get_profile(username)
        followers = self.get_candidates(self.strict_set, customer_profile)
        for follower in followers:
            if len(database_api.get_all_tweets_by_username(follower['username'])) < 200:
                twint_api.get_profile_by_username(follower['username'])