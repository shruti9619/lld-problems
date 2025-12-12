from vehicle import Vehicle
from random import randint

class ParkingEntry:
    def __init__(self, entry_id: str):
        self.entry_id = entry_id
        # self.is_available = True
        self.checkpoint_open = False

    def open_checkpoint(self):
        self.checkpoint_open = True

    def close_checkpoint(self):
        self.checkpoint_open = False

    def process_vehicle_entry(self, vehicle: Vehicle):
        available_slots = self.check_availability()
        if not available_slots:
            return False
        else:
            self.open_checkpoint()
            slot = available_slots[0]
            slot.vehicle = vehicle
            slot.occupy_slot()
            vehicle.assign_parking_slot(slot)
            self.close_checkpoint()
            return True

    def check_availability(self) -> list:
        return [randint(1,100)]
