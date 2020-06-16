from __future__ import print_function, unicode_literals

import click
from prompt_toolkit.terminal.win32_output import NoConsoleScreenBufferError

from cli.commands import Commands
from PyInquirer import style_from_dict, Token, prompt, Separator
from pprint import pprint
import cli.cli_constants as constants

class Interface:

    def __init__(self, commands: Commands):
        try:
            self.commands = commands
            answers = prompt(constants.cli_instructions, style=constants.cli_style)
            pprint(answers)
        except NoConsoleScreenBufferError:
            click.echo("No Windows console found. Are you running cmd.exe?")