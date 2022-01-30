from dataclasses import dataclass, field
from typing import List, Protocol

from app.performance import IPerformance, NoPerformance, Singing, get_all_performances
from app.warehouse_for_instruments import (
    IWarehouseForInstruments,
    WarehouseForInstruments,
)


class IPerformancePicker(Protocol):
    def pick_performance(self, energy: int) -> IPerformance:
        pass

    def get_available_actions(self, energy: int) -> List[IPerformance]:
        pass


@dataclass
class BasePerformancePicker:
    all_performances: List[IPerformance] = field(default_factory=get_all_performances)
    instruments_warehouse: IWarehouseForInstruments = field(
        default_factory=WarehouseForInstruments
    )

    def pick_performance(self, energy: int) -> IPerformance:
        return NoPerformance()

    def get_available_actions(self, energy: int) -> List[IPerformance]:
        result = []
        for action in self.all_performances:
            if action.requires <= energy and (
                not action.is_instrument
                or self.instruments_warehouse.is_available(action.name)
            ):
                result.append(action)
        return result


@dataclass
class DefaultPerformancePicker(BasePerformancePicker):
    def pick_performance(self, energy: int) -> IPerformance:
        if energy > 0:
            return Singing()
        else:
            return NoPerformance()


@dataclass
class TheMostCharmingPerformancePicker(BasePerformancePicker):
    def pick_performance(self, energy: int) -> IPerformance:
        available_actions = self.get_available_actions(energy)
        action: IPerformance = NoPerformance()
        for a in available_actions:
            if a.charm > action.charm:
                action = a
        return action
