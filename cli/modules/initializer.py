from cli.modules.cli_options import CliOptions
from measuring_luck_generation.generating_luck import LuckGenerator
from measuring_tie_strength.measure_tie_strength import TieStrengthTool
from utils import Logger

logger = Logger()


class Initializer:
    def __init__(self, options: CliOptions):
        self.options = options
        self.LG = LuckGenerator(is_online=options.online, limit=options.limit)
        self.TSM = TieStrengthTool(is_online=options.online, limit=options.limit,
                                   username=options.username)
