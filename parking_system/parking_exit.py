import logging
from parking_service import ParkingService
from parking_ticket import ParkingTicket


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

    def process_vehicle_exit(
        self, ticket_id: str, payment_method: str = "CASH"
    ) -> bool:
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
