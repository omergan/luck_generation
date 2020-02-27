import database_api
import twint_api
from enums import Strength
from measuring_tie_strength import measure_tie_strength as tsm
from measuring_luck_generation import datamuse_api
import matplotlib.pyplot as plt
from utils import Logger
import pandas as pd
from collections import Counter

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
            if self.luck_calculation(tie_strength_tool, user, follower['username'], strong_set) == 0:
                follower_full_profile = database_api.get_profile(follower['username'])
                followers_of_followers = self.get_candidates(strong_set, follower_full_profile)
                for follower_of_follower in followers_of_followers:
                    self.luck_calculation(tie_strength_tool, user, follower_of_follower['username'], strong_set)

        self.luck.sort(key=lambda x: x['luck'], reverse=True)
        logger.luck(f'Weak ties scores : {self.luck}')

        self.draw_table(self.luck)
        self.draw_graph(self.luck, 'relevance', 'Occurrence', 'Relevance Histogram')
        self.draw_graph(self.luck, 'surprise', 'Occurrence', 'Surprise Histogram')
        self.draw_graph(self.luck, 'Followers', 'luck', 'Luck Histogram')
        return 0

    def luck_calculation(self, TSM, user, follower, keywords):
        relevance, surprise = TSM.measure_tie_strength(user, follower, keywords)
        NormalF = len(TSM.customer_data['relevance'])
        luck = relevance * surprise / NormalF
        logger.luck(f'Tie strength between {user} -> {follower} is done, Relevance is: {relevance}, Surprise is {surprise}')
        self.luck.append({'follower': follower, 'surprise': surprise, 'relevance': relevance, 'luck': luck})
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
        customer_profile = database_api.get_profile(username)
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

    def draw_histogram(self, data, x_label, y_label, subtitle):
        # TODO: Create set of names and values
        temp = data.copy()
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.suptitle(subtitle)
        x_axis = []
        temp.sort(key=lambda x: x[x_label], reverse=True)
        print(temp)
        for i in range(len(temp)):
            x_axis.append(temp[i][x_label])
        plt.hist(x_axis, 10)
        plt.show()

    def draw_graph(self, data, x_label, y_label, subtitle):
        temp = data.copy()
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.suptitle(subtitle)
        temp.sort(key=lambda x: x[y_label], reverse=True)
        x_dataset = []
        y_dataset = []
        for i in range(10):
            x_dataset.append(temp[i][x_label])
            y_dataset.append(temp[i][y_label])
        plt.plot(x_dataset, y_dataset)
        plt.show()

    def draw_table(self, data):
        df = pd.DataFrame.from_dict(data)
        print(df)
        df.to_excel("luck_generation_data_frame.xlsx",  index=None, header=True)