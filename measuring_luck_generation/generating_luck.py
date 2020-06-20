import os

import database_api
import twint_api
from measuring_tie_strength.measure_tie_strength import TieStrengthTool
from measuring_tie_strength.models import User
import networkx as nx
import math
from utils import Logger
import pandas as pd

logger = Logger()

class LuckGenerator:
    def __init__(self, username, is_online=False, limit=200):
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
        if self.online and database_api.get_profile(username) is None:
            twint_api.get_profile_by_username(username)
        self.user = User(username)

    def generating_luck(self, user, context, network, tsm: TieStrengthTool):
        logger.luck(f'Generating Luck for a given user : {user} in context of : {context}')
        customer = self.user
        strong_set = self.strict_set
        logger.luck(f'Strong keywords length {len(strong_set)}, Strong keywords: {strong_set}')

        for i, v in enumerate(self.get_candidates(customer, tsm, depth=12)):
            target: User = tsm.network.user_dict[v]
            logger.luck(f'[{i}] Calculating luck for {customer.username}: {target.username}')
            self.luck_calculation(customer, target, strong_set, True, tsm)

        self.luck.sort(key=lambda x: x['luck'], reverse=True)
        logger.luck(f'Weak ties scores : {self.luck}')
        self.draw_table(self.luck)
        return 0

    def luck_calculation(self, u: User, v: User, keywords, follower_of_follower, tsm):
        relevance, surprise, follower_data = tsm.measure_tie_strength(u.username, v.username, keywords)
        throw = False
        # Drop followers with 0 relevance for the context
        if sum(follower_data['relevance'].values()) == 0 or relevance == 0:
            throw = True

        normal = sum(follower_data['relevance'].values()) + sum(tsm.customer_data['relevance'].values())

        # Drop followers that too relevance to the context
        if normal == relevance:
            throw = True

        topology = tsm.measure_topology(u, v)
        luck = 0
        if not throw:
            relevance = relevance / normal
            surprise = surprise / normal

            orig_relevance = relevance

            surprise = math.exp(-1 * (orig_relevance - surprise))
            relevance = math.exp(orig_relevance)

            factored_relevance = math.exp(-1 * (orig_relevance - surprise - topology))
            factored_surprise = math.exp(orig_relevance + topology)

            luck = relevance + surprise
            factored_luck = factored_relevance + factored_surprise

            logger.luck(f'Tie strength between {u.username} -> {v.username} is done, Relevance is: {relevance}, '
                        f'Surprise is {surprise}, Luck is {luck}')

            self.luck.append({'follower': v, 'follower_id': v.id, 'username': v.username, 'surprise': surprise,
                              'relevance': relevance, 'luck': luck, 'NormF': normal, 'follower of follower':
                                  follower_of_follower, 'customer relevance set':
                                  tsm.customer_data['relevance'],
                              'follower set': follower_data['relevance'], 'factored_surprise': factored_surprise,
                              'factored_relevance': factored_relevance, 'factored_luck': factored_luck,
                              'topology': topology})
        else:
            self.luck.append({'follower': v, 'follower_id': v.id, 'username': v.username, 'surprise': 0, 'relevance': 0,
                              'luck': 0, 'NormF': normal, 'follower of follower': follower_of_follower,
                              'customer relevance set': tsm.customer_data['relevance'],
                              'follower set': follower_data['relevance'], 'factored_surprise': 0,
                              'factored_relevance': 0, 'factored_luck': 0, 'topology': topology})

        return luck

    def get_candidates(self, customer, tsm, reverse=False, depth=12):
        edges = nx.bfs_edges(tsm.network.graph, customer.id, reverse=reverse, depth_limit=depth)
        nodes = [v for u, v in edges]
        logger.luck(f'Candidates length {len(nodes)}')
        return set(nodes)

    def draw_table(self, data):
        df = pd.DataFrame.from_dict(data)
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../datasets')
        df.to_excel(os.path.join(path, self.user.username + " - FINAL.xlsx"),  index=None, header=True)

