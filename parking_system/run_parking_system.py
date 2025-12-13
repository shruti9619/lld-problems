import logging
from parking_lot import ParkingLot
from parking_enums import ParkingLotStatus, ParkingSlotType
from parking_service import ParkingService
from parking_strategy import NearestSpotStrategy
from parking_entry import ParkingEntry
from parking_exit import ParkingExit
from vehicle import Car, Motorcycle, Truck

logging.basicConfig(level=logging.INFO)


def create_parking_lot():
    slot_distribution = {
        ParkingSlotType.MOTORCYCLE: 1,
        ParkingSlotType.COMPACT: 1,
        ParkingSlotType.LARGE: 0,
    }
    return ParkingLot(
        name="Downtown Parking",
        id="DL123",
        address="123 Main St, Downtown",
        slot_distribution=slot_distribution,
        status=ParkingLotStatus.OPEN,
    )


def create_parking_system(parking_lot):
    strategy = NearestSpotStrategy()
    service = ParkingService(parking_lot, strategy)
    entries = [
        ParkingEntry(f"ENTRY-{i}", service) for i in range(1, 3)
    ]  # Multiple gates
    exits = [ParkingExit(f"EXIT-{i}", service) for i in range(1, 3)]
    return service, entries, exits


def create_vehicles():
    return [
        Car(license_plate="CAR-1234"),
        Motorcycle(license_plate="MOTO-5678"),
        Truck(license_plate="TRUCK-9012"),
    ]


def run_parking_system():
    parking_lot = create_parking_lot()
    service, entries, exits = create_parking_system(parking_lot)
    vehicles = create_vehicles()
    tickets = {}

    for vehicle in vehicles:
        entry = entries[0]  # Use first gate
        ticket = entry.process_vehicle_entry(vehicle)
        if ticket:
            tickets[vehicle.license_plate] = ticket.ticket_id

    for vehicle in vehicles:
        exit_gate = exits[0]  # Use first gate
        ticket_id = tickets.get(vehicle.license_plate)
        if ticket_id:
            exit_gate.process_vehicle_exit(ticket_id)


if __name__ == "__main__":
    run_parking_system()
