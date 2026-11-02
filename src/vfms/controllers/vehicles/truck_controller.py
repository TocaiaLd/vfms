from typing import Any

# External libs
from tabulate import tabulate

# Project dependencies
from vfms.repos.vehicles.truck_repo import TruckRepo
from vfms.models.vehicles.truck import Truck
from vfms.models.vehicles.vehicle import Vehicle
from vfms.enums.vehicle_license import VehicleLicense
from vfms.enums.enum_maintenance import EnumMaintenance

class TruckController:
    def __init__(
        self    : TruckController, 
        repo    : TruckRepo
    ) -> None:
        self.repo = repo

    def create_truck(self, request: dict[str, Any]) -> str:
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

    def get_by_plate(self, plate: str) -> Truck | bool:
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

    def update_truck(self, truck_obj: Truck) -> str:
        response = self.repo.update_truck(truck_obj)
        return response

    def delete_truck(self, plate: str) -> str:
        truck = self.get_by_plate(plate)

        if not truck:
            return "This truck plate doesnt exist"

        if truck.status.value == 1 or truck.status.value == 0:
            response = self.repo.delete_truck(plate)
            return response
        
        return "The car must be AVAILABLE or INACTIVE to delete"

    def refuel_truck(
        self,
        plate_to_refuel: str,
        liters: float,
        price_per_liter: float,
    ) -> tuple[str, tuple[object, ...] | None] | str:
        truck_obj = self.get_by_plate(plate_to_refuel)
        
        if not truck_obj:
            return "The plate is incorrect"
        
        maintenance = truck_obj.refuel(liters, price_per_liter)

        return (self.update_truck(truck_obj), maintenance)

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
    ) -> tuple[str, EnumMaintenance, float, str, str, str] | str:
        vehicle_obj: Truck | bool = self.get_by_plate(plate_to_add_maintenance)

        if not vehicle_obj:
            return "The plate is incorrect"
        
        maintenance = vehicle_obj.new_maintenance(type_maintenance, price, description)

        return maintenance