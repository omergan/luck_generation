from __future__ import print_function, unicode_literals

import click
from cli.modules.commands import Commands
from PyInquirer import prompt
import cli.modules.cli_constants as constants

class Interface:

    def __init__(self, commands: Commands):
        try:
            self.commands = commands
            self.run()
        except Exception:
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
                print("Build sub graph")
                continue