from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class GeneratorConfig:
    base_tlv: str
    cards: List[str]


def dummy():
    print("Hello!")
