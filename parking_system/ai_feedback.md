Below, I'll provide a refactored version of your Parking Lot system to **reduce coupling**, improve **extensibility**, and incorporate a **Ticket system**. I'll explain the changes clearly, focusing on how they address tight coupling, enhance design, and integrate the ticket-based approach.

### Goals of the Refactor
1. **Reduce Coupling**:
   - Introduce a `ParkingService` to mediate between gates and `ParkingLot`.
   - Use interfaces (abstract base classes) for dependency inversion.
   - Remove direct manipulation of `ParkingLot` internals by gates.
2. **Add Ticket System**:
   - Create a `ParkingTicket` class to track entry details.
   - Use tickets as the single source of truth instead of bidirectional `Vehicle` ↔ `Slot` links.
3. **Support Extensibility**:
   - Allow multiple entry/exit gates.
   - Add a basic `ParkingStrategy` for slot allocation.
   - Support different slot types for vehicle compatibility.
4. **Improve Encapsulation**:
   - Hide `ParkingLot` slot management from gates.
   - Centralize state changes (e.g., slot assignment) in `ParkingService`.

### Refactored Code

Below is the refactored code, trimmed to focus on key classes and changes. I'll omit unchanged parts (like `Vehicle` subclasses or enums unless modified) for brevity but note any updates. You can merge these with your existing code.

#### 1. Enums (Updated)
Added `COMPACT` and `LARGE` to `ParkingSlotType` for vehicle compatibility.

```python
from enum import Enum

class VehicleType(Enum):
    SMALL = "Small"
    MEDIUM = "Medium"
    LARGE = "Large"
    ELECTRIC = "Electric"

class ParkingSlotType(Enum):
    MOTORCYCLE = "Motorcycle"  # Only SMALL
    COMPACT = "Compact"        # SMALL or MEDIUM
    LARGE = "Large"            # Any
    ELECTRIC = "Electric"      # ELECTRIC only

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
```

#### 2. ParkingTicket (New)
Tracks parking details and serves as the link between vehicle, slot, and entry time.

```python
from datetime import datetime
from typing import Optional
from slot import Slot
from vehicle import Vehicle

class ParkingTicket:
    def __init__(self, ticket_id: str, vehicle: 'Vehicle', slot: 'Slot', entry_time: datetime):
        self.ticket_id = ticket_id
        self.vehicle = vehicle
        self.slot = slot
        self.entry_time = entry_time
        self.exit_time: Optional[datetime] = None

    def close_ticket(self, exit_time: datetime):
        self.exit_time = exit_time

    def get_duration_hours(self) -> float:
        if not self.exit_time:
            return 0.0
        return (self.exit_time - self.entry_time).total_seconds() / 3600

    def get_info(self):
        return {
            "ticket_id": self.ticket_id,
            "license_plate": self.vehicle.license_plate,
            "slot_id": self.slot.slot_id,
            "entry_time": self.entry_time,
            "exit_time": self.exit_time,
        }
```

#### 3. Slot (Modified)
Removed `vehicle` reference (ticket now tracks this). Added compatibility logic.

```python
from parking_enums import ParkingSlotType, SlotStatus
from typing import Optional

class Slot:
    def __init__(self, slot_id: str, slot_type: ParkingSlotType, status: SlotStatus = SlotStatus.AVAILABLE):
        self.slot_id = slot_id
        self.slot_type = slot_type
        self.status = status
        self.occupied_duration = 0  # Reset to 0 when vacated

    def occupy_slot(self):
        self.status = SlotStatus.OCCUPIED
        self.occupied_duration = 0

    def vacate_slot(self):
        self.status = SlotStatus.AVAILABLE
        self.occupied_duration = 0

    def is_compatible(self, vehicle_type: 'VehicleType') -> bool:
        if self.slot_type == ParkingSlotType.MOTORCYCLE:
            return vehicle_type == VehicleType.SMALL
        elif self.slot_type == ParkingSlotType.COMPACT:
            return vehicle_type in [VehicleType.SMALL, VehicleType.MEDIUM]
        elif self.slot_type == ParkingSlotType.LARGE:
            return True  # Any vehicle
        elif self.slot_type == ParkingSlotType.ELECTRIC:
            return vehicle_type == VehicleType.ELECTRIC
        return False

    def get_slot_info(self):
        return {
            "slot_id": self.slot_id,
            "slot_type": self.slot_type,
            "status": self.status,
            "occupied_duration": self.occupied_duration,
        }
```

