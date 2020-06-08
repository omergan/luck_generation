import twint_api
from measuring_tie_strength import measure_tie_strength as tsm
from measuring_tie_strength.models import User
import networkx as nx
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
        self.tie_strength_tool = None

    def generating_luck(self, user, context):
        logger.luck(f'Generating Luck for a given user : {user} in context of : {context}')

        if self.online:
            twint_api.get_profile_by_username(user)

        customer = User(user)
        strong_set = self.strict_set
        logger.luck(f'Strong keywords length {len(strong_set)}, Strong keywords: {strong_set}')
        self.tie_strength_tool = tsm.TieStrengthTool(is_online=self.online, limit=self.limit, username=customer.username)

        for i, v in enumerate(self.get_candidates(customer, depth=12)):
            target: User = self.tie_strength_tool.network.user_dict[v]
            logger.luck(f'[{i}] Calculating luck for {customer.username}: {target.username}')
            self.luck_calculation(customer, target, strong_set, True)

        self.luck.sort(key=lambda x: x['luck'], reverse=True)
        logger.luck(f'Weak ties scores : {self.luck}')
        # self.tie_strength_tool.apply_topology(customer, self.luck)
        self.draw_table(self.luck)
        return 0

    def luck_calculation(self, u: User, v: User, keywords, follower_of_follower):
        relevance, surprise, follower_data = self.tie_strength_tool.measure_tie_strength(u.username, v.username, keywords)

        throw = False
        # Drop followers with 0 relevance for the context
        if sum(follower_data['relevance'].values()) == 0 or relevance == 0:
            throw = True

        NormF = sum(follower_data['relevance'].values()) + sum(self.tie_strength_tool.customer_data['relevance'].values())

        # Drop followers that too relevance to the context
        if NormF == relevance:
            throw = True

        topology = self.tie_strength_tool.measure_topology(u, v)
        luck = 0
        if not throw:
            relevance = relevance / NormF
            surprise = surprise / NormF

            R = relevance

            surprise = math.exp(-1 * (R - surprise))
            relevance = math.exp(R)

            factored_relevance = math.exp(-1 * (R - surprise - topology))
            factored_surprise = math.exp(R + topology)

            luck = relevance + surprise
            factored_luck = factored_relevance + factored_surprise

            logger.luck(f'Tie strength between {u.username} -> {v.username} is done, Relevance is: {relevance}, Surprise is {surprise}, Luck is {luck}')
            self.luck.append({'follower': v, 'follower_id': v.id, 'surprise': surprise, 'relevance': relevance, 'luck': luck, 'NormF': NormF, 'follower of follower': follower_of_follower, 'customer relevance set': self.tie_strength_tool.customer_data['relevance'], 'follower set': follower_data['relevance'], 'factored_surprise': factored_surprise, 'factored_relevance': factored_relevance, 'factored_luck': factored_luck, 'topology': topology})
        else:
            self.luck.append({'follower': v, 'follower_id': v.id, 'surprise': 0, 'relevance': 0, 'luck': 0, 'NormF': NormF, 'follower of follower': follower_of_follower, 'customer relevance set': self.tie_strength_tool.customer_data['relevance'], 'follower set': follower_data['relevance'], 'factored_surprise': 0, 'factored_relevance': 0, 'factored_luck': 0, 'topology': topology})

        return luck

    def get_candidates(self, customer, reverse=False, depth=12):
        edges = nx.bfs_edges(self.tie_strength_tool.network.graph, customer.id, reverse=reverse, depth_limit=depth)
        nodes = [v for u, v in edges]
        logger.luck(f'Candidates length {len(nodes)}')

        return set(nodes)

    @staticmethod
    def draw_table(data):
        df = pd.DataFrame.from_dict(data)
        df.to_excel("luck_generation_data_frame.xlsx",  index=None, header=True)

