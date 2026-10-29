# external libs
import questionary as q

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

        response = MasterController.VEHICLE_CONTROLLER.value.show_vehicles(what=input)

        print(response)

        q.text("Press a key to go back").ask()

        clear_screen()
