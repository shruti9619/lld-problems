from abc import ABC, abstractmethod
from parking_enums import VehicleType

class Vehicle(ABC):
    def __init__(self, license_plate: str, vehicle_type: VehicleType):
        self.license_plate = license_plate
        self.vehicle_type = vehicle_type
        self.is_parked = False
        self.parking_slot = None
    
    @abstractmethod
    def assign_parking_slot(self, parking_slot):
        pass

    @abstractmethod
    def remove_from_parking_slot(self):
        pass

    @abstractmethod
    def get_vehicle_info(self):
        pass

    
