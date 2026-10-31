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
    
    def get_by_plate(self, plate) -> Car | False:
        vehicle = self.repo.get_by_plate(plate)
        
        if vehicle:
            car = Car(
                plate               = vehicle[0],
                model               = vehicle[1],  
                brand               = vehicle[2],  
                year                = vehicle[3],
                mileage             = vehicle[4],
                average_consumption = vehicle[5],
                status              = vehicle[6],
                max_fuel            = vehicle[7],
                fuel                = vehicle[8],
                ports               = vehicle[9],
                license             = VehicleLicense.B
            )

            return car
        
        return False

    def update_car(self, car_obj):
        response = self.repo.update_car(car_obj)
        return response

    def delete_car(self, plate) -> str:
        response = self.repo.delete_car(plate)
        return response

    def refuel_car(self, plate_to_refuel, liters, price_per_liter) -> tuple:
        car_obj = self.get_by_plate(plate_to_refuel)
        
        if not car_obj:
            return "The plate is incorrect"
        
        refuel = car_obj.refuel(liters, price_per_liter)

        return (self.update_car(car_obj), refuel)

    def vehicle_exists(self, search_plate) -> bool:
        response = self.repo.vehicle_exists(search_plate)
        return response

    def vehicle_is_available(self, search_plate) -> bool:
        response = self.repo.vehicle_is_available(search_plate)
        return response