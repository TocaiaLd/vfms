# External libs
from tabulate import tabulate

# Project dependencies
from vfms.repos.vehicles.truck_repo import TruckRepo
from vfms.models.vehicles.truck import Truck
from vfms.enums.vehicle_license import VehicleLicense

class TruckController:
    def __init__(
        self    : TruckController, 
        repo    : TruckRepo
    ):
        self.repo = repo

    def create_truck(self, request) -> str:
        truck = Truck(
            plate               = request["plate"],
            model               = request["model"],  
            brand               = request["brand"],  
            year                = request["year"],
            mileage             = request["mileage"],
            average_consumption = request["average_consumption"],
            status              = request["status"],
            max_fuel            = request["max_fuel"],
            fuel                = request["fuel"],
            max_weight          = request["max_weight"],
            license             = VehicleLicense.D
        )
       
        response = self.repo.save_truck(truck)
        return response

    def show_trucks(self) -> str:
        response = self.repo.show_trucks()

        collumns = ["Plate", "Model", "Brand", "Year", "Mileage", "Consumption", "Status", "Max Fuel", "Fuel", "Max Weight", "License"]
        data = []

        for motorcycle in response:
            data.append(motorcycle)

        response = tabulate(data, headers=collumns, tablefmt="fancy_grid")

        return response

    def delete_truck(self, plate) -> str:
        response = self.repo.delete_truck(plate)
        return response