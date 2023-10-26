from dataclasses import asdict
from unittest.mock import Mock, call

import pydash
from hamcrest import assert_that, equal_to

from cardtool.card.cipher import encrypt_card
from cardtool.card.model import CardReadingData
from cardtool.dukpt.cipher import Cipher
from cardtool.dukpt.key_type import KeyType


def test_should_cipher_card_data_successfully_when_called():
    data_cipher = Mock(spec=Cipher)
    data_cipher.encrypt.return_value = "encrypt"

    pin_cipher = Mock(spec=Cipher)
    pin_cipher.encrypt.return_value = "pin_encrypt"

    card_data = CardReadingData("tlv", "track1", "track2", "pin", "test")
    encrypted_data = encrypt_card(data_cipher, pin_cipher, card_data)
    expected_data = CardReadingData(
        "encrypt", "encrypt", "encrypt", "pin_encrypt", "test"
    )
    padding = {"track2": 0xFF}

    keys = [KeyType.DATA] * 3
    pin_keys = [KeyType.PIN]

    data_values = asdict(card_data).values()
    pin_values = ["pin"]

    data_cipher.encrypt.assert_has_calls(
        [
            call(data, key, pydash.objects.get(padding, data, 0x00))
            for data, key in zip(data_values, keys)
        ]
    )

    pin_cipher.encrypt.assert_has_calls(
        [
            call(data, key, pydash.objects.get(padding, data, 0x00))
            for data, key in zip(pin_values, pin_keys)
        ]
    )

    assert_that(encrypted_data, equal_to(expected_data))
