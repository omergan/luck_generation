from __future__ import print_function, unicode_literals

import click
from prompt_toolkit.terminal.win32_output import NoConsoleScreenBufferError

from cli.modules.commands import Commands
from PyInquirer import prompt
import cli.modules.cli_constants as constants


def run():
    while True:
        answers = prompt(constants.cli_instructions, style=constants.cli_style)
        if answers['instruction'] == 'Exit':
            break
        if answers['instruction'] == 'Generating luck: Run simulation':
            print("Generating luck: Run simulation")
            continue
        if answers['instruction'] == 'Build entire graph':
            print("Build entire graph")
            continue
        if answers['instruction'] == 'Build sub graph':
            print("Build sub graph")
            continue


class Interface:

    def __init__(self, commands: Commands):
        try:
            self.commands = commands
            run()
        except NoConsoleScreenBufferError:
            click.echo("No Windows console found. Are you running cmd.exe?")
