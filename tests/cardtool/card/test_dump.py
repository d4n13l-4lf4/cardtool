from dataclasses import asdict
from itertools import chain
from unittest.mock import MagicMock, Mock, call, mock_open, patch

from hamcrest import assert_that, same_instance

from cardtool.card.data import CardGen
from cardtool.card.dump import CardDumper
from cardtool.card.model import Card, CardConfig, CardReadingData
from cardtool.dukpt.cipher import Cipher
from cardtool.dukpt.key_type import KeyType
from cardtool.util.serialize import Serializer


class TestDump:
    def serializer_side_effect(self, *args, **_):
        (card_dump, *_) = args
        list(card_dump)

    def test_dump_cards_should_generate_cards_successfully_when_called(self):
        m = mock_open()
        with patch("cardtool.card.dump.open", m):
            cipher = Mock(spec=Cipher)
            serializer = MagicMock(
                spec=Serializer, side_effect=self.serializer_side_effect
            )
            serializer.serialize.side_effect = self.serializer_side_effect
            generator = Mock(spec=CardGen)
            file = "test.test"
            card_config = CardConfig(
                cards=[
                    Card(
                        "pan",
                        "pin",
                        "brand",
                        "cardholder_name",
                        "expiry_month",
                        "expiry_year",
                        "service_code",
                        1,
                    ),
                    Card(
                        "pan",
                        "pin",
                        "brand",
                        "cardholder_name",
                        "expiry_month",
                        "expiry_year",
                        "service_code",
                        2,
                    ),
                ]
            )

            gen_cards = [
                CardReadingData("tlv", "track1", "track2", "pin_block1"),
                CardReadingData("tlv", "track1", "track2", "pin_block2"),
            ]
            generator.generate_data.side_effect = gen_cards
            cipher.encrypt.return_value = "encrypt"
            gen_calls = [
                call(
                    card,
                    terminal=card_config.terminal,
                    transaction=card_config.transaction,
                )
                for card in card_config.cards
            ]

            cards_values = [asdict(card).values() for card in gen_cards]
            keys = [KeyType.DATA, KeyType.DATA, KeyType.DATA, KeyType.PIN]

            cipher_calls = [
                call(val, key)
                for val, key in chain.from_iterable(
                    [list(zip(card_data, keys)) for card_data in cards_values]
                )
            ]

            dm = CardDumper(cipher=cipher, serializer=serializer, generator=generator)
            dm.dump_cards(file, card_config)
            generator.generate_data.assert_called()
            generator.generate_data.assert_has_calls(list(gen_calls), any_order=True)
            cipher.encrypt.assert_has_calls(cipher_calls)
            (mapper, stream) = serializer.serialize.call_args[0]
            m.assert_called_once_with(file, mode="w", encoding="utf-8")
            assert_that(isinstance(mapper, map))
            assert_that(stream, same_instance(m.return_value))
