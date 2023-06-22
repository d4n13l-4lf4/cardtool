from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import List


class TR31Version(Enum):
    A = "A"
    B = "B"


@dataclass(frozen=True)
class KeyBlock:
    version: TR31Version
    hex_length: str
    length: int
    key_usage: str
    algorithm: str
    use_mode: str
    key_version: str
    exportability: str
    optional_blocks: str
    future_use: str
    key_data: str
    authenticator: str


class TR31Parse(ABC):
    # TODO: check if coverage completes when used
    @abstractmethod
    def parse_key_block(self, key_block: str) -> KeyBlock:  # pragma: no cover
        pass


class TR31Parser(TR31Parse):
    def __init__(self):
        self.__ind_mapping_ = [1, 5, 7, 8, 9, 11, 12, 14, 16]

    def parse_key_block(self, key_block: str) -> KeyBlock:
        if key_block.startswith(TR31Version.A.value):
            return self.__parse_version_A_(key_block)
        if key_block.startswith(TR31Version.B.value):
            return self.__parse_version_B_(key_block)
        raise NotImplementedError(f"unknown key block version {key_block[0]}")

    def __parse_version_A_(self, key_block: str) -> KeyBlock:
        ind_mapping = self.__ind_mapping_ + [64, 72]
        return self.__parse_block_(key_block, ind_mapping)

    def __parse_version_B_(self, key_block: str) -> KeyBlock:
        ind_mapping = self.__ind_mapping_ + [64, 80]
        return self.__parse_block_(key_block, ind_mapping)

    def __parse_block_(self, key_block: str, ind_mapping: List[int]) -> KeyBlock:
        out_values = []
        initial_index = 0
        for ix, ind in enumerate(ind_mapping):
            val = key_block[initial_index:ind]
            if ix == 0:
                val = TR31Version[val]
            out_values.append(val)
            if ix == 1:
                out_values.append(int(val, 16))
            initial_index += ind - initial_index
        return KeyBlock(*out_values)
