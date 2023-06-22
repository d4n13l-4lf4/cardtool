import pytest
from click.testing import CliRunner
from hamcrest import assert_that, equal_to
from helper.test_common import SUCCESS_EXIT_CODE

from cardtool.command.tr31_decrypt import decrypt_tr31

testdata = [
    (
        "EFE0853B256B583D868F251CE99EA1D9",
        "08D7B4",
        "A900RA0072B0TN00N00007B2782C0DB0AFAA96F8C67EF76CD6FBD1DC71685FCFA09B5764076C008D7B4",  # noqa: E501
    ),
    (
        "EFE0853B256B583D868F251CE99EA1D9",
        "08D7B4",
        "B0080B0TN00N0000302AE1EF9E3BAAEF3446D9580D2F505485BCE347BCD3810BE13678DE57D97A96",  # noqa: E501
    ),
]

clear_key = "0123456789ABCDEFFEDCBA9876543210"
test_ids = ["version_A", "version_B"]


class TestDecryptTR31:
    @pytest.mark.parametrize("kbpk,kcv,kblock", testdata, ids=test_ids)
    def test_should_decrypt_a_tr31_key_block_successfully(self, kbpk, kcv, kblock):
        runner = CliRunner()
        output = runner.invoke(decrypt_tr31, ["--kbpk", kbpk, "--kcv", kcv, kblock])
        assert_that(output.output, equal_to(f"Plaintext Key: {clear_key}\n"))
        assert_that(output.exit_code, equal_to(SUCCESS_EXIT_CODE))
