from dataclasses import dataclass
from typing import List, Protocol


class IPerformance(Protocol):
    uses: int = 0
    charm: int = 0
    requires: int = 0
    name: str = "IPerformance"
    is_instrument: bool = False


@dataclass
class NoPerformance:
    uses: int = 0
    charm: int = 0
    requires: int = 0
    name: str = "NoPerformance"
    is_instrument: bool = False


@dataclass
class Singing:
    uses: int = 1
    charm: int = 1
    requires: int = 1
    name: str = "Singing"
    is_instrument: bool = False


@dataclass
class Dancing:
    uses: int = 2
    charm: int = 3
    requires: int = 20
    name: str = "Dancing"
    is_instrument: bool = False


@dataclass
class PlayingOnHorns:
    uses: int = 2
    charm: int = 4
    requires: int = 40
    name: str = "Horn"
    is_instrument: bool = True


@dataclass
class PlayingOnMaraca:
    uses: int = 4
    charm: int = 6
    requires: int = 60
    name: str = "Maraca"
    is_instrument: bool = True


@dataclass
class PlayingOnDidgeridoo:
    uses: int = 4
    charm: int = 8
    requires: int = 80
    name: str = "Didgeridoo"
    is_instrument: bool = True


def get_all_performances() -> List[IPerformance]:
    return [
        Singing(),
        Dancing(),
        PlayingOnHorns(),
        PlayingOnMaraca(),
        PlayingOnDidgeridoo(),
    ]
