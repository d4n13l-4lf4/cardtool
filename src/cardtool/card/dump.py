import functools
from abc import ABC, abstractmethod
from typing import Callable, Iterable, TypeVar

from toolz import compose

from cardtool.card.data import Generator as Gen
from cardtool.card.model import CardConfig, CardReadingData
from cardtool.dukpt.cipher import Cipher
from cardtool.dukpt.key_type import KeyType
from cardtool.util.serialize import Serializer

T = TypeVar("T")
S = TypeVar("S")
C = Callable[[T], S]
Mapper = Callable[[C, Iterable[T]], Iterable[S]]


class Dumper(ABC):
    @abstractmethod
    def dump_cards(
        self, out_filepath: str, card_config: CardConfig, mapper: Mapper
    ):  # pragma: nocover
        pass


class CardDumper(Dumper):
    def __init__(
        self,
        cipher: Cipher,
        generator: Gen,
        serializer: Serializer,
    ):
        self.__cipher_ = cipher
        self.__generator_ = generator
        self.__serializer_ = serializer

    def dump_cards(
        self, out_filepath: str, card_config: CardConfig, mapper: Mapper = map
    ):
        cards = card_config.cards
        generate_data = functools.partial(
            self.__generator_.generate_data,
            card_config.terminal,
            card_config.transaction,
        )
        encrypt_data = self.encrypt_card
        pipeline = compose(encrypt_data, generate_data)
        with open(out_filepath, mode="w", encoding="utf-8") as out_file:
            cards_dump = mapper(pipeline, cards)
            self.__serializer_.serialize(cards_dump, out_file)

    def encrypt_card(self, card: CardReadingData) -> CardReadingData:
        enc_tlv = self.__cipher_.encrypt(card.tlv, KeyType.DATA)
        enc_track1 = self.__cipher_.encrypt(card.track1, KeyType.DATA)
        enc_track2 = self.__cipher_.encrypt(card.track2, KeyType.DATA)
        enc_pin_block = self.__cipher_.encrypt(card.pin_block, KeyType.PIN)
        return CardReadingData(enc_tlv, enc_track1, enc_track2, enc_pin_block)
