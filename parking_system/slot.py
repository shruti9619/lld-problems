from parking_enums import ParkingSlotType, SlotStatus
from typing import Optional

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from vehicle import Vehicle

class Slot:
    def __init__(
        self,
        slot_id: str,
        slot_type: ParkingSlotType,
        status: SlotStatus = SlotStatus.AVAILABLE,
        vehicle: Optional["Vehicle"] = None,
    ):
        self.slot_id = slot_id
        self.slot_type = slot_type
        self.status = status
        self.occupied_duration = 0  # in hours
        self.occupied_vehicle = None
        self.vehicle = vehicle

    def occupy_slot(self):
        self.status = SlotStatus.OCCUPIED

    def vacate_slot(self):
        self.status = SlotStatus.AVAILABLE

    def get_slot_info(self):
        return {
            "slot_id": self.slot_id,
            "slot_type": self.slot_type,
            "status": self.status ,
            "occupied_duration": self.occupied_duration,
        }
