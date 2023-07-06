from typing import Callable

from cardtool.card.model import CardReadingData
from cardtool.dukpt.cipher import Cipher
from cardtool.dukpt.key_type import KeyType


def get_encrypt_card(cipher: Cipher) -> Callable[[CardReadingData], CardReadingData]:
    def __inner_(card: CardReadingData) -> CardReadingData:
        enc_tlv = cipher.encrypt(card.tlv, KeyType.DATA)
        enc_track1 = cipher.encrypt(card.track1, KeyType.DATA)
        enc_track2 = cipher.encrypt(card.track2, KeyType.DATA)
        enc_pin_block = cipher.encrypt(card.pin_block, KeyType.PIN)
        return CardReadingData(enc_tlv, enc_track1, enc_track2, enc_pin_block)

    return __inner_
