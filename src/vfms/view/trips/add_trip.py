# external libs
import questionary as q

# project imports
from vfms.models.users.driver import Driver
from vfms.models.vehicles.vehicle import Vehicle
from vfms.depedencies import MasterController

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

    drivers_choices = []

    for i in range(len(drivers)):
        drivers_choices.append(q.Choice(
            title   = repr(drivers[i]),
            value   = i
        ))

    driver_index = q.select(
        message         = "First, select a driver",
        choices         = drivers_choices
    ).ask()

    driver = drivers[driver_index]

    vehicles_choices = []

    for i in range(len(vehicles)):
        vehicles_choices.append(q.Choice(
            title   = repr(vehicles[i]),
            value   = i
        ))

    vehicle_index = q.select(
        message         = "Now, select a vehicle",
        choices         = vehicles_choices
    ).ask()

    vehicle = vehicles[vehicle_index]

    from vfms.repos.trip_repo import TripRepo
    if TripRepo.license_allows(driver.license.name, vehicle.license_category.name):
        origin      = q.text("Origin:").ask()
        destiny     = q.text("Destiny:").ask()
        distance    = q.text("Distance:").ask()

        request = {
            "origin"        : origin,
            "destiny"       : destiny,
            "distance"      : distance,
            "driver_cpf"    : f"{driver.cpf}",
            "vehicle_plate" : vehicle.plate
        }

        try:
            MasterController.TRIP_CONTROLLER.value.new_trip(request)
            q.text("Trip allocated. The driver and vehicle are assigned until the trip is completed.").ask()
        except (ValueError, TypeError) as error:
            q.text(str(error)).ask()
    else:
        q.text("Driver's license is incompatible with the vehicle category. Press any key to continue.").ask()

