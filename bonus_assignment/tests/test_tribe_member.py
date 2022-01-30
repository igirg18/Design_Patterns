from typing import List

import pytest

from app.fur import DottedFur, RegularFur
from app.performance import (
    Dancing,
    IPerformance,
    PlayingOnDidgeridoo,
    PlayingOnHorns,
    PlayingOnMaraca,
    Singing,
)
from app.performance_picker import IPerformancePicker, TheMostCharmingPerformancePicker
from app.tribe_member import (
    ITribeMember,
    Tribe,
    TribeMember,
    TribeMemberWithFur,
    TribeMemberWithTails,
)
from app.warehouse_for_instruments import (
    IWarehouseForInstruments,
    WarehouseForInstruments,
)


@pytest.fixture
def tribe_member_with_regular_fur() -> ITribeMember:
    return TribeMemberWithFur(TribeMember(), RegularFur())


@pytest.fixture
def tribe_member_with_dotted_fur() -> ITribeMember:
    return TribeMemberWithFur(TribeMember(), DottedFur())


@pytest.fixture
def tribe_member_with_tails() -> ITribeMember:
    return TribeMemberWithTails(TribeMember(), 3)


def test_regular_tribe_member_default_performance_picker() -> None:
    member = TribeMember()
    emitted_charm = member.perform()
    assert emitted_charm == 1
    assert member.get_energy() == 99
    member.shake_composure(emitted_charm)
    assert member.get_composure() == 99


def test_tribe_member_with_regular_fur(
    tribe_member_with_regular_fur: ITribeMember,
) -> None:
    emitted_charm = tribe_member_with_regular_fur.perform()
    assert emitted_charm == 2
    assert tribe_member_with_regular_fur.get_energy() == 99
    tribe_member_with_regular_fur.shake_composure(emitted_charm)
    assert tribe_member_with_regular_fur.get_composure() == 98


def test_tribe_member_with_tails(tribe_member_with_tails: ITribeMember) -> None:
    member = tribe_member_with_tails
    emitted_charm = member.perform()
    assert emitted_charm == 10
    assert member.get_energy() == 99
    member.shake_composure(emitted_charm)
    assert member.get_composure() == 90


def test_tribe_member_with_fur_and_tails(
    tribe_member_with_dotted_fur: ITribeMember,
) -> None:
    member = TribeMemberWithTails(tribe_member_with_dotted_fur, 3)
    emitted_charm = member.perform()
    assert emitted_charm == 15
    assert member.get_energy() == 99
    member.shake_composure(emitted_charm)
    assert member.get_composure() == 85


@pytest.fixture()
def tribe(
    tribe_member_with_tails: ITribeMember,
    tribe_member_with_dotted_fur: ITribeMember,
    tribe_member_with_regular_fur: ITribeMember,
) -> ITribeMember:
    return Tribe(
        [
            TribeMember(),
            tribe_member_with_tails,
            tribe_member_with_dotted_fur,
            tribe_member_with_regular_fur,
        ]
    )


def test_tribe_perform(tribe: ITribeMember) -> None:
    emitted_charm = tribe.perform()
    assert emitted_charm == 1 + 10 + 6 + 2


def test_tribe_get_energy(tribe: ITribeMember) -> None:
    assert tribe.get_energy() == 400
    tribe.perform()
    assert tribe.get_energy() == 396


def test_tribe_shake_composure(tribe: ITribeMember) -> None:
    emitted_charm = tribe.perform()
    tribe.shake_composure(emitted_charm)
    assert tribe.get_composure() == 381
    tribe.shake_composure(200)
    assert tribe.get_composure() == 181


def test_tribe_get_composure(tribe: ITribeMember) -> None:
    assert tribe.get_composure() == 400
    tribe.shake_composure(280)
    assert tribe.get_composure() == 120


@pytest.fixture(scope="module")
def actions() -> List[IPerformance]:
    return [
        Singing(),
        Dancing(),
        PlayingOnHorns(),
        PlayingOnMaraca(),
        PlayingOnDidgeridoo(),
    ]


@pytest.fixture(scope="module")
def full_warehouse() -> IWarehouseForInstruments:
    warehouse = WarehouseForInstruments()
    warehouse.add_new_instruments("Horn", 5)
    warehouse.add_new_instruments("maraca", 5)
    warehouse.add_new_instruments("Didgeridoo", 5)
    return warehouse


@pytest.fixture(scope="module")
def only_maracas_in_stash() -> IWarehouseForInstruments:
    warehouse = WarehouseForInstruments()
    warehouse.add_new_instruments("maracA", 5)
    return warehouse


@pytest.fixture(scope="module")
def the_most_charming_performance_picker_only_maracas(
    actions: List[IPerformance], only_maracas_in_stash: IWarehouseForInstruments
) -> IPerformancePicker:
    return TheMostCharmingPerformancePicker(actions, only_maracas_in_stash)


@pytest.fixture
def tribe_member_with_better_picker(
    the_most_charming_performance_picker_only_maracas: IPerformancePicker,
) -> ITribeMember:
    return TribeMember(
        performance_picker=the_most_charming_performance_picker_only_maracas
    )


def test_tribe_member_with_better_picker(
    tribe_member_with_better_picker: TribeMember,
) -> None:
    member = tribe_member_with_better_picker
    emitted_charm = member.perform()
    assert emitted_charm == 6
    assert member.get_energy() == 96