#### 4. Vehicle (Modified)
Removed `parking_slot` reference (ticket tracks slot). Simplified state.

```python
from parking_enums import VehicleType

class Vehicle:
    def __init__(self, license_plate: str, vehicle_type: VehicleType):
        self.license_plate = license_plate
        self.vehicle_type = vehicle_type

    def get_vehicle_info(self):
        return {
            "license_plate": self.license_plate,
            "vehicle_type": self.vehicle_type,
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
```

#### 5. ParkingStrategy (New)
Decouples slot selection logic.

```python
from abc import ABC, abstractmethod
from typing import Optional
from slot import Slot
from parking_lot import ParkingLot
from vehicle import VehicleType

class ParkingStrategy(ABC):
    @abstractmethod
    def find_available_slot(self, parking_lot: 'ParkingLot', vehicle_type: VehicleType) -> Optional[Slot]:
        pass

class NearestSpotStrategy(ParkingStrategy):
    def find_available_slot(self, parking_lot: 'ParkingLot', vehicle_type: VehicleType) -> Optional[Slot]:
        for slot in parking_lot.get_slots().values():
            if slot.status == SlotStatus.AVAILABLE and slot.is_compatible(vehicle_type):
                return slot
        return None
```

#### 6. ParkingService (New)
Centralizes parking logic, reduces coupling.

```python
from datetime import datetime
from parking_lot import ParkingLot
from vehicle import Vehicle
from parking_strategy import ParkingStrategy
from parking_ticket import ParkingTicket
import uuid

class ParkingService:
    def __init__(self, parking_lot: 'ParkingLot', strategy: ParkingStrategy):
        self.parking_lot = parking_lot
        self.strategy = strategy
        self.tickets: dict[str, ParkingTicket] = {}

    def park_vehicle(self, vehicle: Vehicle) -> Optional[ParkingTicket]:
        if self.parking_lot.status == ParkingLotStatus.FULL:
            return None

        slot = self.strategy.find_available_slot(self.parking_lot, vehicle.vehicle_type)
        if not slot:
            self.parking_lot.status = ParkingLotStatus.FULL
            return None

        slot.occupy_slot()
        ticket = ParkingTicket(
            ticket_id=str(uuid.uuid4()),
            vehicle=vehicle,
            slot=slot,
            entry_time=datetime.now()
        )
        self.tickets[ticket.ticket_id] = ticket
        self.parking_lot.available_slots -= 1
        return ticket

    def unpark_vehicle(self, ticket_id: str, exit_time: datetime = datetime.now()) -> Optional[ParkingTicket]:
        ticket = self.tickets.get(ticket_id)
        if not ticket:
            return None

        ticket.close_ticket(exit_time)
        ticket.slot.vacate_slot()
        self.parking_lot.available_slots += 1
        self.parking_lot.status = ParkingLotStatus.OPEN
        del self.tickets[ticket_id]
        return ticket
```

#### 7. ParkingLot (Modified)
Simplified to manage slots and state. No direct gate creation.

```python
from parking_enums import ParkingLotStatus, ParkingSlotType, SlotStatus
from slot import Slot
from typing import Dict

class ParkingLot:
    def __init__(
        self,
        name: str,
        id: str,
        address: str,
        slot_distribution: Dict[ParkingSlotType, int],
        status: ParkingLotStatus = ParkingLotStatus.OPEN,
    ):
        self.name = name
        self.id = id
        self.address = address
        self.total_slots = sum(slot_distribution.values())
        self.available_slots = self.total_slots
        self.slots = self._init_parking_slots(slot_distribution)
        self.status = status

    def _init_parking_slots(self, slot_distribution: Dict[ParkingSlotType, int]) -> Dict[str, Slot]:
        slots = {}
        slot_id = 1
        for slot_type, count in slot_distribution.items():
            for _ in range(count):
                slot = Slot(
                    slot_id=f"SLOT-{slot_id}",
                    status=SlotStatus.AVAILABLE,
                    slot_type=slot_type,
                )
                slots[slot.slot_id] = slot
                slot_id += 1
        return slots

    def get_slots(self) -> Dict[str, Slot]:
        return self.slots

    def get_available_slots(self) -> list:
        return [slot for slot in self.slots.values() if slot.status == SlotStatus.AVAILABLE]
```

