# External libs
from tabulate import tabulate

# Project dependencies
from vfms.repos.vehicles.motorcycle_repo import MotorcycleRepo
from vfms.models.vehicles.motorcycle import Motorcycle
from vfms.enums.vehicle_license import VehicleLicense

class MotorcycleController:
    def __init__(
        self    : MotorcycleController, 
        repo    : MotorcycleRepo
    ):
        self.repo = repo

    def create_motorcycle(self, request) -> str:
        motorcycle = Motorcycle(
            plate               = request["plate"],
            model               = request["model"],  
            brand               = request["brand"],  
            year                = request["year"],
            mileage             = request["mileage"],
            average_consumption = request["average_consumption"],
            status              = request["status"],
            max_fuel            = request["max_fuel"],
            fuel                = request["fuel"],
            cc                  = request["cc"],
            license             = VehicleLicense.A,
        )
       
        response = self.repo.save_motorcycle(motorcycle)
        
        return response
    
    def show_motorcycles(self) -> str:
        response = self.repo.show_motorcycles()
        
        collumns = ["Plate", "Model", "Brand", "Year", "Mileage", "Consumption", "Status", "Max Fuel", "Fuel", "CC", "License"]
        data = []

        for motorcycle in response:
            data.append(motorcycle)

        response = tabulate(data, headers=collumns, tablefmt="fancy_grid")
        
        return response
    
    def get_by_plate(self, plate) -> Motorcycle | False:
        vehicle = self.repo.get_by_plate(plate)
        
        if vehicle:
            motorcycle = Motorcycle(
                plate               = vehicle[0],
                model               = vehicle[1],  
                brand               = vehicle[2],  
                year                = vehicle[3],
                mileage             = vehicle[4],
                average_consumption = vehicle[5],
                status              = vehicle[6],
                max_fuel            = vehicle[7],
                fuel                = vehicle[8],
                cc                  = vehicle[9],
                license             = VehicleLicense.A
            )

            return motorcycle
        
        return False

    def update_motorcycle(self, motorcycle_obj):
        response = self.repo.update_motorcycle(motorcycle_obj)
        return response

    def delete_motorcycle(self, plate) -> str:
        response = self.repo.delete_motorcycle(plate)
        return response

    def refuel_motorcycle(self, plate_to_refuel, liters, price_per_liter) -> tuple:
        motorcycle_obj = self.get_by_plate(plate_to_refuel)
        
        if not motorcycle_obj:
            return "The plate is incorrect"
        
        maintenance = motorcycle_obj.refuel(liters, price_per_liter)

        return (self.update_motorcycle(motorcycle_obj), maintenance)
    
    def vehicle_exists(self, search_plate) -> bool:
        response = self.repo.vehicle_exists(search_plate)
        return response

    def vehicle_is_available(self, search_plate) -> bool:
        response = self.repo.vehicle_is_available(search_plate)
        return response