from parking_enums import ParkingLotStatus, ParkingSlotType, SlotStatus
from slot import Slot
from parking_entry import ParkingEntry
from parking_exit import ParkingExit


class ParkingLot:
    def __init__(
        self,
        name: str,
        id: str,
        address: str,
        total_slots: int,
        status: ParkingLotStatus,
        entry: ParkingEntry,
        exit: ParkingExit,
    ):
        self.name = name
        self.id = id
        self.address = address
        self.total_slots = total_slots
        self.available_slots = total_slots
        self.slots: dict = self._init_parking_slots()
        self.status = status
        self.entry = entry
        self.exit = exit

    def _init_parking_slots(self) -> dict:
        slots = {}
        for i in range(self.total_slots):
            slot = Slot(
                slot_id=f"SLOT-{i + 1}",
                status=SlotStatus.AVAILABLE,
                slot_type=ParkingSlotType.REGULAR,
            )
            slots[slot.slot_id] = slot
        return slots
