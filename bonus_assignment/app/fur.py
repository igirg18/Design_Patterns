from typing import Protocol


class Ifur(Protocol):
    name: str

    def get_modifier(self) -> int:
        pass


class RegularFur:
    name: str = "Regular"

    def get_modifier(self) -> int:
        return 2


class StrippedFur:
    name: str = "Stripped"

    def get_modifier(self) -> int:
        return 4


class DottedFur:
    name: str = "Dotted"

    def get_modifier(self) -> int:
        return 6
