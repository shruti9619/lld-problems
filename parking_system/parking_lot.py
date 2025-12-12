from parking_enums import ParkingLotStatus
from slot import Slot

class ParkingLot:
    def __init__(self, name:str, id: str, address: str, total_slots: int, status: ParkingLotStatus):
        self.name = name
        self.id = id
        self.total_slots = total_slots
        self.available_slots = total_slots
        self.slots = []
        self.status = status

    

    

    