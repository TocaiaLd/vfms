# external libs
import questionary as q

# project imports
from vfms.config.depedencies import MasterController

def show_drivers() -> str:
    drivers = MasterController.DRIVER_CONTROLLER.value.show_drivers()

    for i in range(len(drivers)):
        drivers[i] = q.Choice(
            title   = repr(drivers[i]),
            value   = f"{drivers[i].cpf}"
        )

    input_driver = q.select(
        message         = "First, select a driver",
        choices         = drivers 
    ).ask()

    return input_driver

def show_vehicles() -> str:
    vehicles = MasterController.VEHICLE_CONTROLLER.value.show_vehicles("vehicles")

    for i in range(len(vehicles)):
        vehicles[i] = q.Choice(
            title   = repr(vehicles[i]),
            value   = f"{vehicles[i].plate}"
        )

    input_vehicle = q.select(
        message         = "Now, select a vehicle",
        choices         = vehicles 
    ).ask()

    return input_vehicle

def add_trip():
    cpf = show_drivers()
    plate= show_vehicles()

    origin      = q.text("Origin:").ask()
    destiny     = q.text("Destiny:").ask()
    distance    = q.text("Distance:").ask()

    request = {
        "origin"        : origin,
        "destiny"       : destiny,
        "distance"      : distance,
        "driver_cpf"    : cpf,
        "vehicle_plate" : plate
    }

    MasterController.TRIP_CONTROLLER.value.new_trip(request)
 
