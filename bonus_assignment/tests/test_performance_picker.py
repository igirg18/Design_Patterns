from typing import List

import pytest

from app.performance import (
    Dancing,
    IPerformance,
    NoPerformance,
    PlayingOnDidgeridoo,
    PlayingOnHorns,
    PlayingOnMaraca,
    Singing,
)
from app.performance_picker import (
    DefaultPerformancePicker,
    IPerformancePicker,
    TheMostCharmingPerformancePicker,
)
from app.warehouse_for_instruments import (
    IWarehouseForInstruments,
    WarehouseForInstruments,
)


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
def only_horns_in_stash() -> IWarehouseForInstruments:
    warehouse = WarehouseForInstruments()
    warehouse.add_new_instruments("Horn", 5)
    return warehouse


@pytest.fixture(scope="module")
def only_maracas_in_stash() -> IWarehouseForInstruments:
    warehouse = WarehouseForInstruments()
    warehouse.add_new_instruments("maracA", 5)
    return warehouse


@pytest.fixture(scope="module")
def only_didgeridoos_in_stash() -> IWarehouseForInstruments:
    warehouse = WarehouseForInstruments()
    warehouse.add_new_instruments("didgeridoo", 5)
    return warehouse


@pytest.fixture(scope="module")
def full_warehouse() -> IWarehouseForInstruments:
    warehouse = WarehouseForInstruments()
    warehouse.add_new_instruments("Horn", 5)
    warehouse.add_new_instruments("maraca", 5)
    warehouse.add_new_instruments("Didgeridoo", 5)
    return warehouse


@pytest.fixture(scope="module")
def all_instrument_available_default_picker(
    actions: List[IPerformance], full_warehouse: IWarehouseForInstruments
) -> IPerformancePicker:
    return DefaultPerformancePicker(actions, full_warehouse)


@pytest.fixture(scope="module")
def only_horns_available_default_picker(
    actions: List[IPerformance], only_horns_in_stash: IWarehouseForInstruments
) -> IPerformancePicker:
    return DefaultPerformancePicker(actions, only_horns_in_stash)


@pytest.fixture(scope="module")
def only_maracas_available_default_picker(
    actions: List[IPerformance], only_maracas_in_stash: IWarehouseForInstruments
) -> IPerformancePicker:
    return DefaultPerformancePicker(actions, only_maracas_in_stash)


@pytest.fixture(scope="module")
def only_didgeridoos_available_default_picker(
    actions: List[IPerformance], only_didgeridoos_in_stash: IWarehouseForInstruments
) -> IPerformancePicker:
    return DefaultPerformancePicker(actions, only_didgeridoos_in_stash)


def test_get_available_actions_on_full_warehouse_full_energy(
    all_instrument_available_default_picker: IPerformancePicker,
    actions: List[IPerformance],
) -> None:
    available_actions = all_instrument_available_default_picker.get_available_actions(
        100
    )
    assert available_actions == actions


def test_get_available_actions_only_horns_full_energy(
    only_horns_available_default_picker: IPerformancePicker,
) -> None:
    available_actions = only_horns_available_default_picker.get_available_actions(100)
    assert available_actions == [Singing(), Dancing(), PlayingOnHorns()]


def test_get_available_actions_only_maracas_full_energy(
    only_maracas_available_default_picker: IPerformancePicker,
) -> None:
    available_actions = only_maracas_available_default_picker.get_available_actions(100)
    assert available_actions == [Singing(), Dancing(), PlayingOnMaraca()]


def test_get_available_actions_only_didgeridoos_full_energy(
    only_didgeridoos_available_default_picker: IPerformancePicker,
) -> None:
    available_actions = only_didgeridoos_available_default_picker.get_available_actions(
        100
    )
    assert available_actions == [Singing(), Dancing(), PlayingOnDidgeridoo()]


def test_get_available_actions_modifying_energy_case(
    all_instrument_available_default_picker: IPerformancePicker,
) -> None:
    available_instruments = (
        all_instrument_available_default_picker.get_available_actions(80)
    )
    assert available_instruments == [
        Singing(),
        Dancing(),
        PlayingOnHorns(),
        PlayingOnMaraca(),
        PlayingOnDidgeridoo(),
    ]
    available_instruments = (
        all_instrument_available_default_picker.get_available_actions(60)
    )
    assert available_instruments == [
        Singing(),
        Dancing(),
        PlayingOnHorns(),
        PlayingOnMaraca(),
    ]

    available_instruments = (
        all_instrument_available_default_picker.get_available_actions(40)
    )
    assert available_instruments == [Singing(), Dancing(), PlayingOnHorns()]

    available_instruments = (
        all_instrument_available_default_picker.get_available_actions(20)
    )
    assert available_instruments == [Singing(), Dancing()]

    available_instruments = (
        all_instrument_available_default_picker.get_available_actions(1)
    )
    assert available_instruments == [Singing()]

    available_instruments = (
        all_instrument_available_default_picker.get_available_actions(0)
    )
    assert available_instruments == []


@pytest.fixture(scope="module")
def the_most_charming_performance_picker_all_instrumnets(
    actions: List[IPerformance], full_warehouse: IWarehouseForInstruments
) -> IPerformancePicker:
    return TheMostCharmingPerformancePicker(actions, full_warehouse)


@pytest.fixture(scope="module")
def the_most_charming_performance_picker_only_maracas(
    actions: List[IPerformance], only_maracas_in_stash: IWarehouseForInstruments
) -> IPerformancePicker:
    return TheMostCharmingPerformancePicker(actions, only_maracas_in_stash)


def test_pick_performance_on_default_picker(
    all_instrument_available_default_picker: IPerformancePicker,
) -> None:
    assert all_instrument_available_default_picker.pick_performance(100) == Singing()
    assert (
        all_instrument_available_default_picker.pick_performance(0) == NoPerformance()
    )


def test_pick_performance_on_charming_picker(
    the_most_charming_performance_picker_all_instrumnets: IPerformancePicker,
) -> None:
    assert (
        the_most_charming_performance_picker_all_instrumnets.pick_performance(100)
        == PlayingOnDidgeridoo()
    )
    assert (
        the_most_charming_performance_picker_all_instrumnets.pick_performance(45)
        == PlayingOnHorns()
    )
    assert (
        the_most_charming_performance_picker_all_instrumnets.pick_performance(10)
        == Singing()
    )


def test_pick_performance_on_charming_picker_only_maracas_available(
    the_most_charming_performance_picker_only_maracas: IPerformancePicker,
) -> None:
    assert (
        the_most_charming_performance_picker_only_maracas.pick_performance(100)
        == PlayingOnMaraca()
    )
    assert (
        the_most_charming_performance_picker_only_maracas.pick_performance(40)
        == Dancing()
    )
