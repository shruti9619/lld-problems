class ParkingExit:
    def __init__(self, exit_id: str):
        self.exit_id = exit_id
        self.is_available = True
        self.checkpoint_open = False

    def open_checkpoint(self):
        self.checkpoint_open = True
    
    def close_checkpoint(self):
        self.checkpoint_open = False

    def process_payment(self, vehicle, payment_method):
        pass
    
    def process_vehicle_exit(self, vehicle):
        pass