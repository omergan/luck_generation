from cli.cli_options import CliOptions
from measuring_luck_generation import generating_luck as LG
from utils import Logger
class Initializer:
    def __init__(self, options: CliOptions):
        self.CliOptions = CliOptions
        self.LG = LG.LuckGenerator(is_online=False, limit=CliOptions.limit)