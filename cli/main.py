import click

from cli.cli_options import CliOptions
from cli.commands import Commands
from cli.initializer import Initializer
from cli.interface import Interface
from utils import Logger

logger = Logger()

@click.command()
@click.option('--username', default='LukeMorton', help="Social network username")
@click.option('--context', default='Looking for a software engineering job', help='Generate luck in this context')
@click.option('--network', default='Twitter', help="Input social network for simulation")
@click.option('--limit', default=10, help='Limit for web scraping')
def main(username, context, network, limit):
    logger.debug(f'Cli start with params: username:{username} context:{context} network:{network} '
                 f'limit:{limit}')
    options = CliOptions(username, context, network, limit)
    initializer = Initializer(options)
    commands = Commands(initializer)
    interface = Interface(commands)
    click.echo('Done')


if __name__ == "__main__":
    main()