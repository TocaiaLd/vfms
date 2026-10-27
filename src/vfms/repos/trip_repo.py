# standard libs
import json

# Projects imports
from vfms.repos.repo import Repo
from vfms.models.trip import Trip

class TripRepo(Repo):
    def __init__(self):
        super().__init__()
    
    def save_trip(self, trip):
        # Validate both resources before writing any file, so a rejected
        # allocation never leaves partial trip history behind.
        with open(self.db_vehicles_path, "r", encoding="utf-8") as f:
            vehicles = json.load(f)
        with open(self.db_driver_path, "r", encoding="utf-8") as f:
            drivers = json.load(f)
        driver = drivers.get(str(trip.driver_cpf))
        vehicle_record = next(((kind, plate, data) for kind, items in vehicles.items()
                               for plate, data in items.items()
                               if plate == trip.vehicle_plate), None)
        if driver is None:
            raise ValueError("Driver not found")
        if vehicle_record is None:
            raise ValueError("Vehicle not found")
        kind, plate, vehicle = vehicle_record
        if driver.get("status") != "AVAILABLE":
            raise ValueError("Driver is unavailable for allocation")
        if vehicle.get("status") != "AVAILABLE":
            raise ValueError("Vehicle is unavailable for allocation")
        if not self.license_allows(driver.get("license"), vehicle.get("license_category")):
            raise ValueError("Driver's license is incompatible with the vehicle category")

        new_item = {
            "driver_cpf"    : trip.driver_cpf,       
            "vehicle_plate" : trip.vehicle_plate,
            "origin"        : trip.origin,
            "destiny"       : trip.destiny,
            "distance"      : trip.distance
        }
        
        self.save_only_trip(new_item)
        vehicle["trips"].append(self.id_trip)
        vehicle["status"] = "ON_TRIP"
        driver["trip_history"].append(self.id_trip)
        driver["status"] = "ON_TRIP"
        with open(self.db_vehicles_path, "w", encoding="utf-8") as f:
            json.dump(vehicles, f, indent=4, ensure_ascii=False)
        with open(self.db_driver_path, "w", encoding="utf-8") as f:
            json.dump(drivers, f, indent=4, ensure_ascii=False)
        self.save_trip_index_in_settings()

    @staticmethod
    def license_allows(driver_license, vehicle_license):
        """CNH category coverage; D also covers B, AD covers A/B/D."""
        coverage = {"A": {"A"}, "B": {"B"}, "D": {"B", "D"},
                    "AB": {"A", "B"}, "AD": {"A", "B", "D"}}
        return vehicle_license in coverage.get(driver_license, set())

    def finish_trip(self, trip_id):
        with open(self.db_trips_path, "r", encoding="utf-8") as f:
            trips = json.load(f)
        trip = trips.get(str(trip_id))
        if trip is None:
            raise ValueError("Trip not found")
        with open(self.db_driver_path, "r", encoding="utf-8") as f:
            drivers = json.load(f)
        with open(self.db_vehicles_path, "r", encoding="utf-8") as f:
            vehicles = json.load(f)
        drivers[str(trip["driver_cpf"])]["status"] = "AVAILABLE"
        for items in vehicles.values():
            vehicle = items.get(trip["vehicle_plate"])
            if vehicle:
                vehicle["status"] = "AVAILABLE"
                break
        for path, data in ((self.db_driver_path, drivers), (self.db_vehicles_path, vehicles)):
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

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
