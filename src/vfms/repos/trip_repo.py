# standard libs
import json

# Projects imports
from vfms.repos.repo import Repo
from vfms.models.trip import Trip

class TripRepo(Repo):
    def __init__(self):
        super().__init__()
    
    def save_trip(self, trip):
        if self.database_type == "json":
            self.save_trip_json(trip)
        else:
            pass

    def save_trip_json(self, trip):
        new_item = {
            "driver_cpf"    : trip.driver_cpf,       
            "vehicle_plate" : trip.vehicle_plate,
            "origin"        : trip.origin,
            "destiny"       : trip.destiny,
            "distance"      : trip.distance
        }
        
        
        self.save_only_trip_json(new_item)
        self.save_trip_on_vehicle_json(trip.vehicle_plate)
        self.save_trip_on_driver_json(trip.driver_cpf)

        with open("src/vfms/config/settings.json", "w", encoding="utf-8") as f:
            self.id_trip["settings"]["last_id_trip"] += 1
            json.dump(self.id_trip, f, indent=4, ensure_ascii=False)
            f.close()

    def save_only_trip_json(self, new_item):
        with open(self.db_trips_path, "r", encoding="utf-8") as f:
            database = json.load(f)
            database[self.id_trip["settings"]["last_id_trip"]] = new_item
            f.close()

        with open(self.db_trips_path, "w", encoding="utf-8") as f:
            json.dump(database, f, indent=4, ensure_ascii=False)
            f.close()

    def save_trip_on_vehicle_json(self, plate):
        with open(self.db_vehicles_path, "r", encoding="utf-8") as f:
            database = json.load(f)

            for vehicle_type, data in database.items():
                for db_plate in data:
                    if db_plate == plate:
                        database[vehicle_type][plate]["trips"].append(self.id_trip["settings"]["last_id_trip"])

            f.close()

        with open(self.db_vehicles_path, "w", encoding="utf-8") as f:
            json.dump(database, f, indent=4, ensure_ascii=False)
            f.close()

    def save_trip_on_driver_json(self, driver_cpf):
        with open(self.db_driver_path, "r", encoding="utf-8") as f:
            drivers_db = json.load(f)
            f.close()

        drivers_db[driver_cpf]["trip_history"].append(self.id_trip["settings"]["last_id_trip"])

        with open(self.db_driver_path, "w", encoding="utf-8") as f:
            json.dump(drivers_db, f, indent=4, ensure_ascii=False)
            f.close()