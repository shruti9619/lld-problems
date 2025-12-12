from enum import Enum

class VehicleType(Enum):
    SMALL = "Small"
    MEDIUM = "Medium"
    LARGE = "Large"
    ELECTRIC = "Electric"


class ParkingSlotType(Enum):
    REGULAR = "Regular"
    ELECTRIC = "Electric"

class PaymentMethod(Enum):
    CASH = "Cash"
    CREDIT_CARD = "Credit Card"
    MOBILE_PAYMENT = "Mobile Payment"

class SlotStatus(Enum):
    OCCUPIED = "Occupied"
    AVAILABLE = "Available"

class ParkingLotStatus(Enum):
    OPEN = "Open"
    FULL = "Full"



