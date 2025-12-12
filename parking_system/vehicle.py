from parking_enums import VehicleType
from slot import Slot


class Vehicle:
    def __init__(self, license_plate: str, vehicle_type: VehicleType):
        self.license_plate = license_plate
        self.vehicle_type = vehicle_type
        self.is_parked = False

    def assign_parking_slot(self, parking_slot: Slot):
        self.is_parked = True
        self.parking_slot = parking_slot

    def remove_from_parking_slot(self):
        self.is_parked = False
        old_slot = self.parking_slot
        self.parking_slot = None
        return old_slot

    def get_vehicle_info(self):
        return {
            "license_plate": self.license_plate,
            "vehicle_type": self.vehicle_type,
            "is_parked": self.is_parked,
            "parking_slot_id": self.parking_slot.slot_id if self.is_parked else "N/A",
        }


class Car(Vehicle):
    def __init__(self, license_plate: str):
        super().__init__(license_plate, VehicleType.MEDIUM)


class Motorcycle(Vehicle):
    def __init__(self, license_plate: str):
        super().__init__(license_plate, VehicleType.SMALL)


class Truck(Vehicle):
    def __init__(self, license_plate: str):
        super().__init__(license_plate, VehicleType.LARGE)

