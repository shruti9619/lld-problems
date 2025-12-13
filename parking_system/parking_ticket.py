from datetime import datetime
from typing import Optional
from slot import Slot
from vehicle import Vehicle


class ParkingTicket:
    def __init__(
        self, ticket_id: str, vehicle: "Vehicle", slot: "Slot", entry_time: datetime
    ):
        self.ticket_id = ticket_id
        self.vehicle = vehicle
        self.slot = slot
        self.entry_time = entry_time
        self.exit_time: Optional[datetime] = None

    def close_ticket(self, exit_time: datetime):
        self.exit_time = exit_time

    def get_duration_hours(self) -> float:
        if not self.exit_time:
            return 0.0
        return (self.exit_time - self.entry_time).total_seconds() / 3600

    def get_info(self):
        return {
            "ticket_id": self.ticket_id,
            "license_plate": self.vehicle.license_plate,
            "slot_id": self.slot.slot_id,
            "entry_time": self.entry_time,
            "exit_time": self.exit_time,
        }
