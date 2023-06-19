import click

from command.gen_card import gen_card


@click.group()
def cli_card():
    pass


cli_card.add_command(gen_card)