#### 8. ParkingEntry (Modified)
Uses `ParkingService`, not `ParkingLot`.

```python
import logging
from vehicle import Vehicle
from parking_service import ParkingService
from parking_ticket import ParkingTicket

class ParkingEntry:
    def __init__(self, entry_id: str, parking_service: ParkingService):
        self.entry_id = entry_id
        self.parking_service = parking_service
        self.checkpoint_open = False

    def open_checkpoint(self):
        self.checkpoint_open = True

    def close_checkpoint(self):
        self.checkpoint_open = False

    def process_vehicle_entry(self, vehicle: Vehicle) -> Optional[ParkingTicket]:
        self.open_checkpoint()
        ticket = self.parking_service.park_vehicle(vehicle)
        self.close_checkpoint()

        if ticket:
            logging.info(f"Vehicle {vehicle.license_plate} parked in slot {ticket.slot.slot_id}.")
            return ticket
        else:
            logging.warning(f"No available slots for vehicle {vehicle.license_plate}.")
            return None
```

#### 9. ParkingExit (Modified)
Handles payment and uses `ParkingService`.

```python
import logging
from parking_service import ParkingService
from parking_ticket import ParkingTicket
from datetime import datetime

class ParkingExit:
    def __init__(self, exit_id: str, parking_service: ParkingService):
        self.exit_id = exit_id
        self.parking_service = parking_service
        self.checkpoint_open = False

    def open_checkpoint(self):
        self.checkpoint_open = True

    def close_checkpoint(self):
        self.checkpoint_open = False

    def process_payment(self, ticket: ParkingTicket, payment_method: str) -> bool:
        duration = ticket.get_duration_hours()
        charge = 10 * duration  # $10 per hour
        logging.info(
            f"Payment of ${charge:.2f} received for vehicle {ticket.vehicle.license_plate} via {payment_method}."
        )
        return True

    def process_vehicle_exit(self, ticket_id: str, payment_method: str = "CASH") -> bool:
        ticket = self.parking_service.unpark_vehicle(ticket_id)
        if not ticket:
            logging.error(f"Ticket {ticket_id} not found.")
            return False

        if not self.process_payment(ticket, payment_method):
            logging.error(f"Payment failed for ticket {ticket_id}. Exit Denied.")
            return False

        self.open_checkpoint()
        self.close_checkpoint()
        logging.info(f"Vehicle {ticket.vehicle.license_plate} exited successfully.")
        return True
```

#### 10. Main Simulation (Updated)

```python
import logging
from parking_lot import ParkingLot
from parking_enums import ParkingLotStatus, ParkingSlotType
from parking_service import ParkingService
from parking_strategy import NearestSpotStrategy
from parking_entry import ParkingEntry
from parking_exit import ParkingExit
from vehicle import Car, Motorcycle, Truck

logging.basicConfig(level=logging.INFO)

def create_parking_lot():
    slot_distribution = {
        ParkingSlotType.MOTORCYCLE: 1,
        ParkingSlotType.COMPACT: 1,
        ParkingSlotType.LARGE: 1,
    }
    return ParkingLot(
        name="Downtown Parking",
        id="DL123",
        address="123 Main St, Downtown",
        slot_distribution=slot_distribution,
        status=ParkingLotStatus.OPEN,
    )

def create_parking_system(parking_lot):
    strategy = NearestSpotStrategy()
    service = ParkingService(parking_lot, strategy)
    entries = [ParkingEntry(f"ENTRY-{i}", service) for i in range(1, 3)]  # Multiple gates
    exits = [ParkingExit(f"EXIT-{i}", service) for i in range(1, 3)]
    return service, entries, exits

def create_vehicles():
    return [
        Car(license_plate="CAR-1234"),
        Motorcycle(license_plate="MOTO-5678"),
        Truck(license_plate="TRUCK-9012"),
    ]

def run_parking_system():
    parking_lot = create_parking_lot()
    service, entries, exits = create_parking_system(parking_lot)
    vehicles = create_vehicles()
    tickets = {}

    for vehicle in vehicles:
        entry = entries[0]  # Use first gate
        ticket = entry.process_vehicle_entry(vehicle)
        if ticket:
            tickets[vehicle.license_plate] = ticket.ticket_id

    for vehicle in vehicles:
        exit_gate = exits[0]  # Use first gate
        ticket_id = tickets.get(vehicle.license_plate)
        if ticket_id:
            exit_gate.process_vehicle_exit(ticket_id)

if __name__ == "__main__":
    run_parking_system()
```

