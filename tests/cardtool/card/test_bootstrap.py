from unittest.mock import patch

from hamcrest import assert_that, instance_of, same_instance

from cardtool.card.bootstrap import bootstrap
from cardtool.card.dump import CardDumper, Dumper
from cardtool.card.model import CardConfig, Key
from cardtool.util.serialize import Serialize


@patch("cardtool.card.bootstrap.get_abs_path")
@patch("cardtool.card.bootstrap.safe_load")
def test_bootstrap_should_create_a_dumper_when_called(safe_load, get_abs_path):
    cfg = CardConfig(key={"shared": Key()})
    safe_load.return_value = cfg
    get_abs_path.return_value = "test"
    (cfg, dumper) = bootstrap("cfg_file.yaml", Serialize.JSON.value)
    safe_load.assert_called_once_with("cfg_file.yaml", "test")
    get_abs_path.assert_called_once_with("card-config.json")
    assert_that(cfg, same_instance(cfg))
    assert_that(dumper, instance_of(CardDumper))
    assert_that(issubclass(dumper.__class__, Dumper))
