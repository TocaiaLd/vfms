# standard libs
import json

# Projects imports
from vfms.repos.repo import Repo
from vfms.models.trip import Trip

class TripRepo(Repo):
    def __init__(self):
        super().__init__()
    
    def save_trip(self, trip):
        new_item = {
            "driver_cpf"    : trip.driver_cpf,       
            "vehicle_plate" : trip.vehicle_plate,
            "origin"        : trip.origin,
            "destiny"       : trip.destiny,
            "distance"      : trip.distance
        }
        
        self.save_only_trip(new_item)
        self.save_trip_on_vehicle(trip.vehicle_plate)
        self.save_trip_on_driver(trip.driver_cpf)
        self.save_trip_index_in_settings()

    def save_only_trip(self, new_item):
        with open(self.db_trips_path, "r", encoding="utf-8") as f:
            database = json.load(f)
            database[self.id_trip] = new_item
            f.close()

        with open(self.db_trips_path, "w", encoding="utf-8") as f:
            json.dump(database, f, indent=4, ensure_ascii=False)
            f.close()

    def save_trip_on_vehicle(self, plate):
        with open(self.db_vehicles_path, "r", encoding="utf-8") as f:
            database = json.load(f)

            for vehicle_type, data in database.items():
                for db_plate in data:
                    if db_plate == plate:
                        database[vehicle_type][plate]["trips"].append(self.id_trip)

            f.close()

        with open(self.db_vehicles_path, "w", encoding="utf-8") as f:
            json.dump(database, f, indent=4, ensure_ascii=False)
            f.close()

    def save_trip_on_driver(self, driver_cpf):
        with open(self.db_driver_path, "r", encoding="utf-8") as f:
            drivers_db = json.load(f)
            f.close()

        drivers_db[driver_cpf]["trip_history"].append(self.id_trip)

        with open(self.db_driver_path, "w", encoding="utf-8") as f:
            json.dump(drivers_db, f, indent=4, ensure_ascii=False)
            f.close()
    
    def save_trip_index_in_settings(self) -> None:
        with open("src/vfms/config/settings.json", "r", encoding="utf-8") as f:
            settings = json.load(f)
            self.id_trip += 1
            settings["settings"]["repository"]["last_id_trip"] = self.id_trip
            f.close()
        
        with open("src/vfms/config/settings.json", "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=4, ensure_ascii=False)
            f.close()