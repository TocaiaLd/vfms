import questionary

from vfms.enums.vehicle_license import VehicleLicense
from vfms.enums import VehicleStatus

from vfms.view.page_close import page_close

def car_asks() -> dict:
    ports = questionary.text("Number of ports: ").ask()
    license_category = VehicleLicense.B    
    
    d = {
        "type"              : "Car",
        "ports"             : ports,
        "license_category"  : license_category
    }

    return d

def page_create_vehicle() -> dict:
    options = [
        questionary.Choice("Car", value=car_asks), 
        questionary.Choice("Truck"), 
        questionary.Choice("Motorcicle"),
        questionary.Choice("Back to homepage", value=0), 
    ]
    
    input = questionary.select(
        "Choose a vehicle type:",
        choices = options
    ).ask()
    
    if input == 0:
        return page_close(message="Are you sure to go to the homepage?")
        
    plate = questionary.text("Plate: ").ask()
    model = questionary.text("Model: ").ask()
    brand = questionary.text("Brand: ").ask()
    year = questionary.text("Year: ").ask()
    mileage = questionary.text("Mileage: ").ask()
    average_consumption = 0.0
    status = VehicleStatus.AVAILABLE
    maintenance_h = None

    request = {
        "type" : None,
        "plate": plate,
        "model": model,
        "brand": brand,
        "year": year,
        "mileage": mileage,
        "average_consumption": average_consumption,
        "status": status,
        "license_category": None,
        "maintenance_h": maintenance_h
    }

    # Call specifics asks
    request.update(input())

    return request
