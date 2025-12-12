import logging

from parking_lot import ParkingLot
from parking_enums import ParkingLotStatus

logging.basicConfig(level=logging.INFO)


def create_parking_lot():
    logging.info("Creating parking lot...")
    parking_lot = ParkingLot(
        name="Downtown Parking",
        id="DL123",
        address="123 Main St, Downtown",
        total_slots=2,
        status=ParkingLotStatus.OPEN,
    )
    return parking_lot


def create_vehicles():
    logging.info("Creating vehicles...")
    from vehicle import Car, Motorcycle, Truck

    car = Car(license_plate="CAR-1234")
    motorcycle = Motorcycle(license_plate="MOTO-5678")
    truck = Truck(license_plate="TRUCK-9012")

    return [car, motorcycle, truck]


def run_parking_system():
    parking_lot = create_parking_lot()
    vehicles = create_vehicles()
    logging.info("Parking lot and vehicles created successfully.\n\n")

    for vehicle in vehicles:
        logging.info(f"Processing entry for vehicle {vehicle.license_plate}...\n")
        if parking_lot.entry.process_vehicle_entry(vehicle):
            logging.info(f"Vehicle {vehicle.license_plate} parked successfully.\n")
        else:
            logging.warning(
                f"No available slots for vehicle {vehicle.license_plate}.\n"
            )
        logging.info("\n\n")

    for vehicle in vehicles:
        logging.info(f"Processing exit for vehicle {vehicle.license_plate}...\n")
        parking_lot.exit.process_vehicle_exit(vehicle)

    logging.info("Parking system simulation completed.")


if __name__ == "__main__":
    run_parking_system()
