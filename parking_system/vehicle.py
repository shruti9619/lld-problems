from abc import ABC, abstractmethod
from parking_enums import VehicleType


class Vehicle(ABC):
    def __init__(self, license_plate: str, vehicle_type: VehicleType):
        self.license_plate = license_plate
        self.vehicle_type = vehicle_type
        self.is_parked = False
        self.parking_slot_id = None

    @abstractmethod
    def assign_parking_slot(self, parking_slot):
        pass

    @abstractmethod
    def remove_from_parking_slot(self):
        pass

    @abstractmethod
    def get_vehicle_info(self):
        pass


class Car(Vehicle):
    def __init__(self, license_plate: str):
        super().__init__(license_plate, VehicleType.MEDIUM)

    def assign_parking_slot(self, parking_slot):
        self.is_parked = True
        self.parking_slot_id = parking_slot.slot_id

    def remove_from_parking_slot(self):
        self.is_parked = False
        self.parking_slot_id = None

    def get_vehicle_info(self):
        return {
            "license_plate": self.license_plate,
            "vehicle_type": self.vehicle_type,
            "is_parked": self.is_parked,
            "parking_slot_id": self.parking_slot_id,
        }


class Motorcycle(Vehicle):
    def __init__(self, license_plate: str):
        super().__init__(license_plate, VehicleType.SMALL)

    def assign_parking_slot(self, parking_slot):
        self.is_parked = True
        self.parking_slot_id = parking_slot.slot_id

    def remove_from_parking_slot(self):
        self.is_parked = False
        self.parking_slot_id = None

    def get_vehicle_info(self):
        return {
            "license_plate": self.license_plate,
            "vehicle_type": self.vehicle_type,
            "is_parked": self.is_parked,
            "parking_slot_id": self.parking_slot_id,
        }


class Truck(Vehicle):
    def __init__(self, license_plate: str):
        super().__init__(license_plate, VehicleType.LARGE)

    def assign_parking_slot(self, parking_slot):
        self.is_parked = True
        self.parking_slot_id = parking_slot.slot_id

    def remove_from_parking_slot(self):
        self.is_parked = False
        self.parking_slot_id = None

    def get_vehicle_info(self):
        return {
            "license_plate": self.license_plate,
            "vehicle_type": self.vehicle_type,
            "is_parked": self.is_parked,
            "parking_slot_id": self.parking_slot_id,
        }
