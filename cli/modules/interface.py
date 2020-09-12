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
            if answers['instruction'] == 'Generating luck: Online data mining':
                self.commands.run_online_data_mining(online=True)
                continue
            if answers['instruction'] == 'Tie Strength: Build entire graph':
                x = input("Directed? Y/N ")
                while x != 'Y' and x != 'N':
                    x = input("Directed? Y/N ")
                directed = True if x == 'Y' else False
                self.commands.run_build_full_graph(directed=directed)
                continue
            if answers['instruction'] == 'Tie Strength: Build sub graph':
                answers = prompt(constants.build_sub_graph_options, style=constants.cli_style)
                self.handle_sub_graph_routine(answers['options'])
                continue
            if answers['instruction'] == 'Tie Strength: Choose color mapping':
                answers = prompt(constants.choose_color_mapping_options, style=constants.cli_style)
                self.handle_color_mapping_routine(answers['options'])
                continue
            if answers['instruction'] == 'Tie Strength: Count parameters per layer':
                threshold = input("Type parameter threshold : ")
                while not threshold.isnumeric():
                    threshold = input("Type threshold : ")
                self.commands.run_count_parameters(int(threshold))
                continue
            if answers['instruction'] == 'Tie Strength: Extract qualification data':
                self.commands.run_extract_qualification_data()
                continue
            if answers['instruction'] == 'Word Cloud: Generate costumer word cloud':
                self.commands.generate_costumer_word_cloud()
                continue
            if answers['instruction'] == 'Word Cloud: Generate followers word cloud':
                self.commands.generate_followers_word_cloud()
                continue
            if answers['instruction'] == 'Word Cloud: Generate followers surprise words cloud':
                answers = prompt(constants.build_followers_surprise_word_clouds, style=constants.cli_style)
                self.handle_build_followers_surprise_word_clouds(answers['options'])
                continue

    def handle_build_followers_surprise_word_clouds(self, answer):
        self.commands.generate_followers_surprise_word_cloud(answer != 'All')

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
            threshold = input("Type luck threshold : ")
            while not threshold.isnumeric():
                threshold = input("Type threshold : ")
            self.commands.run_map_color_by_luck(int(threshold))
            return
        if answer == 'Map by relevance and surprise':
            threshold = input("Type relevance/surprise threshold : ")
            while not threshold.isnumeric():
                threshold = input("Type threshold : ")
            self.commands.run_map_color_by_relevance_and_surprise(int(threshold))
            return
        if answer == 'Map by relevance':
            threshold = input("Type relevance/surprise threshold : ")
            while not threshold.isnumeric():
                threshold = input("Type threshold : ")
            self.commands.run_map_color_by_relevance(int(threshold))
            return
        if answer == 'Map by surprise':
            threshold = input("Type relevance/surprise threshold : ")
            while not threshold.isnumeric():
                threshold = input("Type threshold : ")
            self.commands.run_map_color_by_surprise(int(threshold))
            return
