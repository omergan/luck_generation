import database_api
from enums import Strength
from measuring_tie_strength import measure_tie_strength as tsm
from utils import Logger
logger = Logger()

class LuckGenerator:
    def __init__(self, is_online=False):
        self.online = is_online

    def generating_luck(self, user, context):
        logger.luck(f'Generating_luck for a given user : {user} in context of : {context}')

        # Generate set from datamuse
        strong_keywords = database_api.get_datamuse_set(context, Strength.STRONG.value)
        weak_keywords = database_api.get_datamuse_set(context, Strength.WEAK.value)

        # Update DB when new set is generated
        # strong_keywords = database_api.insert_datamuse_set('Looking for a software engineering job', set_of_words, 'strong_set')

        # Get all candidates by context
        candidates = database_api.get_all_users_by_context(context)

        # The candidates that failed to generate luck
        rejected = []

        # Dictionary [{username, strong tie score, weak tie score}] of candidate and their score
        ranking = []

        tie_strength_tool = tsm.TieStrengthTool(is_online=self.online)
        strong_tie_score = tie_strength_tool.measure_tie_strength(user, "ResilientWalker", strong_keywords, context)
        logger.luck(f'Measure tie strength for strong connection return : {strong_tie_score} for candidate {"ResilientWalker"}')
        return strong_tie_score
        # Create queue with strong measured
        # for candidate in candidates:
        #     strong_tie_score = measure_tie_strength.measure_tie_strength(user, candidate, strong_keywords, context)
        #     logging.info(f'Measure tie strength for strong connection return : {strong_tie_score} for candidate {candidate}')

        # Create queue with weak measured
        # for candidate in candidates:
        #     weak_tie_score = measure_tie_strength(user, candidate, weak_keywords, context)
        #     logging.info(f'Measure tie strength for weak connection return : {weak_tie_score} for candidate {candidate}')