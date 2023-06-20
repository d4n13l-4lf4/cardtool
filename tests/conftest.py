import os
from typing import Callable

import pytest


@pytest.fixture
def data_resolver() -> Callable[[], str]:
    def inner(file: str):
        current_dir = os.path.dirname(__file__)
        config_path = os.path.join(current_dir, "data", file)
        return config_path

    return inner
