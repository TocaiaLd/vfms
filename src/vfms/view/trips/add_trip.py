from typing import Any

# external libs
import questionary as q

# utilities
from vfms.utilities.clear_screen import clear_screen
from vfms.depedencies import settings
from vfms.config.settings_validations import is_license_compatible

# project imports
from vfms.enums.enum_trip import EnumTrip
from vfms.depedencies import MasterController
from vfms.models.users.driver import Driver

def show_drivers() -> None:
    response = MasterController.DRIVER_CONTROLLER.value.show_drivers()

    print(response)

def show_vehicles(vehicle_controller: Any, vehicle_type: str) -> None:
    print(getattr(vehicle_controller, f"show_{vehicle_type}")())

def loop_driver() -> str | bool | None:
    loop = True

    while loop:
        show_drivers()
        driver_to_add_trip = q.text("Write the cpf of the driver that you want to add a trip: ").ask()
        driver_exists = MasterController.DRIVER_CONTROLLER.value.driver_exists(driver_to_add_trip)

        if not driver_exists:
            loop = q.confirm("This driver does not exists. Do you want to select another driver?").ask()
        else:
            driver_available = (
                MasterController.DRIVER_CONTROLLER.value.driver_is_available(
                    driver_to_add_trip
                )
            )

            if driver_available:
                return driver_to_add_trip
            else:
                loop = q.confirm("This driver is not available. Do you want to select other driver?").ask()

        clear_screen()

    return loop

def loop_vehicle(
    vehicle_controller: Any,
    driver_cpf: str,
    vehicle_type: str,
) -> str | bool | None:
    loop = True

    while loop:
        show_vehicles(vehicle_controller, vehicle_type)
        vehicle_to_add_trip = q.text(f"Write the plate of the {vehicle_type} that you want to add a trip: ").ask()
        vehicle_exists = vehicle_controller.vehicle_exists(vehicle_to_add_trip)

        if not vehicle_exists:
            loop = q.confirm("This vehicle does not exists. Do you want to select other vehicle?").ask()
        elif vehicle_exists:
            vehicle_available = vehicle_controller.vehicle_is_available(vehicle_to_add_trip)

            if vehicle_available:
                driver_obj  = MasterController.DRIVER_CONTROLLER.value.get_by_cpf(driver_cpf)

                if not isinstance(driver_obj, Driver):
                    q.text("The selected driver could not be loaded.").ask()
                    loop = False
                    continue

                # Check the driver's license against the selected vehicle category.
                if not is_license_compatible(settings, vehicle_type, driver_obj.license):
                    q.text(
                        "The driver's license does not meet the configured requirements."
                    ).ask()

                    loop = False
                    continue

                return vehicle_to_add_trip
            else:
                loop = q.confirm("This vehicle is not available. Do you want to select another vehicle?").ask()

        clear_screen()
    
    return loop

def add_trip() -> bool | None:
    running = True

    while running:
        selection = q.select(
            "Choose a vehicle type to add a trip:",
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
                    title   = "Back to the previous page", 
                    value   = False
                ), 
            ]
        ).ask()
        
        vehicle_controller: Any = None

        if selection == "cars":
            vehicle_controller = MasterController.CAR_CONTROLLER.value
        elif selection == "trucks":
            vehicle_controller = MasterController.TRUCK_CONTROLLER.value
        elif selection == "motorcycles":
            vehicle_controller = MasterController.MOTORCYCLE_CONTROLLER.value

        if not selection:
            running = False
            return not running

        cpf = loop_driver()
        
        if cpf:
            plate = loop_vehicle(vehicle_controller, cpf, selection)
            
            if plate:
                origin       = q.text("Write the origin").ask()
                destiny      = q.text("Write the destiny").ask()
                distance     = q.text("Write the mileage of the trip").ask()

                dict_trip = {
                    "driver_cpf"      : cpf,
                    "vehicle_plate"   : plate,
                    "origin"          : origin,
                    "destiny"         : destiny,
                    "distance"        : distance,
                    "status"          : EnumTrip.IN_PROGRESS
                }

                response = MasterController.TRIP_CONTROLLER.value.new_trip(dict_trip)

                q.text(f"{response} press any key to return to vehicle selection trip").ask()


        clear_screen()
