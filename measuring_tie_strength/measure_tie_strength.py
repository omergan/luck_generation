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
        topology_score = self.topology(user, user_id, candidate, candidate_id) + self.topology(candidate, candidate_id, user, user_id)
        # likeness_score = self.likeness(user_id, candidate_id, context)
        communication_score = self.communication(user_id, user, candidate_id, candidate, context) + self.communication(candidate_id, candidate, user_id, user, context)
        logger.tie(f'Tie Score for {user} and {candidate} is {communication_score * topology_score}')
        return communication_score * topology_score

    def communication(self, user_id, user, candidate_id, candidate, context):
        logger.tie(f'Calculating communication for {user} --> {candidate}')

        # Favourites
        if self.online:
            all_favorites = twint_api.get_favorites_by_username(user, 80)
        favorites = list(filter(lambda x: x.user_id == candidate_id, all_favorites))

        if self.online:
            all_tweets = twint_api.get_tweets_from_timeline(user, 80)

        # Retweets
        all_retweets = list(filter(lambda x: x.user_id != user_id, all_tweets))
        retweets = list(filter(lambda x: x.user_id == candidate_id, all_retweets))

        # Mentions
        mentioned_in = list(filter(lambda x: x.user_id == user_id and candidate.lower() in x.mentions, all_tweets))

        logger.debug(f'User liked a total of {len(all_favorites)} tweets.')
        logger.debug(f'User liked {len(favorites)} of candidate tweets.')
        logger.debug(f'User tweeted a total of {len(all_tweets)} times.')
        logger.debug(f'User retweeted a total of {len(all_retweets)} times.')
        logger.debug(f'User retweeted {len(retweets)} of candidate tweets.')
        logger.debug(f'User mentioned candidate in {len(mentioned_in)} tweets.')
        return len(mentioned_in + retweets + favorites) / len(all_favorites + all_retweets + mentioned_in)

    def likeness(self, user_id, target_id, context):

        # Replies : how many time target_id replied to user_id
        # Retweets : how many time target_id retweeted to user_id
        # Favourites: how many time target_id liked user_id tweet

        return 0  # Replies U Retweets U Favourites

    def topology(self, user, user_id, target, target_id):
        logger.tie(f'Calculating topology for {user} --> {target}')
        if self.online:
            twint_api.get_followers(user_id, 20)
        user_followers = database_api.get_all_followers(user_id)
        if target_id in user_followers:
            return 1

        intersection = []
        if self.online:
            twint_api.get_following(target_id, 20)
        candidate_following = database_api.get_all_following(target_id)
        intersection = [follower for follower in user_followers if follower in candidate_following]
        if len(user_followers) != 0:
            return len(intersection) / len(user_followers)
        return 1