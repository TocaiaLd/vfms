# Standard libs
import questionary as q

# Project imports
from vfms.config.depedencies import MasterController
from vfms.enums.vehicle_status import VehicleStatus

def motorcycle_asks() -> dict:
    ports = q.text("cc: ").ask() 
    
    d = {
        "type"           : "motorcycle",
        "cc"             : ports,
    }

    return d

def truck_asks() -> dict:
    ports = q.text("Max weight: ").ask() 
    
    d = {
        "type"                   : "truck",
        "max_weight"             : ports,
    }

    return d

def car_asks() -> dict:
    ports = q.text("Number of ports: ").ask() 
    
    d = {
        "type"              : "car",
        "ports"             : ports,
    }

    return d

def vehicle_asks() -> dict:
    plate                           = q.text("Plate: ").ask()
    model                           = q.text("Model: ").ask()
    brand                           = q.text("Brand: ").ask()
    year                            = q.text("Year: ").ask()
    mileage                         = q.text("Mileage: ").ask()

    request = {
        "plate"                 : plate,
        "model"                 : model,
        "brand"                 : brand,
        "year"                  : year,
        "mileage"               : mileage,
        "average_consumption"   : 0.0,
        "status"                : VehicleStatus.AVAILABLE,
        "maintenance_h"         : [],
        "trips"                 : []
    }

    # Call specifics asks
    return request

def page_create_vehicle():
    i = q.select(
        "Choose a vehicle type:",
        choices = [
            q.Choice(
                title   = "Car", 
                value   = car_asks
            ), 
            q.Choice(
                title   = "Truck", 
                value   = truck_asks
            ), 
            q.Choice(
                title   = "Motorcycle", 
                value   = motorcycle_asks
            ), 
            q.Choice(
                title   = "Back to homepage", 
                value   = 0
            ), 
        ]
    ).ask()
        
    if i == 0:
        return
    
    request = vehicle_asks()
    request.update(i())

    MasterController.VEHICLE_CONTROLLER.value.create_vehicle(request)
