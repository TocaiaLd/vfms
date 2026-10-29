# External libs
import questionary as q

# Utilities
from vfms.utilities.clear_screen import clear_screen

# Project imports
from vfms.depedencies import MasterController
from vfms.enums.vehicle_status import VehicleStatus

def motorcycle_asks() -> dict:
    cc = q.text("cc: ").ask() 
    
    d = {
        "type"           : "Motorcycle",
        "cc"             : cc,
    }

    return d

def truck_asks() -> dict:
    max_weight = q.text("Max weight: ").ask() 
    
    d = {
        "max_weight"             : max_weight,
    }

    return d

def car_asks() -> dict:
    ports = q.text("Number of ports: ").ask() 
    
    d = {
        "ports"             : ports,
    }

    return d

def vehicle_asks() -> dict:
    plate               = q.text("Plate: ").ask()
    model               = q.text("Model: ").ask()
    brand               = q.text("Brand: ").ask()
    year                = q.text("Year: ").ask()
    mileage             = q.text("Mileage: ").ask()
    average_consumption = q.text("Average consumption:").ask()
    
    status = q.select(
        "Choose a vehicle type:",
        choices = [
            q.Choice(
                title   = "Available", 
                value   = VehicleStatus.AVAILABLE
            ), 
            q.Choice(
                title   = "Inactive", 
                value   = VehicleStatus.INACTIVE
            ), 
            q.Choice(
                title   = "Maintenance", 
                value   = VehicleStatus.MAINTENANCE
            ), 
        ]
    ).ask()

    max_fuel            = q.text("Max fuel:").ask()
    fuel                = q.text("fuel:").ask()

    request = {
        "plate"                 : plate,
        "model"                 : model,
        "brand"                 : brand,
        "year"                  : year,
        "mileage"               : mileage,
        "average_consumption"   : average_consumption,
        "status"                : status,
        "max_fuel"              : max_fuel,
        "fuel"                  : fuel
    }

    # Returns a dict with the general attributes of a Vehicle class
    return request

def page_create_vehicle() -> bool:
    running = True

    while running:
        input = q.select(
            "Choose a vehicle type:",
            choices = [
                q.Choice(
                    title   = "Car", 
                    value   = (car_asks, 1)
                ), 
                q.Choice(
                    title   = "Truck", 
                    value   = (truck_asks, 2)
                ), 
                q.Choice(
                    title   = "Motorcycle", 
                    value   = (motorcycle_asks, 3)
                ), 
                q.Choice(
                    title   = "Back to the previous page", 
                    value   = False
                ), 
            ]
        ).ask()
        
        if not input:
            running = False
            return not running

        request = vehicle_asks()
        request.update(input[0]())

        response = None

        if input[1] == 1:
            response = MasterController.CAR_CONTROLLER.value.create_car(request)
        elif input[1] == 2:
            response = MasterController.TRUCK_CONTROLLER.value.create_truck(request)
        elif input[1] == 3:
            response = MasterController.MOTORCYCLE_CONTROLLER.value.create_motorcycle(request)
        
        q.text(f"{response}. Press any key to continue...").ask()

        clear_screen()
