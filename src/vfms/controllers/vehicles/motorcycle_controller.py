from typing import Any

# External libs
from tabulate import tabulate

# Project dependencies
from vfms.repos.vehicles.motorcycle_repo import MotorcycleRepo
from vfms.models.vehicles.motorcycle import Motorcycle
from vfms.models.vehicles.vehicle import Vehicle
from vfms.enums.vehicle_license import VehicleLicense
from vfms.enums.enum_maintenance import EnumMaintenance

class MotorcycleController:
    # Coordinate motorcycle operations between the view, model, and repository.
    def __init__(
        self    : MotorcycleController, 
        repo    : MotorcycleRepo
    ) -> None:
        self.repo = repo

    def create_motorcycle(self, request: dict[str, Any]) -> str:
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
    
    def get_by_plate(self, plate: str) -> Motorcycle | bool:
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
                license             = VehicleLicense[vehicle[10]]
            )

            return motorcycle
        
        return False

    def update_motorcycle(self, motorcycle_obj: Motorcycle) -> str:
        response = self.repo.update_motorcycle(motorcycle_obj)
        return response

    def delete_motorcycle(self, plate: str) -> str:
        motorycle = self.get_by_plate(plate)

        if not motorycle:
            return "This motorycle plate doesnt exist"

        if motorycle.status.value == 1 or motorycle.status.value == 0:
            response = self.repo.delete_motorcycle(plate)
            return response
        
        return "The motorycle must be AVAILABLE or INACTIVE to delete"

    def refuel_motorcycle(
        self,
        plate_to_refuel: str,
        liters: float | str,
        price_per_liter: float | str,
    ) -> tuple[str, tuple[object, ...] | None] | str:
        motorcycle_obj = self.get_by_plate(plate_to_refuel)
        
        if not motorcycle_obj:
            return "The plate is incorrect"
        
        maintenance = motorcycle_obj.refuel(liters, price_per_liter)

        return (self.update_motorcycle(motorcycle_obj), maintenance)
    
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
        vehicle_obj: Motorcycle | bool = self.get_by_plate(plate_to_add_maintenance)

        if not vehicle_obj:
            return "The plate is incorrect"
        
        maintenance = vehicle_obj.new_maintenance(type_maintenance, price, description)

        return maintenance
