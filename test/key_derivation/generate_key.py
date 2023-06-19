import pytest
from hamcrest import assert_that, equal_to

from key_derivation.generate_key import generate_key
from key_derivation.key_type import KeyType

testdata = [
    # BDK, KSN
    ("0123456789ABCDEFFEDCBA9876543210", "FFFF4357486333600003"),
]


class TestGenerateKey:

    @pytest.mark.parametrize("bdk,ksn", testdata)
    def test_should_get_data_key_when_requested(self, bdk, ksn):
        data_key = "CA7091701C616F92697955B77E723D27"
        key = generate_key(bdk=bdk, ksn=ksn, key_type=KeyType.DATA)
        assert_that(key, equal_to(data_key))

    @pytest.mark.parametrize("bdk,ksn", testdata)
    def test_should_get_mac_key_when_requested(self, bdk, ksn):
        mac_key = "6FF19ADA821E250A87D77C0E1C000AA4"
        key = generate_key(bdk=bdk, ksn=ksn, key_type=KeyType.MAC)
        assert_that(key, equal_to(mac_key))

    @pytest.mark.parametrize("bdk,ksn", testdata)
    def test_should_get_pin_key_when_requested(self, bdk, ksn):
        pin_key = "6FF19ADA821EDAF587D77C0E1C00F55B"
        key = generate_key(bdk=bdk, ksn=ksn, key_type=KeyType.PIN)
        assert_that(key, equal_to(pin_key))

    @pytest.mark.parametrize("bdk,ksn", testdata)
    def test_should_get_session_key_when_requested(self, bdk, ksn):
        session_key = "6FF19ADA821EDA0A87D77C0E1C00F5A4"
        key = generate_key(bdk=bdk, ksn=ksn, key_type=KeyType.SESSION)
        assert_that(key, equal_to(session_key))

    @pytest.mark.parametrize("bdk,ksn", testdata)
    def test_should_get_ikey_when_requested(self, bdk, ksn):
        ikey = "D7147FDAFDC32CC450AA594D8D40FABF"
        key = generate_key(bdk=bdk, ksn=ksn, key_type=KeyType.IKEY)
        assert_that(key, equal_to(ikey))

    @pytest.skip
    def test_should_throw_parameter(self):
        with pytest.raises(ValueError, match='invalid parameter'):
           raise ValueError("fake")
           _ = generate_key(bdk="1", ksn="fake", key_type=KeyType.IKEY)
        print(value_err.value.args[0])

