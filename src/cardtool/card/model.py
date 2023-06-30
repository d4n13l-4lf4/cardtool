from dataclasses import dataclass, field
from enum import Enum

import yaml


@dataclass(frozen=True)
class CardReadingData:
    tlv: str
    track1: str
    track2: str
    pin_block: str


@dataclass(frozen=True)
class Card(yaml.YAMLObject):  # pragma: no cover
    yaml_tag = "!Card"
    yaml_loader = yaml.SafeLoader
    pan: str
    pin: str
    brand: str
    cardholder_name: str
    expiry_month: str
    expiry_year: str
    service_code: str
    sequence_number: int


@dataclass(frozen=True)
class Terminal(yaml.YAMLObject):  # pragma: no cover
    yaml_tag = "!Terminal"
    yaml_loader = yaml.SafeLoader
    country: str


@dataclass(frozen=True)
class Transaction(yaml.YAMLObject):  # pragma: no cover
    yaml_tag = "!Transaction"
    yaml_loader = yaml.SafeLoader
    country: str
    type: str
    amount: float
    other_amount: float
    currency: str
    date: str
    counter: int


@dataclass(frozen=True)
class Key(yaml.YAMLObject):  # pragma: no cover
    yaml_tag = "!Key"
    yaml_loader = yaml.SafeLoader
    bdk: str
    ksn: str


@dataclass(frozen=True)
class CardConfig(yaml.YAMLObject):  # pragma: no cover
    yaml_tag = "!CardConfig"
    yaml_loader = yaml.SafeLoader
    version: str
    transaction: Transaction = field(default_factory=dict)
    key: dict[str, Key] = field(default_factory=dict)
    terminal: Terminal = field(default_factory=dict)
    cards: list[Card] = field(default_factory=list)


class Brand(Enum):
    MASTERCARD = "Mastercard"
    VISA = "Visa"
    CARNET = "Carnet"
