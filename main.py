import database_api
from enum import Enum
from measuring_luck_generation import datamuse_api as datamuse

class Strength(Enum):
    WEAK = 1
    STRONG = 2

# Generate set from datamuse
# set_of_words = datamuse.generate_set('Looking for a software engineering job')
strong_keywords = database_api.get_datamuse_set('Looking for a software engineering job', Strength.STRONG.value)

# Update DB
# strong_keywords = database_api.insert_datamuse_set('Looking for a software engineering job', set_of_words, 'strong_set')

candidates = database_api.get_all_users_by_context('software engineering job')
rejected = []

# Create queue with strong measured
for candidate in candidates:
    # strong_measured = measure_tie_strength(self, candidate, keywords, context)
    # candidates_with_strengthes("user_name", "score")

# Create queue with weak measured
for candidate in candidates:
    # strong_measured = measure_tie_strength(self, candidate, keywords, context)
    # candidates_with_strengthes("user_name", "score")


# tweets_by_context = database_api.get_all_tweets_by_context('software engineering job')
# candidates = {x[14]: x[12] for x in tweets_by_context}
# (self, candidate, keywords, context)