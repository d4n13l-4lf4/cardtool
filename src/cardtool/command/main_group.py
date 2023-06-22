import click

from cardtool.command.gen_card import gen_card
from cardtool.log.logger import configure_logger

WELCOME_MESSAGE = (
    "Welcome to our card data generation tool. Please see usage with --help flag"
)


@click.group(invoke_without_command=True)
def cli_card():
    configure_logger()
    click.echo(WELCOME_MESSAGE)


cli_card.add_command(gen_card)