### Explanation of Changes

1. **Ticket System**:
   - **Why**: Eliminates bidirectional `Vehicle ↔ Slot` dependency. Centralizes parking details (vehicle, slot, times).
   - **How**: `ParkingTicket` stores `ticket_id`, `vehicle`, `slot`, `entry_time`, `exit_time`. Created on entry, closed on exit.
   - **Impact**: Simplifies state management. `Vehicle` no longer needs `parking_slot`, `Slot` no longer needs `vehicle`.

2. **ParkingService**:
   - **Why**: Reduces coupling by mediating between gates and `ParkingLot`.
   - **How**: Handles `park_vehicle` and `unpark_vehicle`. Manages tickets and slot allocation via a `ParkingStrategy`.
   - **Impact**: Gates no longer directly access `ParkingLot` slots → better encapsulation. Dependency inversion (gates depend on service, not lot).

3. **ParkingStrategy**:
   - **Why**: Decouples slot selection logic.
   - **How**: Abstract `ParkingStrategy` with `NearestSpotStrategy` implementation. Can add others (e.g., LargestFirst).
   - **Impact**: Makes slot allocation extensible without changing `ParkingService`.

4. **Multiple Gates**:
   - **Why**: Real lots have multiple entry/exit points.
   - **How**: `ParkingLot` no longer creates gates. Main script creates lists of `ParkingEntry` and `ParkingExit`.
   - **Impact**: Extensible and realistic.

5. **Slot Type Compatibility**:
   - **Why**: Your original had all `REGULAR` slots, ignoring vehicle size.
   - **How**: Added `MOTORCYCLE`, `COMPACT`, `LARGE`. `Slot.is_compatible()` checks vehicle type.
   - **Impact**: Realistic slot assignment.

6. **Encapsulation**:
   - **Why**: Gates were reaching into `ParkingLot` internals.
   - **How**: `ParkingService` hides slot management. `ParkingLot.get_slots()` is internal-facing.
   - **Impact**: Cleaner boundaries, less feature envy.

7. **Time-Based Payment**:
   - **Why**: Your payment used hardcoded duration.
   - **How**: `ParkingTicket` tracks real `entry_time` and `exit_time` using `datetime`.
   - **Impact**: Realistic fee calculation.

### Coupling Impact
| Association | Original | Refactored |
|-------------|----------|------------|
| Gates ↔ ParkingLot | Tight (direct ref) | Loose (via ParkingService) |
| Vehicle ↔ Slot | Tight (bidirectional) | None (ticket mediates) |
| Slot Allocation | Hardcoded (first slot) | Loose (strategy pattern) |
| Gates | Single, hardcoded | Multiple, configurable |

- **Result**: **Much looser coupling**. Gates depend on `ParkingService` (abstraction). No direct manipulation of `ParkingLot`. Ticket system removes mutual dependencies.

### Design Impact
- **Extensibility**: Easy to add new strategies, slot types, or floors (just add a `ParkingFloor` class).
- **Single Responsibility**: Each class does one thing (e.g., `ParkingService` for ops, `Ticket` for state).
- **Dependency Inversion**: Gates depend on `ParkingService`, not concrete `ParkingLot`.
- **Real-World Modeling**: Tickets, time-based fees, and slot compatibility make it production-like.

### How to Test
Run the `run_parking_system()` script. It creates a lot with 3 slots (1 MOTORCYCLE, 1 COMPACT, 1 LARGE), parks 3 vehicles, and exits them. Check logs for slot assignments and payments.

### Next Steps
- Add `ParkingFloor` for multi-level support.
- Implement concurrent access (thread-safety) if needed.
- Add more strategies (e.g., `HandicapPriorityStrategy`).

This refactored design is now **interview-ready for mid-to-senior LLD** (even FAANG-level with minor polish). Let me know if you want to dive deeper into any part (e.g., adding floors or testing)!