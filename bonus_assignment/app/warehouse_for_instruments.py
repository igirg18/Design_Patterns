from dataclasses import dataclass, field
from typing import Dict, Protocol


class IWarehouseForInstruments(Protocol):
    def is_available(self, instrument_name: str) -> bool:
        pass

    def add_new_instruments(self, instrument_name: str, amount: int) -> None:
        pass

    def take_instrument_from_warehouse(self, insturment_name: str) -> None:
        pass

    def return_instrument_to_warehouse(self, instrument_name: str) -> None:
        pass

    def refill_warehouse(self) -> None:
        pass


@dataclass
class WarehouseForInstruments:
    available_instruments: Dict[str, int] = field(init=False, default_factory=dict)
    instrument_counts: Dict[str, int] = field(init=False, default_factory=dict)

    def is_available(self, instrument_name: str) -> bool:
        instrument_name = instrument_name.lower()
        return (
            self.available_instruments.get(instrument_name) is not None
            and self.available_instruments[instrument_name] > 0
        )

    def add_new_instruments(self, insturment_name: str, amount: int) -> None:
        insturment_name = insturment_name.lower()
        if self.instrument_counts.get(insturment_name) is None:
            self.instrument_counts[insturment_name] = 0
            self.available_instruments[insturment_name] = 0
        self.available_instruments[insturment_name] += amount
        self.instrument_counts[insturment_name] += amount

    def take_instrument_from_warehouse(self, instrument_name: str) -> None:
        instrument_name = instrument_name.lower()
        if self.available_instruments.get(instrument_name) is None:
            print("No Such Insturment In Warehouse")
            return
        if self.instrument_counts.get(instrument_name) == 0:
            print(f"All of {instrument_name} are already taken")
            return
        self.available_instruments[instrument_name] -= 1

    def return_instrument_to_warehouse(self, instrument_name: str) -> None:
        instrument_name = instrument_name.lower()
        if self.available_instruments.get(instrument_name) is None:
            print("No Such Insturment In Warehouse")
            return
        if (
            self.available_instruments.get(instrument_name)
            == self.instrument_counts[instrument_name]
        ):
            print(f"That {instrument_name} doesn't belong in this warehouse")
            return
        self.available_instruments[instrument_name] += 1

    def refill_warehouse(self) -> None:
        for k in self.available_instruments:
            self.available_instruments[k] = self.instrument_counts[k]
