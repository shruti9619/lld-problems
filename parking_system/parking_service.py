from typing import Optional
from datetime import datetime
from parking_lot import ParkingLot
from vehicle import Vehicle
from parking_strategy import ParkingStrategy
from parking_ticket import ParkingTicket
from parking_enums import ParkingLotStatus
import uuid


class ParkingService:
    def __init__(self, parking_lot: "ParkingLot", strategy: ParkingStrategy):
        self.parking_lot = parking_lot
        self.strategy = strategy
        self.tickets: dict[str, ParkingTicket] = {}

    def park_vehicle(self, vehicle: Vehicle) -> Optional[ParkingTicket]:
        if self.parking_lot.status == ParkingLotStatus.FULL:
            return None

        slot = self.strategy.find_available_slot(self.parking_lot, vehicle.vehicle_type)
        if not slot:
            self.parking_lot.status = ParkingLotStatus.FULL
            return None

        slot.occupy_slot()
        ticket = ParkingTicket(
            ticket_id=str(uuid.uuid4()),
            vehicle=vehicle,
            slot=slot,
            entry_time=datetime.now(),
        )
        self.tickets[ticket.ticket_id] = ticket
        self.parking_lot.available_slots -= 1
        return ticket

    def unpark_vehicle(
        self, ticket_id: str, exit_time: datetime = datetime.now()
    ) -> Optional[ParkingTicket]:
        ticket = self.tickets.get(ticket_id)
        if not ticket:
            return None

        ticket.close_ticket(exit_time)
        ticket.slot.vacate_slot()
        self.parking_lot.available_slots += 1
        self.parking_lot.status = ParkingLotStatus.OPEN
        del self.tickets[ticket_id]
        return ticket
