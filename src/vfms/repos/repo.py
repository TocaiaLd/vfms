import json

class Repo():
    def __init__(
        self, 
    ):
        self.db_vehicles_path   = "db/json/vehicles.json"
        self.db_driver_path     = "db/json/drivers.json"
        self.db_trips_path      = "db/json/trips.json"
        self.id_trip       = self.get_trip_id_from_json()

    def get_trip_id_from_json(self) -> int:
        with open("src/vfms/config/settings.json", "r", encoding="utf-8") as f:
            trips = json.load(f)
            last_id_trip = trips["settings"]["repository"]["last_id_trip"]
            f.close()
            return last_id_trip