import logging
from vehicle import Vehicle
from parking_service import ParkingService
from parking_ticket import ParkingTicket

from typing import Optional


class ParkingEntry:
    def __init__(self, entry_id: str, parking_service: ParkingService):
        self.entry_id = entry_id
        self.parking_service = parking_service
        self.checkpoint_open = False

    def open_checkpoint(self):
        self.checkpoint_open = True

    def close_checkpoint(self):
        self.checkpoint_open = False

    def process_vehicle_entry(self, vehicle: Vehicle) -> Optional[ParkingTicket]:
        self.open_checkpoint()
        ticket = self.parking_service.park_vehicle(vehicle)
        self.close_checkpoint()

        if ticket:
            logging.info(
                f"Vehicle {vehicle.license_plate} parked in slot {ticket.slot.slot_id}."
            )
            return ticket
        else:
            logging.warning(f"No available slots for vehicle {vehicle.license_plate}.")
            return None
