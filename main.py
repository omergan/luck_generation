from measuring_luck_generation import generating_luck
import twint_api

from utils import Logger

logger = Logger()

logger.luck("Calculating luck starts")
print(generating_luck.generating_luck("MizrahiMichael", "software engineering job"))