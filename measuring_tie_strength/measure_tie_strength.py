import database_api
import twint_api
from utils import Logger

logger = Logger()

# Contextual Tie Strength Measuring Tool
class TieStrengthTool:
    def __init__(self, is_local=True):
        self.mode = is_local

    def measure_tie_strength(self, user, candidate, keywords, context):
        # likeness
        # Topology
        # Comms

        topology_score = self.topology(user, candidate)
        return topology_score

    def topology(self, user, candidate):
        logger.tie(f'Calculating topology for {user} --> {candidate}')
        user_followers = twint_api.get_followers(user, 2)
        print(user_followers)

        counter = 1
        return counter