class ParkingEntry:
    def __init__(self, entry_id: str):
        self.entry_id = entry_id
        # self.is_available = True
        self.checkpoint_open = False

    def open_checkpoint(self):
        self.checkpoint_open = True

    def close_checkpoint(self):
        self.checkpoint_open = False

    def process_vehicle_entry(self):
        pass

    def check_availability(self):
        pass
