import click

from hyperpocket.cli.pull import pull


@click.group()
def cli():
    pass

cli.add_command(pull)

cli()
