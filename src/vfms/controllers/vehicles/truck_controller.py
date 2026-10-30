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

        for truck in response:
            data.append(truck)

        response = tabulate(data, headers=collumns, tablefmt="fancy_grid")

        return response

    def get_by_plate(self, plate) -> Truck | False:
        vehicle = self.repo.get_by_plate(plate)
        
        if vehicle:
            truck = Truck(
                plate               = vehicle[0],
                model               = vehicle[1],  
                brand               = vehicle[2],  
                year                = vehicle[3],
                mileage             = vehicle[4],
                average_consumption = vehicle[5],
                status              = vehicle[6],
                max_fuel            = vehicle[7],
                fuel                = vehicle[8],
                max_weight          = vehicle[9],
                license             = VehicleLicense.D
            )

            return truck
        
        return False

    def update_truck(self, truck_obj):
        response = self.repo.update_truck(truck_obj)
        return response

    def delete_truck(self, plate) -> str:
        response = self.repo.delete_truck(plate)
        return response

    def refuel_truck(self, plate_to_refuel, liters, price_per_liter) -> tuple:
        truck_obj = self.get_by_plate(plate_to_refuel)
        
        if not truck_obj:
            return "The plate is incorrect"
        
        maintenance = truck_obj.refuel(liters, price_per_liter)

        return (self.update_truck(truck_obj), maintenance)