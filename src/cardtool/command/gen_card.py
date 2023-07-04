import os
from multiprocessing import Pool
from typing import Callable, Tuple

import click
import dill as pickle  # NOQA

from cardtool.card.dump import Dumper
from cardtool.card.model import CardConfig
from cardtool.util.serialize import Serialize


def init_gen_card(bootstrap: Callable[[str, str], Tuple[CardConfig, Dumper]]):
    @click.command(name="gen-card")
    @click.option("--config", "-cfg", type=click.Path(exists=True, readable=True))
    @click.option(
        "--format",
        "-fmt",
        type=click.Choice(
            [Serialize.JSON.value, Serialize.YAML.value], case_sensitive=True
        ),
    )
    @click.argument(
        "out_file",
        type=click.Path(
            writable=True,
            resolve_path=True,
            dir_okay=False,
            file_okay=True,
            exists=False,
        ),
    )
    def __inner_(config: str, format: str, out_file: str):
        with Pool(os.cpu_count()) as p:
            (cfg, dumper) = bootstrap(config, format)
            dumper.dump_cards(out_file, cfg, p.imap)
            click.echo("Done!")

    return __inner_
