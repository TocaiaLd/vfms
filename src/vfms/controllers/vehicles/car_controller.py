from typing import Any

# External libs
from tabulate import tabulate

# Project dependencies
from vfms.models.vehicles.vehicle import Vehicle
from vfms.enums.vehicle_license import VehicleLicense
from vfms.enums.enum_maintenance import EnumMaintenance
from vfms.repos.vehicles.car_repo import CarRepo
from vfms.models.vehicles.car import Car

class CarController:
    # Coordinate car operations between the view, model, and repository.
    def __init__(
        self    : CarController, 
        repo    : CarRepo
    ) -> None:
        self.repo = repo

    def create_car(self, request: dict[str, Any]) -> str:
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
    
    def get_by_plate(self, plate: str) -> Car | bool:
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
                license             = VehicleLicense[vehicle[10]]
            )

            return car
        
        return False

    def update_car(self, car_obj: Car) -> str:
        response = self.repo.update_car(car_obj)
        return response

    def delete_car(self, plate: str) -> str:
        car = self.get_by_plate(plate)

        if not car:
            return "This car plate doesnt exist"

        if car.status.value == 1 or car.status.value == 0:
            response = self.repo.delete_car(plate)
            return response
        
        return "The car must be AVAILABLE or INACTIVE to delete"

    def refuel_car(
        self,
        plate_to_refuel: str,
        liters: float | str,
        price_per_liter: float | str,
    ) -> tuple[str, tuple[object, ...] | None] | str:
        car_obj = self.get_by_plate(plate_to_refuel)
        
        if not car_obj:
            return "The plate is incorrect"
        
        refuel = car_obj.refuel(liters, price_per_liter)

        return (self.update_car(car_obj), refuel)

    def vehicle_exists(self, search_plate: str) -> bool:
        response = self.repo.vehicle_exists(search_plate)
        return response

    def vehicle_is_available(self, search_plate: str) -> bool:
        response = self.repo.vehicle_is_available(search_plate)
        return response

    def add_maintenance(
        self,
        plate_to_add_maintenance: str,
        type_maintenance: EnumMaintenance,
        price: float,
        description: str,
    ) -> tuple[str, str, float, str, str, str, float] | str:
        vehicle_obj: Car | bool = self.get_by_plate(plate_to_add_maintenance)

        if not vehicle_obj:
            return "The plate is incorrect"
        
        maintenance = vehicle_obj.new_maintenance(type_maintenance, price, description)

        return maintenance
