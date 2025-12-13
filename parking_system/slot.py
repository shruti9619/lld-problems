from parking_enums import ParkingSlotType, SlotStatus, VehicleType
from typing import Optional


class Slot:
    def __init__(
        self,
        slot_id: str,
        slot_type: ParkingSlotType,
        status: SlotStatus = SlotStatus.AVAILABLE,
    ):
        self.slot_id = slot_id
        self.slot_type = slot_type
        self.status = status
        self.occupied_duration = 0  # Reset to 0 when vacated

    def occupy_slot(self):
        self.status = SlotStatus.OCCUPIED
        self.occupied_duration = 0

    def vacate_slot(self):
        self.status = SlotStatus.AVAILABLE
        self.occupied_duration = 0

    def is_compatible(self, vehicle_type: "VehicleType") -> bool:
        if self.slot_type == ParkingSlotType.MOTORCYCLE:
            return vehicle_type == VehicleType.SMALL
        elif self.slot_type == ParkingSlotType.COMPACT:
            return vehicle_type in [VehicleType.SMALL, VehicleType.MEDIUM]
        elif self.slot_type == ParkingSlotType.LARGE:
            return True  # Any vehicle
        elif self.slot_type == ParkingSlotType.ELECTRIC:
            return vehicle_type == VehicleType.ELECTRIC
        return False

    def get_slot_info(self):
        return {
            "slot_id": self.slot_id,
            "slot_type": self.slot_type,
            "status": self.status,
            "occupied_duration": self.occupied_duration,
        }
