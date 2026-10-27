# external libs
import questionary as q

# project imports
from vfms.models.users.driver import Driver
from vfms.models.vehicles.vehicle import Vehicle
from vfms.config.depedencies import MasterController

def get_drivers() -> list[Driver]:
    drivers = MasterController.DRIVER_CONTROLLER.value.show_drivers()

    if not drivers:
        return False

    return drivers

def get_vehicles() -> list[Vehicle]:
    vehicles = MasterController.VEHICLE_CONTROLLER.value.show_vehicles("vehicles")

    if not vehicles:
        return False

    return vehicles

def add_trip():
    drivers = get_drivers()
    vehicles= get_vehicles()

    if not drivers or not vehicles:
        if not drivers and not vehicles:
            q.text("there are no drivers and vehicles, please add at least one of each to create a trip. Press any key to go back to the menu").ask()
        elif not drivers:
            q.text("there are no drivers, please add at least one to create a trip. Press any key to go back to the menu").ask()
        elif not vehicles:
            q.text("there are no vehicles, please add at least one to create a trip. Press any key to go back to the menu").ask()

        return

    for i in range(len(drivers)):
        drivers[i] = q.Choice(
            title   = repr(drivers[i]),
            value   = f"{drivers[i].cpf}"
        )

    cpf = q.select(
        message         = "First, select a driver",
        choices         = drivers 
    ).ask()

    for i in range(len(vehicles)):
        vehicles[i] = q.Choice(
            title   = repr(vehicles[i]),
            value   = f"{vehicles[i].plate}"
        )

    plate = q.select(
        message         = "Now, select a vehicle",
        choices         = vehicles 
    ).ask()


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
 
