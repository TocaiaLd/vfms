import json

from vfms.repos.repo import Repo
from vfms.models.vehicles.motorcycle import Motorcycle
from vfms.models.vehicles.truck import Truck
from vfms.models.vehicles.car import Car

class VehicleRepo(Repo):
    def specific_atributtes(self, vehicle) -> dict:
        
        if isinstance(vehicle, Car):
            d = {
                "ports": vehicle.ports
            }
        elif isinstance(vehicle, Truck):
            d = {
                "max_weight": vehicle.max_weight
            }
        elif isinstance(vehicle, Motorcycle):
            d = {
                "cc":  vehicle.cc
            }

        return d
    
    def save_vehicle(
            self, 
            vehicle : Car | Truck | Motorcycle,
        ):
        
        response = None

        if self.database_type == "json":
            response = self.save_vehicle_json(vehicle)
        else:
            response = self.save_vehicle_sql(vehicle)
        
        return response

    def save_vehicle_json(self, vehicle):
        with open(self.db_vehicles_path, "r", encoding="utf-8") as f:
            database = json.load(f)

            new_item = {
                "model"                 : vehicle.model,
                "brand"                 : vehicle.brand,
                "year"                  : vehicle.year,
                "mileage"               : vehicle.mileage,
                "average_consumption"   : vehicle.average_consumption,
                "status"                : vehicle.status.name,
                "license_category"      : vehicle.license_category.name,
                "maintenance_h"         : vehicle.maintenance_h,
                "trips"                 : vehicle.trips,
                "fuel"                  : vehicle.fuel
            }

            new_item.update(self.specific_atributtes(vehicle))

            database[vehicle.__class__.__name__][vehicle.plate] = new_item
            f.close()

        with open(self.db_vehicles_path, "w", encoding="utf-8") as f:
            json.dump(database, f, indent=4, ensure_ascii=False)
            f.close()
        
        response = {
            "sucess" : True,
            "message": f"{vehicle.__class__.__name__} of plate {vehicle.plate} saved!",
        }

        return response

    def save_vehicle_sql(self, vehicl):
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


                    


