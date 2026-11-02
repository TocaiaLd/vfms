# external libs
import questionary as q

# Utilities
from vfms.enums.vehicle_status import VehicleStatus
from vfms.utilities.clear_screen import clear_screen

# Project imports
from vfms.depedencies import MasterController
from vfms.models.vehicles.car import Car
from vfms.models.vehicles.motorcycle import Motorcycle
from vfms.models.vehicles.truck import Truck
from vfms.models.vehicles.vehicle import Vehicle

def motorcycle_asks(vehicle_obj: Motorcycle) -> Motorcycle:
    vehicle_obj.cc = q.text(f"New cc: {vehicle_obj.cc}").ask() 

    return vehicle_obj

def truck_asks(vehicle_obj: Truck) -> Truck:
    vehicle_obj.max_weight = q.text(f"Max weight: {vehicle_obj.max_weight}").ask() 

    return vehicle_obj

def car_asks(vehicle_obj: Car) -> Car:
    vehicle_obj.ports = q.text(f"New number of ports: {vehicle_obj.ports}").ask() 

    return vehicle_obj

def vehicle_asks(vehicle_obj: Vehicle) -> Vehicle:
    vehicle_obj.model               = q.text(f"New model: (Old is {vehicle_obj.model})").ask()
    vehicle_obj.brand               = q.text(f"New brand: (Old is {vehicle_obj.brand})").ask()
    vehicle_obj.year                = q.text(f"New year: (Old is {vehicle_obj.year})").ask()
    vehicle_obj.mileage             = q.text(f"New mileage: (Old is {vehicle_obj.mileage})").ask()
    vehicle_obj.average_consumption = q.text(f"New average consumption: (Old is {vehicle_obj.average_consumption})").ask()
    vehicle_obj.max_fuel            = q.text(f"New max fuel: (Old is {vehicle_obj.max_fuel} - Actual fuel is {vehicle_obj.fuel})").ask()

    while vehicle_obj.max_fuel < vehicle_obj.fuel:
        vehicle_obj.max_fuel = q.text(f"The new max fuel cannot be less than the actual fuel: (Old is {vehicle_obj.max_fuel})").ask()

    return vehicle_obj

def update_vehicle() -> bool | None:
    running = True
    
    while running:
        input = q.select(
            "What type of vehicle do you want to update?",
            choices = [
                q.Choice(
                    title   = "Car", 
                    value   = "cars"
                ), 
                q.Choice(
                    title   = "Truck", 
                    value   = "trucks"
                ), 
                q.Choice(
                    title   = "Motorcycle", 
                    value   = "motorcycles"
                ),
                q.Choice(
                    title   = "Back to previous page", 
                    value   = False
                ), 
            ]
        ).ask()

        if not input:
            running = False
            return True

        
        loop_edit = True

        controllers = []

        if input == "cars":
            controllers.append(MasterController.CAR_CONTROLLER.value.show_cars)
            controllers.append(MasterController.CAR_CONTROLLER.value.get_by_plate)
            controllers.append(car_asks)
            controllers.append(MasterController.CAR_CONTROLLER.value.update_car)
        elif input == "trucks":
            controllers.append(MasterController.TRUCK_CONTROLLER.value.show_trucks)
            controllers.append(MasterController.TRUCK_CONTROLLER.value.get_by_plate)
            controllers.append(truck_asks)
            controllers.append(MasterController.TRUCK_CONTROLLER.value.update_truck)
        elif input == "motorcycles":
            controllers.append(MasterController.MOTORCYCLE_CONTROLLER.value.show_motorcycles)
            controllers.append(MasterController.MOTORCYCLE_CONTROLLER.value.get_by_plate)
            controllers.append(motorcycle_asks)
            controllers.append(MasterController.MOTORCYCLE_CONTROLLER.value.update_motorcycle)

        while loop_edit:
            response = controllers[0]()
            
            print(response)

            plate_to_edit = q.text("Write the vehicle plate that you want to update: ").ask()

            vehicle_obj = controllers[1](plate_to_edit)

            if not vehicle_obj: 
                 q.text("This vehicle doesnt exists, press any key to try again: ").ask()
            elif vehicle_obj.status.value == 1:

                vehicle_obj = vehicle_asks(vehicle_obj)
                vehicle_obj = controllers[2](vehicle_obj)

                response = controllers[3](vehicle_obj)            

                loop_edit = q.confirm(f"{response}. Do you want to continue?").ask()

                clear_screen()

            else:
                loop_edit = q.confirm(f"The vehicle must be with the status AVAILABLE. Do you want to continue in update session?").ask()
                clear_screen()
