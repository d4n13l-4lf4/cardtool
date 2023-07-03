import functools
from abc import ABC, abstractmethod
from typing import Callable, Iterable, TypeVar

import dill as pickle  # NOQA
from toolz import compose

from cardtool.card.data import Generator as Gen
from cardtool.card.model import CardConfig, CardReadingData
from cardtool.dukpt.cipher import Cipher
from cardtool.dukpt.key_type import KeyType
from cardtool.util.serialize import Serializer

T = TypeVar("T")
S = TypeVar("S")
C = Callable[[T], S]


class Dumper(ABC):
    @abstractmethod
    def dump_cards(self, out_filepath: str, card_config: CardConfig):  # pragma: nocover
        pass


class CardDumper(Dumper):
    def __init__(
        self,
        cipher: Cipher,
        generator: Gen,
        serializer: Serializer,
        mapper: Callable[[C, Iterable[T]], Iterable[S]] = map,
    ):
        self.__cipher_ = cipher
        self.__generator_ = generator
        self.__serializer_ = serializer
        self.__mapper_ = mapper

    def dump_cards(self, out_filepath: str, card_config: CardConfig):
        cards = card_config.cards
        generate_data = functools.partial(
            self.__generator_.generate_data,
            terminal=card_config.terminal,
            transaction=card_config.transaction,
        )
        encrypt_data = self.__encrypt_card_
        pipeline = compose(encrypt_data, generate_data)
        with open(out_filepath, mode="w", encoding="utf-8") as out_file:
            cards_dump = self.__mapper_(pipeline, cards)
            self.__serializer_.serialize(cards_dump, out_file)

    def __encrypt_card_(self, card: CardReadingData) -> CardReadingData:
        enc_tlv = self.__cipher_.encrypt(card.tlv, KeyType.DATA)
        enc_track1 = self.__cipher_.encrypt(card.track1, KeyType.DATA)
        enc_track2 = self.__cipher_.encrypt(card.track2, KeyType.DATA)
        enc_pin_block = self.__cipher_.encrypt(card.pin_block, KeyType.PIN)
        return CardReadingData(enc_tlv, enc_track1, enc_track2, enc_pin_block)
