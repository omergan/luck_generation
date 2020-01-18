import database_api
from enums import Strength
from measuring_tie_strength import measure_tie_strength

# Generate set from datamuse
strong_keywords = database_api.get_datamuse_set('Looking for a software engineering job', Strength.STRONG.value)
weak_keywords = database_api.get_datamuse_set('Looking for a software engineering job', Strength.WEAK.value)


# Update DB when new set is generated
# strong_keywords = database_api.insert_datamuse_set('Looking for a software engineering job', set_of_words, 'strong_set')

# Get all candidates by context
candidates = database_api.get_all_users_by_context('software engineering job')
print(candidates)

# The candidates that failed to generate luck
rejected = []

# Dictionary [{username, strong tie score, weak tie score}] of candidate and their score
ranking = []

# Create queue with strong measured
for candidate in candidates:
    strong_tie_score = measure_tie_strength('twitter user', candidate, strong_keywords, 'software engineering job')
    pass

# Create queue with weak measured
for candidate in candidates:
    weak_tie_score = measure_tie_strength('twitter user', candidate, weak_keywords, 'software engineering job')
    pass