from parking_lot import ParkingLot
from parking_entry import ParkingEntry
from parking_exit import ParkingExit
from parking_enums import ParkingLotStatus


def create_parking_lot():
    entry = ParkingEntry(entry_id="ENTRY-1")
    exit = ParkingExit(exit_id="EXIT-1")
    parking_lot = ParkingLot(
        name="Downtown Parking",
        id="DL123",
        address="123 Main St, Downtown",
        total_slots=100,
        status=ParkingLotStatus.OPEN,
        entry=entry,
        exit=exit,
    )
    return parking_lot
