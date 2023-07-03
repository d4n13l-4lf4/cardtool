import os
from multiprocessing import Pool

import pydash.objects

from cardtool.card.data import CardGen
from cardtool.card.dump import CardDumper, Dumper
from cardtool.card.model import CardConfig, Key
from cardtool.card.pin import generate_pin_block
from cardtool.config.load import get_abs_path, safe_load
from cardtool.dukpt.cipher import DUKPTCipher
from cardtool.dukpt.key import generate_key
from cardtool.util.serialize import new_serializer


def bootstrap(config: str, format: str) -> (CardConfig, Dumper):
    with Pool(os.cpu_count()) as p:
        cfg: CardConfig = safe_load(config, get_abs_path("card-config.json"))
        shared_keys: Key = pydash.objects.get(cfg.key, "shared")
        cipher = DUKPTCipher(
            bdk=shared_keys.bdk, ksn=shared_keys.ksn, derive_key=generate_key
        )
        return (
            cfg,
            CardDumper(
                cipher,
                CardGen(generate_pin_block),
                new_serializer(format),
                mapper=p.imap,
            ),
        )
