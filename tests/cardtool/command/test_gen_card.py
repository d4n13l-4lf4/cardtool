import json
import os
from typing import Any, Callable, Dict

import pytest
from click.testing import CliRunner
from hamcrest import assert_that, equal_to

from cardtool.command.gen_card import gen_card


@pytest.mark.parametrize("config_file,expected_file", [("config.yaml", "cards.json")])
def test_gen_json_card(
    config_file, expected_file, tmp_path, data_resolver: Callable[[str], str]
):
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path):
        config_file_fullpath = data_resolver(config_file)
        expected_file_fullpath = data_resolver(expected_file)
        outfile_fullpath = os.path.join(tmp_path, expected_file)
        result = runner.invoke(
            gen_card,
            [
                "--config",
                config_file_fullpath,
                "--format",
                "json",
                "--name",
                outfile_fullpath,
            ],
        )
        cards = load_json_dict(outfile_fullpath)
        expected_cards = load_json_dict(expected_file_fullpath)
        assert_that(result.exit_code, equal_to(0))
        assert_that(cards, equal_to(expected_cards))


def load_json_dict(file: str) -> Dict[str, Any]:
    with open(file, mode="r", encoding="utf-8") as f:
        return json.load(f)
