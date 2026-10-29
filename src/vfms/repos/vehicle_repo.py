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

    def save_car(
        self            : VehicleRepo, 
        vehicle_obj     : Car,
    ):
        self.repo._cursor.execute("SELECT * FROM cars WHERE plate = ?", (vehicle_obj.plate,))
        search_result = self.repo._cursor.fetchone()

        if not search_result:
            self.repo._cursor.execute("INSERT INTO cars (plate, model, brand, year, mileage, average_consumption, status, max_fuel, fuel, ports, license) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (vehicle_obj.plate, vehicle_obj.model, vehicle_obj.brand, vehicle_obj.year, vehicle_obj.mileage, vehicle_obj.average_consumption, vehicle_obj.status.name, vehicle_obj.max_fuel, vehicle_obj.fuel, vehicle_obj.ports, vehicle_obj.license.name))
            self.repo._con.commit()

            return "Vehicle saved successfuly"

        return f"Already exists a Vehicle with the {vehicle_obj.plate} plate"

    def save_truck(
        self            : VehicleRepo, 
        vehicle_obj     : Truck,
    ):
        self.repo._cursor.execute("SELECT * FROM trucks WHERE plate = ?", (vehicle_obj.plate,))
        search_result = self.repo._cursor.fetchone()

        if not search_result:
            self.repo._cursor.execute("INSERT INTO trucks (plate, model, brand, year, mileage, average_consumption, status, max_fuel, fuel, max_weight, license) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",(vehicle_obj.plate, vehicle_obj.model, vehicle_obj.brand, vehicle_obj.year, vehicle_obj.mileage, vehicle_obj.average_consumption, vehicle_obj.status.name, vehicle_obj.max_fuel, vehicle_obj.fuel, vehicle_obj.max_weight, vehicle_obj.license.name))
            self.repo._con.commit()

            return "Vehicle saved successfuly"

        return f"Already exists a Vehicle with the {vehicle_obj.plate} plate"

    def save_motorcycle(
        self            : VehicleRepo, 
        vehicle_obj     : Truck,
    ):
        self.repo._cursor.execute("SELECT * FROM trucks WHERE plate = ?", (vehicle_obj.plate,))
        search_result = self.repo._cursor.fetchone()
        
        if not search_result:
            self.repo._cursor.execute("INSERT INTO motorcycles (plate, model, brand, year, mileage, average_consumption, status, max_fuel, fuel, cc, license) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",(vehicle_obj.plate, vehicle_obj.model, vehicle_obj.brand, vehicle_obj.year, vehicle_obj.mileage, vehicle_obj.average_consumption, vehicle_obj.status.name, vehicle_obj.max_fuel, vehicle_obj.fuel, vehicle_obj.cc, vehicle_obj.license.name))
            self.repo._con.commit()

            return "Vehicle saved successfuly"
        
        return f"Already exists a Vehicle with the {vehicle_obj.plate} plate"

    def show_cars(self):
        self.repo._cursor.execute(f"SELECT * from cars")
        list_vehicles = self.repo._cursor.fetchall()

        return list_vehicles
    
    def show_trucks(self):
        self.repo._cursor.execute(f"SELECT * from trucks")
        list_vehicles = self.repo._cursor.fetchall()

        return list_vehicles

    def show_motorcycles(self):
        self.repo._cursor.execute(f"SELECT * from motorcycles")
        list_vehicles = self.repo._cursor.fetchall()

        return list_vehicles

    def delete_car(self, plate):
        self.repo._cursor.execute("SELECT * FROM cars WHERE plate = ?", (plate,))
        search_result = self.repo._cursor.fetchone()

        if not search_result:
            return "This car plate doesn't exists"

        self.repo._cursor.execute("DELETE FROM cars WHERE plate = ?", (plate,))
        self.repo._con.commit()

        return f"The car with plate {plate} was deleted"
    
    def delete_truck(self, plate):
        self.repo._cursor.execute("SELECT * FROM trucks WHERE plate = ?", (plate,))
        search_result = self.repo._cursor.fetchone()

        if not search_result:
            return "This truck plate doesn't exists"

        self.repo._cursor.execute("DELETE FROM trucks WHERE plate = ?", (plate,))
        self.repo._con.commit()

        return f"The truck with plate {plate} was deleted."

    def delete_motorcycles(self, plate):
        self.repo._cursor.execute("SELECT * FROM motorcycles WHERE plate = ?", (plate,))
        search_result = self.repo._cursor.fetchone()

        if not search_result:
            return "This motorcycle plate doesn't exists"

        self.repo._cursor.execute("DELETE FROM motorcycles WHERE plate = ?", (plate,))
        self.repo._con.commit()

        return f"The motorcycle with plate {plate} was deleted."
                    


