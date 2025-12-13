from parking_enums import ParkingLotStatus, ParkingSlotType, SlotStatus
from slot import Slot
from typing import Dict


class ParkingLot:
    def __init__(
        self,
        name: str,
        id: str,
        address: str,
        slot_distribution: Dict[ParkingSlotType, int],
        status: ParkingLotStatus = ParkingLotStatus.OPEN,
    ):
        self.name = name
        self.id = id
        self.address = address
        self.total_slots = sum(slot_distribution.values())
        self.available_slots = self.total_slots
        self.slots = self._init_parking_slots(slot_distribution)
        self.status = status

    def _init_parking_slots(
        self, slot_distribution: Dict[ParkingSlotType, int]
    ) -> Dict[str, Slot]:
        slots = {}
        slot_id = 1
        for slot_type, count in slot_distribution.items():
            for _ in range(count):
                slot = Slot(
                    slot_id=f"SLOT-{slot_id}",
                    status=SlotStatus.AVAILABLE,
                    slot_type=slot_type,
                )
                slots[slot.slot_id] = slot
                slot_id += 1
        return slots

    def get_slots(self) -> Dict[str, Slot]:
        return self.slots

    def get_available_slots(self) -> list:
        return [
            slot for slot in self.slots.values() if slot.status == SlotStatus.AVAILABLE
        ]
