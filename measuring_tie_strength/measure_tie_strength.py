import database_api
import twint_api
from utils import Logger

logger = Logger()

# Contextual Tie Strength Measuring Tool
class TieStrengthTool:
    def __init__(self, is_online=False, limit=100):
        self.online = is_online
        self.limit = limit

    def measure_relevance(self, customer, context):
        # TODO : make this work in online mode
        user_profile = database_api.get_profile(customer)
        keywords = context.split(" ")
        for kw in keywords:
            context_favorites = database_api.get_favorites_by_context(user_profile[0], kw)
            context_tweets = database_api.get_user_tweets_by_context(user_profile[0], kw)

            all_user_tweets = database_api.get_all_tweets_by_username(user_profile[3])
            all_favorites = database_api.get_favorites(user_profile[0])

        #TODO : RETWEET IS BROKEN
        # all_retweets = list(filter(lambda x: x[0] != user_profile[0], all_user_tweets))
        # print(f'all_user_tweets: {len(all_user_tweets)}, all_favorites: {len(all_favorites)}, context_favorites: {len(context_favorites)}, context_tweets: {len(context_tweets)}')

        # print(len(context_tweets + context_favorites) * (len(all_user_tweets) + len(all_favorites) - len(context_tweets + context_favorites)) / len (all_user_tweets) + len(all_favorites))
        return len(context_tweets + context_favorites) * (len(all_user_tweets) + len(all_favorites) - len(context_tweets + context_favorites)) / len (all_user_tweets) + len(all_favorites)

    def measure_tie_strength(self, user, candidate, context):

        logger.tie(f'Measuring tie strength for {user} and {candidate}')

        if self.online:
            twint_api.get_profile_by_username(candidate)
            twint_api.get_profile_by_username(user)

        user_profile = database_api.get_profile(user)
        candidate_profile = database_api.get_profile(candidate)
        if candidate_profile is None:
            twint_api.get_profile_by_username(candidate)
            candidate_profile = database_api.get_profile(candidate)
            print(candidate_profile)

        user_id = user_profile[0]
        candidate_id = candidate_profile[0]

        # Favourites
        if self.online:
            twint_api.get_favorites_by_username(user, self.limit)

        filtered_user_favorites = database_api.get_filtered_favorites(user_id, candidate_id)

        if self.online:
            twint_api.get_favorites_by_username(candidate, self.limit)

        filtered_candidate_favorites = database_api.get_filtered_favorites(candidate_id, user_id)

        # Tweets
        if self.online:
            twint_api.get_tweets_from_timeline(user, self.limit)
            twint_api.get_tweets_from_timeline(candidate, self.limit)

        all_user_tweets = database_api.get_all_tweets_by_username(user)
        all_candidate_tweets = database_api.get_all_tweets_by_username(candidate)

        data = {
            'filtered_user_favorites': filtered_user_favorites,
            'filtered_candidate_favorites': filtered_candidate_favorites,
            'all_user_tweets': all_user_tweets,
            'all_candidate_tweets': all_candidate_tweets,
            'context': context,
            'user_profile': user_profile,
            'candidate_profile': candidate_profile,
        }

        topology_score = self.topology(data) + self.topology(data)
        likeness_score = self.likeness(data)
        user_to_candidate_communication_score = self.communication(data)
        candidate_to_user_communication_score = self.communication(data)
        communication_score = user_to_candidate_communication_score + candidate_to_user_communication_score
        logger.tie(f'Tie Score for {user} and {candidate} is {communication_score + topology_score + likeness_score}')

        logger.debug(f'Comms: {communication_score} , Topology: {topology_score}, Likeness: {likeness_score}')
        return communication_score + topology_score + likeness_score

    def communication(self, data):

        # Unpack data
        user_profile = data['user_profile']
        user_id = user_profile[0]
        all_user_tweets = data['all_user_tweets']
        candidate_profile = data['candidate_profile']
        candidate_id = candidate_profile[0]
        filtered_user_favorites = data['filtered_user_favorites']
        logger.tie(f'Calculating communication for {user_profile[2]} --> {candidate_profile[2]}')

        # Favorites
        all_favorites = database_api.get_favorites(user_profile[0])

        # Retweets
        all_retweets = list(filter(lambda x: x[0] != user_id, all_user_tweets))
        retweets = list(filter(lambda x: x[0] == candidate_id, all_retweets))

        # Mentions
        mentioned_in = list(filter(lambda x: x[0] == user_id and candidate_profile[3].lower() in x.mentions, all_user_tweets))

        logger.debug(f'{user_profile[2]} liked a total of {len(all_favorites)} tweets.')
        logger.debug(f'{user_profile[2]} liked {len(filtered_user_favorites)} of {candidate_profile[2]} tweets.')
        logger.debug(f'{user_profile[2]} tweeted a total of {len(all_user_tweets)} times.')
        logger.debug(f'{user_profile[2]} retweeted a total of {len(all_retweets)} times.')
        logger.debug(f'{user_profile[2]} retweeted {len(retweets)} of {candidate_profile[2]} tweets.')
        logger.debug(f'{user_profile[2]} mentioned {candidate_profile[2]} in {len(mentioned_in)} tweets.')

        retweet_score = (len(retweets) * (len(all_retweets) - len(retweets) / len(all_retweets)))
        mention_score = (len(mentioned_in) * (len(all_user_tweets) - len(mentioned_in) / len(all_user_tweets)))
        favorite_score = (len(filtered_user_favorites) * (len(all_favorites) - len(filtered_user_favorites)) / len(all_favorites))
        return mention_score + retweet_score + favorite_score

    def likeness(self, data):

        # Unpack data
        user_profile = data['user_profile']
        candidate_profile = data['candidate_profile']

        logger.tie(f'Calculating likeness for {user_profile[2]} --> {candidate_profile[2]}')

        user_favorites = []
        candidate_favorites = []
        # Common * Non common / total
        # How many common likes user and candidate have
        user_favorites += database_api.get_favorites(user_profile[0])
        candidate_favorites += database_api.get_favorites(candidate_profile[0])
        total_favorites = len(user_favorites + candidate_favorites)
        common_favorites = len(database_api.get_common_favorites(user_profile[0], candidate_profile[0]))
        favorite_score = common_favorites * (total_favorites - common_favorites) / total_favorites

        logger.tie(f'Likeness Score : {favorite_score}')
        return favorite_score

    def topology(self, data):
        # TODO: Fix query for followers list
        # Unpack data
        user_profile = data['user_profile']
        user_id = user_profile[0]
        candidate_profile = data['candidate_profile']
        candidate_id = candidate_profile[0]

        logger.tie(f'Calculating topology for {user_profile[2]} --> {candidate_profile[2]}')

        if self.online:
            twint_api.get_followers(user_profile, self.limit)
        user_followers = database_api.get_all_followers_ids(user_id)
        if candidate_id in user_followers:
            logger.tie(f'{user_profile[2]} and {candidate_profile[2]} have a direct connection')
            return 1

        if self.online:
            twint_api.get_following(candidate_id, self.limit)

        candidate_following = database_api.get_all_following(candidate_id)
        intersection = [follower for follower in user_followers if follower in candidate_following]
        if len(user_followers) != 0:
            logger.debug(f'{candidate_profile[2]} follows {len(intersection)} of {user_profile[2]} followers')
            logger.tie(f'Topology Score : {len(intersection) / len(user_followers)}')
            return len(intersection) / len(user_followers)
        return 1