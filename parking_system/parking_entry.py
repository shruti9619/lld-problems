import logging

from vehicle import Vehicle
from random import randint


class ParkingEntry:
    def __init__(self, entry_id: str, parking_lot=None):
        self.entry_id = entry_id
        # self.is_available = True
        self.parking_lot = parking_lot
        self.checkpoint_open = False

    def open_checkpoint(self):
        self.checkpoint_open = True

    def close_checkpoint(self):
        self.checkpoint_open = False

    def process_vehicle_entry(self, vehicle: Vehicle):
        available_slots = self.parking_lot.get_available_slots()
        if not available_slots:
            return False
        else:
            self.open_checkpoint()
            slot = available_slots[0]
            slot.vehicle = vehicle
            slot.occupy_slot()
            vehicle.assign_parking_slot(slot)
            self.close_checkpoint()

            logging.info("Available slots after parking:")
            for slot in available_slots:
                print(slot.get_slot_info())
            return True
        return False
