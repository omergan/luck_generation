import click

@click.command()
@click.argument('username')
@click.argument('context')
@click.argument('network')
@click.argument('limit')
@click.option('--init', '-i')
@click.command()
def main(username, context, network, limit):
    click.echo("This is a CLI built with Click ✨")
    click.echo(f'{username} {context} {network} {limit}')


if __name__ == "__main__":
    main()