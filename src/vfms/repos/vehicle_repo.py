import json

from vfms.repos.repo import Repo
from vfms.models.vehicles.motorcycle import Motorcycle
from vfms.models.vehicles.truck import Truck
from vfms.models.vehicles.car import Car

class VehicleRepo():
    def __init__(
        self    : VehicleRepo, 
        repo    : Repo
    ):
        self.repo = repo
    
    # def update_vehicle(
    #     self    : VehicleRepo, 
    #     plate   : str, 
    #     update  : 
    # ):
    #     pass

    def save_vehicle(
        self            : VehicleRepo, 
        vehicle_obj     : Car | Truck | Motorcycle,
    ):
        response = "Vehicle saved successfuly."
        
        if isinstance(vehicle_obj, Car):
            self.save_car(vehicle_obj)
        elif isinstance(vehicle_obj, Truck):
            self.save_truck(vehicle_obj)
        elif isinstance(vehicle_obj, Motorcycle):
            self.save_motorcycle(vehicle_obj)
        else:
            response = "Error to save the vehicle. Class doesn't exists"

        self.repo._con.commit()
        return response

    def save_car(
        self            : VehicleRepo, 
        vehicle_obj     : Car,
    ):
        self.repo._cursor.execute("""
INSERT INTO cars (plate, model, brand, year, mileage, average_consumption, status, max_fuel, fuel, ports, license) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""",
(vehicle_obj.plate, vehicle_obj.model, vehicle_obj.brand, vehicle_obj.year, vehicle_obj.mileage, vehicle_obj.average_consumption, vehicle_obj.status.name, vehicle_obj.max_fuel, vehicle_obj.fuel, vehicle_obj.ports, vehicle_obj.license.name)
)

    def save_truck(
        self            : VehicleRepo, 
        vehicle_obj     : Truck,
    ):
        self.repo._cursor.execute("""
INSERT INTO trucks (plate, model, brand, year, mileage, average_consumption, status, max_fuel, fuel, max_weight, license) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""",
(vehicle_obj.plate, vehicle_obj.model, vehicle_obj.brand, vehicle_obj.year, vehicle_obj.mileage, vehicle_obj.average_consumption, vehicle_obj.status.name, vehicle_obj.max_fuel, vehicle_obj.fuel, vehicle_obj.max_weight, vehicle_obj.license.name)
)

    def save_motorcycle(
        self            : VehicleRepo, 
        vehicle_obj     : Truck,
    ):
        self.repo._cursor.execute("""
INSERT INTO motorcycles (plate, model, brand, year, mileage, average_consumption, status, max_fuel, fuel, cc, license) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""",
(vehicle_obj.plate, vehicle_obj.model, vehicle_obj.brand, vehicle_obj.year, vehicle_obj.mileage, vehicle_obj.average_consumption, vehicle_obj.status.name, vehicle_obj.max_fuel, vehicle_obj.fuel, vehicle_obj.cc, vehicle_obj.license.name)
)

    def show_vehicles(self, what):
        pass


                    


