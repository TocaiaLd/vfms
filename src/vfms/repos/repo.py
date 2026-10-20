import json
from vfms.config.settings import file_path

class Repo():
    def __init__(
        self, 
    ):
        self.db_vehicles_path   = "db/json/vehicles.json"
        self.db_driver_path     = "db/json/drivers.json"
        self.db_trips_path      = "db/json/trips.json"

    def get_database_type(self) -> None:
        with open(file_path, "r", encoding="utf-8") as f:
            settings = json.load(f)
            self.database_type = settings["settings"]["repository"]
            f.close()

    def get_trip_id_from_json(self) -> None:
        with open("src/vfms/config/settings.json", "r", encoding="utf-8") as f:
            self.id_trip = json.load(f)
            f.close()