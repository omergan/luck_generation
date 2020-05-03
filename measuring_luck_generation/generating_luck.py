import database_api
import twint_api
from enums import Strength
from measuring_tie_strength import measure_tie_strength as tsm
from measuring_luck_generation import datamuse_api
import math
from utils import Logger
import pandas as pd

logger = Logger()

class LuckGenerator:
    def __init__(self, is_online=False, limit=50):
        self.online = is_online
        self.limit = limit
        self.strict_set = ['software', 'engineering', 'developer', 'devops', 'computers', 'algorithm', 'TechOps',
                           'python', 'programmer', 'java', 'computer science', 'data science', 'data analyze', 'c++',
                           'web', 'framework', 'embedded', 'alpha version', 'API', 'api', 'app', 'application', 'beta',
                           'version', 'bios', 'qa', 'automation', 'agile', 'scrum', 'demo', 'development', 'device',
                           'emulator', 'freeware', 'open source', 'interface', 'operating systems', 'workflow',
                           'machine learning', 'deep learning', 'startup', 'innovation', 'internet', 'IoT', 'VR', 'code'
                           'coding']
        self.luck = []

    def generating_luck(self, user, context):
        logger.luck(f'Generating Luck for a given user : {user} in context of : {context}')

        if self.online:
            twint_api.get_profile_by_username(user)

        customer_profile = database_api.get_profile(user)

        strong_set = self.generate_strong_set(context)
        logger.luck(f'Strong keywords length {len(strong_set)}, Strong keywords: {strong_set}')

        followers = self.get_candidates(strong_set, customer_profile)
        logger.luck(f'Followers length {len(followers)} , Followers are : {followers}')

        # Tie strength tool (By Omer Ganon)
        tie_strength_tool = tsm.TieStrengthTool(is_online=self.online, limit=self.limit, username=user)
        # Luck calculation using TSM
        for follower in followers:
            self.luck_calculation(tie_strength_tool, user, follower['username'], strong_set, False)
            follower_full_profile = database_api.get_profile(follower['username'])
            followers_of_followers = self.get_candidates(strong_set, follower_full_profile)
            for follower_of_follower in followers_of_followers:
                self.luck_calculation(tie_strength_tool, user, follower_of_follower['username'], strong_set, True)

        self.luck.sort(key=lambda x: x['surprise'], reverse=True)
        logger.luck(f'Weak ties scores : {self.luck}')

        self.export_to_excel(self.luck)
        # self.draw_histogram(self.luck, 'relevance', 'occurrence', 'Relevance Histogram')
        # self.draw_histogram(self.luck, 'surprise', 'occurrence', 'Surprise Histogram')
        # self.draw_graph(self.luck,  'relevance', 'surprise', 'Surprise X Relevance Graph')
        # self.draw_graph(self.luck, 'surprise', 'luck', 'Surprise X Luck Graph')
        # self.draw_mosaic(self.luck)
        return 0

    def luck_calculation(self, TSM, user, follower, keywords, follower_of_follower):
        relevance, surprise, follower_data = TSM.measure_tie_strength(user, follower, keywords)

        # Drop followers with 0 relevance for the context
        if sum(follower_data['relevance'].values()) == 0 or relevance == 0:
            return

        NormF = sum(follower_data['relevance'].values()) + sum(TSM.customer_data['relevance'].values())

        # Drop followers that too relevance to the context
        if NormF == relevance:
            return

        relevance = relevance / NormF
        surprise = surprise / NormF

        R = relevance
        S = surprise

        r_s = R - S
        s_r = S - R

        surprise = math.exp(-1 * (R - surprise))
        relevance = math.exp(R)

        luck = relevance + surprise

        logger.luck(f'Tie strength between {user} -> {follower} is done, Relevance is: {relevance}, Surprise is {surprise}, Luck is {luck}')

        self.luck.append({'follower': follower, 'surprise': surprise, 'relevance': relevance, 'luck': luck, 'NormF': NormF, 'R-S': r_s, 'S-R': s_r, 'follower of follower': follower_of_follower, 'customer relevance set': TSM.customer_data['relevance'], 'follower set': follower_data['relevance']})
        return luck

    def get_candidates(self, keywords, client_twitter_profile):
        if self.online:
            twint_api.get_followers(client_twitter_profile[0], self.limit)
        followers_ids = database_api.get_all_followers_ids(client_twitter_profile[0])
        followers = []
        # for follower_id in followers_ids:
        #     for keyword in keywords:
        #         if database_api.get_user_tweets_by_context(follower_id, keyword):
        #             candidates.append(database_api.id_to_username(follower_id))
        for follower_id in followers_ids:
            follower = {'id': follower_id, 'username': database_api.id_to_username(follower_id)}
            followers.append(follower)
        return followers

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
        while True:
            try:
                twint_api.get_profile_by_username(username)
                customer_profile = database_api.get_profile(username)
                twint_api.get_followers(customer_profile[0], self.limit)
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

    def export_to_excel(self, data):
        df = pd.DataFrame.from_dict(data)
        df.to_excel("luck_generation_data_frame.xlsx",  index=None, header=True)
