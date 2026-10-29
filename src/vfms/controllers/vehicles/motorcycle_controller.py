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
    
    def delete_motorcycle(self, plate) -> str:
        response = self.repo.delete_motorcycle(plate)
        return response