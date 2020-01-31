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

        client_twitter_profile = database_api.get_profile(user)
        # Get all candidates by context and Geo location
        candidates = self.get_candidates(context, client_twitter_profile)
        # Generate set from datamuse
        # if self.online:
        #     weak_set_online = datamuse_api.generate_weak_set(context)
        #     strong_set_online = datamuse_api.generate_strong_set(context)
        #     self.store_sets(context, strong_set_online, weak_set_online)
        logger.luck(f'Candidates length {len(candidates)} ,Candidates are : {candidates}')

        strong_set = self.generate_strong_set(context)
        weak_set = self.generate_weak_set(context)

        logger.luck(f'Strong keywords length {len(strong_set)}, Strong keywords: {strong_set}')
        logger.luck(f'Weak keywords length {len(weak_set)}, Weak keywords: {weak_set}')

        # The candidates with their score against strong keywords
        strong_ties = []

        # The candidates with their score against weak keywords
        weak_ties = []

        # Tie strength tool (By Omer Ganon)
        tie_strength_tool = tsm.TieStrengthTool(is_online=self.online)

        # TODO: Redesign how to decide which candidate pass the first step, Aka, on which candidates calculate weak ties

        # Create queue with strong measured
        for candidate in candidates:
            strong_tie_score = tie_strength_tool.measure_tie_strength(user, candidate, strong_set, context)
            strong_ties.append({'candidate': candidate, 'score': strong_tie_score})
            logger.luck(f'Strong tie strength between {user} -> {candidate} is {strong_tie_score}')

        strong_ties.sort(key=lambda x: x['score'], reverse=True)

        # Create queue with weak measured
        for candidate in candidates:
            weak_tie_score = tie_strength_tool.measure_tie_strength(user, candidate, weak_set, context)
            weak_ties.append({'candidate': candidate, 'score': weak_tie_score})
            logger.luck(f'Weak tie strength between {user} -> {candidate} is {weak_tie_score}')

        weak_ties.sort(key=lambda x: x['score'], reverse=True)


        logger.debug(f'\nFinished calculating per candidate total results are:')
        logger.luck(f'Strong ties scores : {strong_ties}')
        logger.luck(f'Weak ties scores : {weak_ties}')

        # TODO: Get the highest score candidate: Weak * Strong

        return 0


    def get_candidates(self, context, client_twitter_profile):
        if self.online:
            twint_api.get_tweets(context, 20)
        candidates_by_context = database_api.get_all_users_by_context(context)
        # TODO: Filter by geo location
        candidates = list(filter(lambda x: x != client_twitter_profile[3], candidates_by_context))
        return candidates

    def generate_weak_set(self, context):
        # TODO: Create dictionary to support complex queries
        # weak_set = database_api.get_datamuse_set(context, "weak_set").split(";")
        # logger.luck(f'Weak key words{weak_set} tweets.')
        return ['graduate', 'education', 'certificate', 'experience', 'hiring', 'search',
                'innovators', 'innovation', 'team', 'linkedin', 'startup', 'work'
                , 'cv', 'market', 'salary', 'recruit', 'company', 'openings']

    def generate_strong_set(self, context):
        # TODO: Create dictionary to support complex queries
        strong_set = database_api.get_datamuse_set(context, "strong_set").split(";")
        return strong_set

    def store_sets(self, context, strong_set, weak_set):
        # Update DB when new set is generated
        strong_merged_list = []
        for set in strong_set:
            strong_merged_list += set

        weak_merged_list = []
        for set in weak_set:
            weak_merged_list += set
        database_api.insert_datamuse_set(context, strong_merged_list, weak_merged_list)