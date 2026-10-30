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
    running = True

    while running:
        input = q.select(
            "Choose a vehicle type:",
            choices = [
                q.Choice(
                    title   = "Car", 
                    value   = 
                ), 
                q.Choice(
                    title   = "Truck", 
                    value   = 
                ), 
                q.Choice(
                    title   = "Motorcycle", 
                    value   = 
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

        response = None
        
        q.text(f"{response}. Press any key to continue...").ask()

        clear_screen()
