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
    ):
        self.name = name
        self.id = id
        self.address = address
        self.total_slots = total_slots
        self.available_slots = total_slots
        self.slots: dict = self._init_parking_slots()
        self.status = status
        self.entry = ParkingEntry(entry_id="ENTRY-1", parking_lot=self)
        self.exit = ParkingExit(exit_id="EXIT-1", parking_lot=self)

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
    
    def get_available_slots(self) -> list:
        available_slots = [
            slot for slot in self.slots.values() if slot.status == SlotStatus.AVAILABLE
        ]
        return available_slots
    
    def search_vehicle(self, license_plate: str):
        for slot in self.slots.values():
            if slot.vehicle and slot.vehicle.license_plate == license_plate:
                return True
        return False
