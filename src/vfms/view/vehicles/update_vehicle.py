# external libs
import questionary as q

# Utilities
from vfms.utilities.clear_screen import clear_screen

# Project imports
from vfms.depedencies import MasterController

def update_vehicle():
    running = True
    
    while running:
        input = q.select(
            "What type of vehicle do you want to update?",
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
                    title   = "Back to previous page", 
                    value   = False
                ), 
            ]
        ).ask()

        if not input:
            running = False
            return True

        
        loop_update = True

        while loop_update:
            response = MasterController.VEHICLE_CONTROLLER.value.show_vehicles(what=input)
            
            print(response)

            delete_input = q.text("Write the vehicle plate that you want to update: ").ask()

            response = MasterController.VEHICLE_CONTROLLER.value.delete_vehicle(what=input, plate=delete_input)

            loop_update = q.confirm(f"{response}. Do you want to continue?").ask()

            clear_screen()
