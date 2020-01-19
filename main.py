from measuring_luck_generation import generating_luck
import twint_api

from utils import Logger

logger = Logger()

logger.critical("Something went wrong!")
logger.debug("I wonder what this value is")
logger.luck("Doing some random datamuse API calls")
logger.tie("Measuring tie between people")

generating_luck.generating_luck(2993950570, "software engineering job")
# twint_api.get_tweets("software jobs positions", 1)
# twint_api.get_profile_by_username("MizrahiMichael")