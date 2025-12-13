from abc import ABC, abstractmethod
from typing import Optional
from slot import Slot
from parking_lot import ParkingLot
from vehicle import VehicleType
from parking_enums import SlotStatus


class ParkingStrategy(ABC):
    @abstractmethod
    def find_available_slot(
        self, parking_lot: "ParkingLot", vehicle_type: VehicleType
    ) -> Optional[Slot]:
        pass


class NearestSpotStrategy(ParkingStrategy):
    def find_available_slot(
        self, parking_lot: "ParkingLot", vehicle_type: VehicleType
    ) -> Optional[Slot]:
        for slot in parking_lot.get_slots().values():
            if slot.status == SlotStatus.AVAILABLE and slot.is_compatible(vehicle_type):
                return slot
        return None
