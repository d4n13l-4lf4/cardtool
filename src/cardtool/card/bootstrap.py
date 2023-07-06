import functools

import pydash.objects

from cardtool.card.cipher import get_encrypt_card
from cardtool.card.data import CardGen
from cardtool.card.dump import CardDumper
from cardtool.card.model import CardConfig, Key
from cardtool.card.pin import generate_pin_block
from cardtool.dukpt.cipher import DUKPTCipher
from cardtool.dukpt.key import generate_key
from cardtool.util.serialize import new_serializer


def bootstrap(config: CardConfig, format: str) -> CardDumper:
    shared_keys: Key = pydash.objects.get(config.key, "shared")
    cipher = DUKPTCipher(
        bdk=shared_keys.bdk, ksn=shared_keys.ksn, derive_key=generate_key
    )
    callable_cipher = get_encrypt_card(cipher)
    card_generator = CardGen(generate_pin_block).generate_data
    callable_generator = functools.partial(
        card_generator, terminal=config.terminal, transaction=config.transaction
    )
    serializer = new_serializer(format)
    return CardDumper(callable_cipher, callable_generator, serializer)
