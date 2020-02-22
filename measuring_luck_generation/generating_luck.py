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

    def generating_luck(self, user, context):
        logger.luck(f'Generating_luck for a given user : {user} in context of : {context}')

        if self.online:
            twint_api.get_profile_by_username(user)

        client_twitter_profile = database_api.get_profile(user)

        # Generate set from datamuse
        strong_set = self.generate_strong_set(context)

        # Get all candidates by context and Geo location
        candidates = self.get_candidates(strong_set, client_twitter_profile)

        logger.luck(f'Candidates length {len(candidates)} ,Candidates are : {candidates}')
        logger.luck(f'Strong keywords length {len(strong_set)}, Strong keywords: {strong_set}')

        # The candidates with their score against weak keywords
        luck = []

        # Tie strength tool (By Omer Ganon)
        tie_strength_tool = tsm.TieStrengthTool(is_online=self.online, limit=self.limit)

        # TODO: Redesign how to decide which candidate pass the first step, Aka, on which candidates calculate weak ties

        # The connection between the customer and given context -> Match
        relevance = tie_strength_tool.measure_relevance(user, context)

        for candidate in candidates:
            # The connection between the customer and given candidate -> Mismatch
            surprise = tie_strength_tool.measure_tie_strength(user, candidate, context)
            luck.append({'candidate': candidate, 'score': surprise * relevance})
            logger.luck(f'Weak tie strength between {user} -> {candidate} is {surprise}')

        luck.sort(key=lambda x: x['score'], reverse=True)
        logger.debug(f'\nFinished calculating per candidate total results are:')
        logger.luck(f'Weak ties scores : {luck}')

        # TODO: Get the highest score candidate: Weak * Strong

        return 0

    def get_candidates(self, keywords, client_twitter_profile):
        followers_ids = database_api.get_all_followers_ids(client_twitter_profile[0])
        candidates = []
        for follower_id in followers_ids:
            if self.online:
                twint_api.get_tweets_by_username(follower_id, self.limit)
            for keyword in keywords:
                if database_api.get_user_tweets_by_context(follower_id, keyword):
                    candidates.append(database_api.id_to_username(follower_id))
        return candidates

    def generate_strong_set(self, context):
        # TODO: Create dictionary to support complex queries
        # strong_set = database_api.get_datamuse_set(context, "strong_set").split(";")
        return ['software', 'job', 'engineering', 'developer']

    def store_sets(self, context, strong_set, weak_set):
        # Update DB when new set is generated
        strong_merged_list = []
        for set in strong_set:
            strong_merged_list += set

        weak_merged_list = []
        for set in weak_set:
            weak_merged_list += set
        database_api.insert_datamuse_set(context, strong_merged_list, weak_merged_list)