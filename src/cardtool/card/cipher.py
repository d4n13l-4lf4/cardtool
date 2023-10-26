from cardtool.card.model import CardReadingData
from cardtool.dukpt.cipher import Cipher
from cardtool.dukpt.key_type import KeyType

TRACK2_PAD = 0xFF
DEFAULT_PAD = 0x00


def encrypt_card(
    data_cipher: Cipher, pin_cipher: Cipher, card: CardReadingData
) -> CardReadingData:
    enc_tlv = data_cipher.encrypt(card.tlv, KeyType.DATA, DEFAULT_PAD)
    enc_track1 = data_cipher.encrypt(card.track1, KeyType.DATA, DEFAULT_PAD)
    enc_track2 = data_cipher.encrypt(card.track2, KeyType.DATA, TRACK2_PAD)
    enc_pin_block = pin_cipher.encrypt(card.pin_block, KeyType.PIN, DEFAULT_PAD)
    return CardReadingData(enc_tlv, enc_track1, enc_track2, enc_pin_block, card.label)
