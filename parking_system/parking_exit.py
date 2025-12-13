import logging
from vehicle import Vehicle


class ParkingExit:
    def __init__(self, exit_id: str, parking_lot=None):
        self.exit_id = exit_id
        self.is_available = True
        self.checkpoint_open = False
        self.parking_lot = parking_lot

    def open_checkpoint(self):
        self.checkpoint_open = True

    def close_checkpoint(self):
        self.checkpoint_open = False

    def process_payment(self, vehicle: Vehicle, payment_method: str):
        vehicle_info = vehicle.get_vehicle_info()
        logging.info(f"Processing {payment_method} payment for vehicle {vehicle_info}")
        # Process payment logic here
        charge = 10 * vehicle.parking_slot.occupied_duration  # Dummy charge
        logging.info(
            f"Payment of ${charge} received for vehicle {vehicle.license_plate} via {payment_method}."
        )
        return True

    def process_vehicle_exit(self, vehicle: Vehicle):
        vehicle_lookup = self.parking_lot.search_vehicle(vehicle.license_plate)
        if not vehicle_lookup:
            print(f"Vehicle {vehicle.license_plate} not found in the parking lot.")
            return

        if self.process_payment(vehicle, payment_method="CASH"):
            logging.info(f"Exit Authorized for vehicle {vehicle.license_plate}.")
        else:
            logging.error(
                f"Payment failed for vehicle {vehicle.license_plate}. Exit Denied."
            )
            return

        self.open_checkpoint()

        old_slot = vehicle.remove_from_parking_slot()
        old_slot.vacate_slot()

        self.close_checkpoint()
        logging.info(f"Vehicle {vehicle.license_plate} exited successfully.\n")

        logging.info("Available slots after exit:")
        for slot in self.parking_lot.get_available_slots():
            print(slot.get_slot_info())
