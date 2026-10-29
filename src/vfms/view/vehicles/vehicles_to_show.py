# external libs
import questionary as q
from tabulate import tabulate

# Utilities
from vfms.utilities.clear_screen import clear_screen

# Project imports
from vfms.depedencies import MasterController

def menu_vehicles_to_show():
    running = True
    
    while running:
        input = q.select(
            "Choose a vehicle type to show:",
            choices = [
                q.Choice(
                    title   = "Show only cars", 
                    value   = "cars"
                ), 
                q.Choice(
                    title   = "Show only trucks", 
                    value   = "trucks"
                ), 
                q.Choice(
                    title   = "Show only motorcycles", 
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

        response = None
        if input == "cars":
            response = MasterController.CAR_CONTROLLER.value.show_cars()
        elif input == "trucks":
            response = MasterController.TRUCK_CONTROLLER.value.show_trucks()
        elif input == "motorcycles":
            response = MasterController.MOTORCYCLE_CONTROLLER.value.show_motorcycles()

        print(response)

        q.text("Press a key to go back").ask()

        clear_screen()
