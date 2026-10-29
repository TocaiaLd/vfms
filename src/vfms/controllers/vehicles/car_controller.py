# External libs
from tabulate import tabulate

# Project dependencies
from vfms.enums.vehicle_license import VehicleLicense
from vfms.repos.vehicles.car_repo import CarRepo
from vfms.models.vehicles.car import Car

class CarController:
    def __init__(
        self    : CarController, 
        repo    : CarRepo
    ):
        self.repo = repo

    def create_car(self, request) -> str:
        car = Car(
            plate               = request["plate"],
            model               = request["model"],  
            brand               = request["brand"],  
            year                = request["year"],
            mileage             = request["mileage"],
            average_consumption = request["average_consumption"],
            status              = request["status"],
            max_fuel            = request["max_fuel"],
            fuel                = request["fuel"],
            ports               = request["ports"],
            license             = VehicleLicense.B
        )
       
        response = self.repo.save_car(car)
        return response

    def show_cars(self) -> str:
        response = self.repo.show_cars()
        
        collumns = ["Plate", "Model", "Brand", "Year", "Mileage", "Consumption", "Status", "Max Fuel", "Fuel", "Ports", "License"]
        data = []

        for car in response:
            data.append(car)

        response = tabulate(data, headers=collumns, tablefmt="fancy_grid")
        
        return response
    
    def delete_car(self, plate) -> str:
        response = self.repo.delete_car(plate)
        return response