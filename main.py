from measuring_luck_generation import generating_luck as LG
from measuring_tie_strength import measure_tie_strength as tsm
import twint_api
from measuring_luck_generation import datamuse_api
import database_api

LIMIT = 200

from utils import Logger
logger = Logger()

if __name__ == '__main__':
    logger.debug("Starting main program!\n")
    luck_generator = LG.LuckGenerator(is_online=False, limit=LIMIT)
    luck_generator.generating_luck("Charliedysonrec", "Looking for a software engineering job")
    # luck_generator.scrap("MizrahiMichael")
    # luck_generator.draw_mosaic(None)
    logger.debug("\nEnding main program!")
