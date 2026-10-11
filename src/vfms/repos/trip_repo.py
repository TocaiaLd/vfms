# standard libs
import json

# Projects imports
from vfms.repos.repo import Repo
from vfms.models.trip import Trip

class TripRepo(Repo):
    def __init__(
        self, 
    ):
        super().__init__()
    
    def save_trip(
            self, 
            trip            : Trip,
            driver_cpf      : str,
            vehicle_plate   : str
        ):
        
        if self.database_type == "json":
            self.save_trip_json(trip, driver_cpf, vehicle_plate)
        else:
            # self.save_driver_sql(trip)
            pass

    def save_trip_json(self, trip, driver_cpf, vehicle_plate):
        with open("src/vfms/config/settings.json", "r", encoding="utf-8") as f:
            id_trip = json.load(f)
            f.close()

        with open(self.db_trips_path, "r", encoding="utf-8") as f:
            database = json.load(f)

            new_item = {
                "driver_cpf"    : driver_cpf,       
                "vehicle_plate" : vehicle_plate,
                "origin"        : trip.origin,
                "destiny"       : trip.destiny,
                "distance"      : trip.distance
            }

            database[id_trip["settings"]["last_id_trip"]] = new_item
            f.close()

        with open(self.db_trips_path, "w", encoding="utf-8") as f:
            json.dump(database, f, indent=4, ensure_ascii=False)
            f.close()

        with open("src/vfms/config/settings.json", "w", encoding="utf-8") as f:
            id_trip["settings"]["last_id_trip"] += 1
            json.dump(id_trip, f, indent=4, ensure_ascii=False)
            f.close()

    # def read_drivers_json(self):
    #     with open(self.db_driver_path, "r", encoding="utf-8") as f:
    #         database = json.load(f)

    #     list_drivers = {}

    #     for db_title, data in database.items():
    #             for cpf, data in data.items():
    #                 list_drivers[cpf] = data

    #     return list_drivers
