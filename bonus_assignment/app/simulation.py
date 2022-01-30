import random
from typing import Dict

from app.fur import DottedFur, Ifur, RegularFur, StrippedFur
from app.performance_picker import TheMostCharmingPerformancePicker
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

instrument_mapping = {1: "horn", 2: "maraca", 3: "didgeridoo"}
fur_mapping: Dict[int, Ifur] = {1: RegularFur(), 2: StrippedFur(), 3: DottedFur()}


def generate_random_member(warehouse: IWarehouseForInstruments) -> ITribeMember:
    member: ITribeMember = TribeMember(
        performance_picker=TheMostCharmingPerformancePicker(
            instruments_warehouse=warehouse
        )
    )
    want_fur = bool(random.getrandbits(1))
    log_str = f"Generated Member With Following Characteristics: Energy: {member.get_energy()}; Composure: {member.get_composure()} "
    if want_fur:
        fur_id = random.randint(1, 3)
        member = TribeMemberWithFur(member, fur_mapping[fur_id])
        log_str += f"Fur: {fur_mapping[fur_id].name}; "
    want_tail = bool(random.getrandbits(1))
    if want_tail:
        tails = random.randint(1, 3)
        member = TribeMemberWithTails(member, tails)
        log_str += f"Tails: {tails} "
    print(log_str)
    return member


def generate_random_instrument_warehouse() -> IWarehouseForInstruments:
    instruments_count = random.randint(1, 15)
    tribe_warehouse = WarehouseForInstruments()
    for bla in range(1, instruments_count):
        instrument_id = random.randint(1, 3)
        tribe_warehouse.add_new_instruments(instrument_mapping[instrument_id], 1)
    return tribe_warehouse


def generate_random_tribe() -> ITribeMember:
    tribe_members_num = random.randint(1, 5)
    tribe_warehouse = generate_random_instrument_warehouse()
    print(tribe_warehouse)
    members = []
    for blu in range(0, tribe_members_num):
        members.append(generate_random_member(tribe_warehouse))
    return Tribe(members)


def simulate() -> None:
    print("starting to generate host tribe... \n=========")
    host_tribe = generate_random_tribe()
    print("\nstarting to generate guest tribe... \n===========")
    guest_tribe = generate_random_tribe()
    while True:
        if host_tribe.get_composure() <= 0:
            print("Guests have charmed Hosts")
            break
        if guest_tribe.get_energy() <= 0:
            print("Hosts have dissapointed guests")
            break
        emitted_charm = guest_tribe.perform()
        host_tribe.shake_composure(emitted_charm)


for i in range(1, 100):
    print("\n\nStarting Simulation #" + str(i))
    simulate()
