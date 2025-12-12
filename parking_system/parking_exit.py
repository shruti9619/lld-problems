from vehicle import Vehicle


class ParkingExit:
    def __init__(self, exit_id: str):
        self.exit_id = exit_id
        self.is_available = True
        self.checkpoint_open = False

    def open_checkpoint(self):
        self.checkpoint_open = True

    def close_checkpoint(self):
        self.checkpoint_open = False

    def process_payment(self, vehicle: Vehicle, payment_method: str):
        vehicle_info = vehicle.get_vehicle_info()
        print(f"Processing {payment_method} payment for vehicle {vehicle_info}")
        # Process payment logic here
        charge = 10  # Dummy charge
        return charge

    def process_vehicle_exit(self, vehicle: Vehicle):
        old_slot = vehicle.remove_from_parking_slot()
        old_slot.vacate_slot()
        old_slot.vehicle = None

        self.process_payment(vehicle, payment_method="CASH")

        self.open_checkpoint()
        print(f"Vehicle {vehicle.license_plate} has exited through exit {self.exit_id  }.")
        self.close_checkpoint()


        
