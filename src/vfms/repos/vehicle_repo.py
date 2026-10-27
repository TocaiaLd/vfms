import json

from vfms.repos.repo import Repo
from vfms.models.vehicles.motorcycle import Motorcycle
from vfms.models.vehicles.truck import Truck
from vfms.models.vehicles.car import Car

class VehicleRepo(Repo):
    def update_vehicle(self, plate, update):
        with open(self.db_vehicles_path, "r", encoding="utf-8") as f:
            database = json.load(f)
        for vehicles in database.values():
            if plate in vehicles:
                vehicles[plate].update(update)
                with open(self.db_vehicles_path, "w", encoding="utf-8") as f:
                    json.dump(database, f, indent=4, ensure_ascii=False)
                return vehicles[plate]
        raise ValueError("Vehicle not found")

    def save_vehicle(
            self         : VehicleRepo, 
            vehicle_dict : dict,
            vehicle_type : str
        ):
        
        response = None

        with open(self.db_vehicles_path, "r", encoding="utf-8") as f:
            database = json.load(f)

            database[vehicle_type].update(vehicle_dict) 
            f.close()

        with open(self.db_vehicles_path, "w", encoding="utf-8") as f:
            json.dump(database, f, indent=4, ensure_ascii=False)
            f.close()
        
        response = {
            "sucess" : True,
            "message": f"{vehicle_type} saved in json!",
        }

        return response

    def show_vehicles(self, what):
        with open(self.db_vehicles_path, "r", encoding="utf-8") as f:
            database = json.load(f)

        list_vehicles = {}

        for vehicle_type, vehicles in database.items():
            if vehicles:
                if what == vehicle_type:
                    list_vehicles[what] = vehicles
                elif what == "vehicles":
                    list_vehicles[vehicle_type] = vehicles

        return list_vehicles


                    


