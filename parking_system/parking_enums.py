from enum import Enum


class VehicleType(Enum):
    SMALL = "Small"
    MEDIUM = "Medium"
    LARGE = "Large"
    ELECTRIC = "Electric"


class ParkingSlotType(Enum):
    MOTORCYCLE = "Motorcycle"  # Only SMALL
    COMPACT = "Compact"  # SMALL or MEDIUM
    LARGE = "Large"  # Any
    ELECTRIC = "Electric"  # ELECTRIC only


class SlotStatus(Enum):
    OCCUPIED = "Occupied"
    AVAILABLE = "Available"


class ParkingLotStatus(Enum):
    OPEN = "Open"
    FULL = "Full"


class PaymentMethod(Enum):
    CASH = "Cash"
    CREDIT_CARD = "Credit Card"
    MOBILE_PAYMENT = "Mobile Payment"
