import json

from vfms.repos.repo import Repo
from vfms.models.vehicles.motorcycle import Motorcycle
from vfms.models.vehicles.truck import Truck
from vfms.models.vehicles.car import Car

class VehicleRepo(Repo):
    def save_vehicle(
            self, 
            vehicle_dict : dict,
            vehicle_type : str
        ):
        
        response = None

        if self.database_type == "json":
            response = self.save_vehicle_json(vehicle_dict, vehicle_type)
        else:
            response = self.save_vehicle_sql(vehicle_dict, vehicle_type)
        
        return response

    def save_vehicle_json(self, vehicle_dict, vehicle_type):
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

    def save_vehicle_sql(self, vehicle, vehicle_type):
        print("sql")

    def show_vehicles_json(self, what):
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


                    


