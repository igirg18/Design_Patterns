from dataclasses import dataclass, field
from typing import List, Protocol

from app.fur import Ifur
from app.performance_picker import DefaultPerformancePicker, IPerformancePicker


class ITribeMember(Protocol):
    def perform(self) -> int:
        pass

    def shake_composure(self, charm: int) -> None:
        pass

    def get_energy(self) -> int:
        pass

    def get_composure(self) -> int:
        pass


@dataclass
class TribeMember:
    energy: int = 100
    composure: int = 100
    performance_picker: IPerformancePicker = field(
        default_factory=DefaultPerformancePicker
    )

    def perform(self) -> int:
        performance = self.performance_picker.pick_performance(self.energy)
        self.energy -= performance.uses
        return performance.charm

    def shake_composure(self, charm: int) -> None:
        self.composure -= charm

    def get_energy(self) -> int:
        return self.energy

    def get_composure(self) -> int:
        return self.composure


@dataclass
class TribeMemberBaseDecorator:
    inner: ITribeMember

    def perform(self) -> int:
        return self.inner.perform()

    def shake_composure(self, charm: int) -> None:
        self.inner.shake_composure(charm)

    def get_energy(self) -> int:
        return self.inner.get_energy()

    def get_composure(self) -> int:
        return self.inner.get_composure()


@dataclass
class TribeMemberWithTails(TribeMemberBaseDecorator):
    tails: int

    def perform(self) -> int:
        return self.inner.perform() + (self.tails * 3)


@dataclass
class TribeMemberWithFur(TribeMemberBaseDecorator):
    fur: Ifur

    def perform(self) -> int:
        return self.inner.perform() * self.fur.get_modifier()


@dataclass
class Tribe:
    tribe_members: List[ITribeMember] = field(default_factory=list)

    def perform(self) -> int:
        tribe_performance = 0
        for member in self.tribe_members:
            tribe_performance += member.perform()
        return tribe_performance

    def shake_composure(self, charm: int) -> None:
        for member in self.tribe_members:
            if member.get_composure() > charm:
                member.shake_composure(charm)
                return
            else:
                charm -= member.get_composure()
                member.shake_composure(member.get_composure())

    def get_energy(self) -> int:
        tribe_energy = 0
        for member in self.tribe_members:
            tribe_energy += member.get_energy()
        return tribe_energy

    def get_composure(self) -> int:
        tribe_composure = 0
        for member in self.tribe_members:
            tribe_composure += member.get_composure()
        return tribe_composure
