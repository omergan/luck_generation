import database_api
import twint_api
from enums import Strength
from measuring_tie_strength import measure_tie_strength as tsm
from measuring_luck_generation import datamuse_api
from utils import Logger
logger = Logger()

class LuckGenerator:
    def __init__(self, is_online=False):
        self.online = is_online

    def generating_luck(self, user, context):
        logger.luck(f'Generating_luck for a given user : {user} in context of : {context}')

        if self.online:
            twint_api.get_profile_by_username(user)

        client_twitter_profile = database_api.get_profile(database_api.username_to_id(user))
        # Get all candidates by context
        candidates = self.get_candidates(context, client_twitter_profile)

        # Generate set from datamuse
        strong_set = self.generate_strong_set(context)
        weak_set = self.generate_weak_set(context)

        logger.debug(weak_set)

        # Update DB when new set is generated
        strong_merged_list = []
        for set in strong_set:
            strong_merged_list += set

        weak_merged_list = []
        for set in weak_set:
            weak_merged_list += set
        database_api.insert_datamuse_set('Looking for a software engineering job', strong_merged_list, weak_merged_list)
        return 0

        # The candidates that failed to generate luck
        strong_ties = []

        # Dictionary [{username, strong tie score, weak tie score}] of candidate and their score
        weak_ties = []

        tie_strength_tool = tsm.TieStrengthTool(is_online=self.online)

        # TODO: Redesign how to decide which candidate pass the first step, Aka, on which candidates calculate weak ties

        # Create queue with strong measured
        for candidate in candidates:
            strong_tie_score = tie_strength_tool.measure_tie_strength(user, candidate, strong_set, context)
            strong_ties.append({candidate: strong_tie_score})

        logger.luck(f'Measure tie strength for strong connection return : {strong_ties} for candidate {"accelerator_ffm"}')

        # Create queue with weak measured
        for candidate in candidates:
            weak_tie_score = tie_strength_tool.measure_tie_strength(user, candidate, weak_set, context)
            weak_ties.append({candidate: weak_tie_score})

        logger.luck(f'Measure tie strength for strong connection return : {weak_set} for candidate {"accelerator_ffm"}')

        return 0


    def get_candidates(self, context, client_twitter_profile):
        if self.online:
            twint_api.get_tweets(context, 20)
        candidates_by_context = database_api.get_all_users_by_context(context)

        # TODO: Filter by geo location

        return list(filter(lambda x: x[0] != client_twitter_profile[3], candidates_by_context))

    def generate_weak_set(self, context):
        weak_set = datamuse_api.generate_weak_set(context)

        # TODO: Create dictionary to support complex queries

        return weak_set

    def generate_strong_set(self, context):
        strong_set = datamuse_api.generate_strong_set(context)

        # TODO: Create dictionary to support complex queries

        return strong_set