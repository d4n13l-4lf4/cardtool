import os.path
from unittest.mock import MagicMock, Mock, patch

import pytest
from click.testing import CliRunner
from hamcrest import assert_that, equal_to

from cardtool.card.dump import Dumper
from cardtool.card.model import CardConfig
from cardtool.command.gen_card import init_gen_card


@pytest.mark.parametrize(
    "config_file,format", [("card-config.yaml", "json"), ("card-config.yaml", "yaml")]
)
@patch("cardtool.command.gen_card.Pool", new_callable=MagicMock())
def test_gen_card(_, config_file, format, data_resolver, tmp_path):
    runner = CliRunner()

    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        bootstrap = MagicMock()
        dumper = Mock(spec=Dumper)
        card_cfg = CardConfig()
        bootstrap.side_effect = [(card_cfg, dumper)]
        Mock()

        cmd = init_gen_card(bootstrap)
        cfg_file = data_resolver("data", config_file)
        out_file = os.path.join(td, "test-gen.{0}".format(format))
        result = runner.invoke(
            cmd,
            [
                "-cfg",
                cfg_file,
                "-fmt",
                format,
                out_file,
            ],
        )

        bootstrap.assert_called_once_with(cfg_file, format)
        dumper.dump_cards.assert_called_once()
        assert_that(result.output, equal_to("Done!\n"))
        assert_that(result.exit_code, equal_to(0))
