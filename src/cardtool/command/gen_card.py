import json

import click
from loguru import logger


@click.command(name="gencard")
@click.option("--config", type=click.Path(exists=True, readable=True))
@click.option(
    "--format", type=click.Choice(["json", "yaml", "stdout"], case_sensitive=True)
)
@click.option(
    "--name",
    type=click.Path(
        writable=True, resolve_path=True, dir_okay=False, file_okay=True, exists=False
    ),
)
def gen_card(config, format, name):
    with open(name, mode="w", encoding="utf-8") as card_file:
        logger.info("Something awesome!")
        fake_card = [
            {
                "label": "VISA_PAN",
                "card": "4455220000000001234",
                "tlv": "",
                "track1": "",
                "track2": "",
                "pin_block": "",
                "ksn": "",
            },
            {
                "label": "VISA_PAN",
                "card": "4645960000001234",
                "tlv": "",
                "track1": "",
                "track2": "",
                "pin_block": "",
                "ksn": "",
            },
        ]
        card_file.write(json.dumps(fake_card))
