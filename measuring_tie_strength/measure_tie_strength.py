import database_api
import twint_api
from utils import Logger

logger = Logger()

# Contextual Tie Strength Measuring Tool
class TieStrengthTool:
    def __init__(self, is_online=False):
        self.online = is_online

    def measure_tie_strength(self, user, candidate, keywords, context):
        # likeness
        # Topology
        # Comms
        if self.online:
            twint_api.get_profile_by_username(candidate)
            twint_api.get_profile_by_username(user)

        candidate_id = database_api.username_to_id(candidate)
        user_id = database_api.username_to_id(user)


        # TODO : code below is placeholder
        topology_score = self.topology(user_id, candidate_id) + self.topology(candidate_id, user_id)
        communication_score = self.communication(user_id, candidate_id, context)
        likeness_score = self.likeness(user_id, candidate_id, context)
        return topology_score * communication_score * likeness_score

    def likeness(self, user_id, target_id, context):

        # Common Favourites
        # Common Retweets
        # Common Replies

        return 0  # Favourites U Retweets U Replies

    def communication(self, user_id, target_id, context):

        # Replies : how many time target_id replied to user_id
        # Retweets : how many time target_id retweeted to user_id
        # Favourites: how many time target_id liked user_id tweet

        return 0  # Replies U Retweets U Favourites

    def topology(self, user_id, target_id):
        logger.tie(f'Calculating topology for {user_id} --> {target_id}')
        if self.online:
            twint_api.get_followers(user_id, 200)
        user_followers = database_api.get_all_followers(user_id)
        if target_id in user_followers:
            return 1

        intersection = []
        if self.online:
            twint_api.get_following(target_id, 200)
        candidate_following = database_api.get_all_following(target_id)
        intersection = [follower for follower in user_followers if follower in candidate_following]
        return len(intersection)