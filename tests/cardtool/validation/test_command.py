from contextlib import nullcontext as does_not_raise
from unittest.mock import Mock

import click
import pytest
from hamcrest import assert_that, equal_to

from cardtool.validation.command import apply_in_order, validate_string_callable


@pytest.mark.parametrize(
    "input,exception,expectation",
    [
        ("1", None, does_not_raise()),
        ("2", ValueError("error"), pytest.raises(ValueError, match="error")),
    ],
    ids=["valid input", "invalid input"],
)
def test_should_trigger_a_chain_of_validators_when_called(
    input, exception, expectation
):
    with expectation:
        first_validator = Mock()
        second_validator = Mock(side_effect=exception)
        validate = apply_in_order(first_validator, second_validator)
        validate(input)

    first_validator.assert_called_with(input)
    second_validator.assert_called_with(input)


@pytest.mark.parametrize(
    "input,exception,expectation",
    [
        ("1", None, does_not_raise()),
        ("2", ValueError("error"), pytest.raises(click.BadParameter, match="error")),
        (
            3,
            ValueError("parameter is not string"),
            pytest.raises(click.BadParameter, match="parameter is not string"),
        ),
    ],
    ids=["valid input", "invalid input", "invalid int input"],
)
def test_should_validate_an_option_when_called(input, exception, expectation):
    with expectation:
        validator = Mock(side_effect=exception)
        callable_validator = validate_string_callable(validator)
        out = callable_validator({}, "", input)
        validator.assert_called_with(input)
        assert_that(out, equal_to(input))
