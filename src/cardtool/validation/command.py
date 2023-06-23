from functools import wraps
from typing import Callable

import click


def validate_string_callable(validate: Callable[[str], None]):
    @wraps(validate)
    def wrapper(*args, **_) -> str:
        (_, _, value) = args
        if not isinstance(value, str):
            raise click.BadParameter("parameter is not string")
        try:
            validate(value)
            return value
        except ValueError as e:
            raise click.BadParameter("{0}".format(e))

    return wrapper


def InOrder(*validator: Callable[[str], None]):
    def __inner_(data: str):
        for validate in validator:
            validate(data)

    return __inner_
