from __future__ import print_function, unicode_literals
import traceback
import sys
import click
from cli.modules.commands import Commands
from PyInquirer import prompt
import cli.modules.cli_constants as constants

from utils import Logger
logger = Logger()

class Interface:

    def __init__(self, commands: Commands):
        try:
            self.commands = commands
            self.run()
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            click.echo("No Windows console found. Are you running cmd.exe?")

    def run(self):
        while True:
            answers = prompt(constants.cli_instructions, style=constants.cli_style)
            if answers['instruction'] == 'Exit':
                break
            if answers['instruction'] == 'Generating luck: Run simulation':
                x = input("Run online? Y/N ")
                while x != 'Y' and x != 'N':
                    x = input("Run online? Y/N ")
                online = True if x == 'Y' else False
                self.commands.run_generating_luck_simulation(online=online)
                continue
            if answers['instruction'] == 'Build entire graph':
                x = input("Directed? Y/N ")
                while x != 'Y' and x != 'N':
                    x = input("Directed? Y/N ")
                directed = True if x == 'Y' else False
                self.commands.run_build_full_graph(directed=directed)
                continue
            if answers['instruction'] == 'Build sub graph':
                answers = prompt(constants.build_sub_graph_options, style=constants.cli_style)
                self.handle_sub_graph_routine(answers['options'])
                continue
            if answers['instruction'] == 'Choose color mapping':
                answers = prompt(constants.choose_color_mapping_options, style=constants.cli_style)
                self.handle_color_mapping_routine(answers['options'])
                continue

    def handle_sub_graph_routine(self, answer):
        if answer == 'Back':
            return
        if answer == 'Filter by topology':
            topology = input("Type topology threshold : ")
            while not topology.isnumeric():
                topology = input("Type topology threshold : ")
            self.commands.run_build_sub_graph_by_topology(topology)
            return
        if answer == 'Filter by luck':
            return
        if answer == 'Filter by relevance and surprise':
            return

    def handle_color_mapping_routine(self, answer):
        if answer == 'Back':
            return
        if answer == 'Map by luck':
            self.commands.run_map_color_by_luck()
            return
        if answer == 'Map by relevance and surprise':
            self.commands.run_map_color_by_relevance_and_surprise()
            return
