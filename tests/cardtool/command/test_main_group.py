from click.testing import CliRunner
from hamcrest import assert_that, equal_to, string_contains_in_order
from helper.test_common import SUCCESS_EXIT_CODE

from cardtool.command.main_group import WELCOME_MESSAGE, cli_card


class TestMainGroup:
    def test_should_show_a_welcome_message(self):
        runner = CliRunner()
        result = runner.invoke(cli_card, None)
        assert_that(result.exit_code, equal_to(SUCCESS_EXIT_CODE))
        assert_that(result.output, equal_to(WELCOME_MESSAGE + "\n"))

    def test_should_show_all_available_commands(self):
        runner = CliRunner()
        result = runner.invoke(cli_card, ["--help"])

        commands = ["gencard"]
        assert_that(result.exit_code, equal_to(SUCCESS_EXIT_CODE))
        assert_that(result.output, string_contains_in_order(*commands))
