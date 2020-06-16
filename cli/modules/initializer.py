import os
import pandas as pd

from cli.modules.cli_options import CliOptions
from measuring_luck_generation.generating_luck import LuckGenerator
from measuring_tie_strength.measure_tie_strength import TieStrengthTool
from utils import Logger

logger = Logger()


class Initializer:
    def __init__(self, options: CliOptions):
        self.options = options
        self.LG = LuckGenerator(options.username, is_online=options.online, limit=options.limit)
        self.TSM = TieStrengthTool(is_online=options.online, limit=options.limit,
                                   username=options.username)
        self.EXCEL = None
        my_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(my_path, '../../datasets/')
        directory = os.listdir(path)
        for file in directory:
            if options.username in file:
                df = pd.read_excel(os.path.join(path, file))
                self.EXCEL = list(df.T.to_dict().values())
                break