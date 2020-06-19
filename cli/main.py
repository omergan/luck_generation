import click

from cli.modules.cli_options import CliOptions
from cli.modules.commands import Commands
from cli.modules.initializer import Initializer
from cli.modules.interface import Interface
from utils import Logger

logger = Logger()

@click.command()
@click.option('--username', default='LukeMorton', help="Social network username")
@click.option('--context', default='Looking for a software engineering job', help='Generate luck in this context')
@click.option('--network', default='Twitter', help="Input social network for simulation")
@click.option('--limit', default=200, help='Limit for web scraping')
@click.option('--online', default=False, help='Run simulation online/local')
def cli(username, context, network, limit, online):
    logger.debug(f'\nCli is initialized with the following params:\nUsername: {username}\nContext: {context}\nNetwork: {network}\nLimit:{limit}\n')
    options = CliOptions(username, context, network, limit, online)
    initializer = Initializer(options)
    commands = Commands(initializer)
    interface = Interface(commands)
    logger.debug(f'\nDone')


if __name__ == "__main__":
    cli()