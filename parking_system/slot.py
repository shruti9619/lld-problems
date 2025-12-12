from parking_enums import ParkingSlotType, SlotStatus


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
        self.occupied_duration = 0  # in hours
        self.occupied_vehicle = None

    def occupy_slot(self):
        self.is_occupied = True

    def vacate_slot(self):
        self.is_occupied = False

    def get_slot_info(self):
        return {
            "slot_id": self.slot_id,
            "slot_type": self.slot_type,
            "is_occupied": self.is_occupied,
        }
