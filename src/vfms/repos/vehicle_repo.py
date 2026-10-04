import json

from vfms.models.vehicles.motorcicle import Motorcicle
from vfms.models.vehicles.truck import Truck
from vfms.models.vehicles.car import Car

class VehicleRepo:
    def specific_atributtes(self, vehicle) -> dict:
        
        if isinstance(vehicle, Car):
            d = {
                "ports": vehicle.ports
            }
        elif isinstance(vehicle, Truck):
            d = {
                "max-weight": vehicle.max_weight
            }
        elif isinstance(vehicle, Motorcicle):
            d = {
                "cc":  vehicle.cc
            }

        return d
    
    
    def save_vehicle(
            self, 
            vehicle : Car | Truck | Motorcicle,
            type    : str
        ):

        with open("database.json", "r", encoding="utf-8") as f:
            database = json.load(f)

            new_item = {
                "model": vehicle.model,
                "brand": vehicle.brand,
                "year": vehicle.year,
                "mileage": vehicle.mileage,
                "average_compsumption": vehicle.average_consumption,
                "status": vehicle.status.name,
                "license_category": vehicle.license_category.name,
                "maintenance_h" : vehicle.maintenance_h
            }

            new_item.update(self.specific_atributtes(vehicle))

            database["vehicles"][type][vehicle.plate] = new_item
            f.close()

        with open("database.json", "w", encoding="utf-8") as f:
            json.dump(database, f, indent=4, ensure_ascii=False)
            f.close()
        
        print("Vehicle saved!")

    def show_all_vehicles(self):
        with open("database.json", "r", encoding="utf-8") as f:
            database = json.load(f)

        for title, data in database.items():
            if title == "vehicles":
                for vehicle, data in data.items():
                    print(data["status"])


    