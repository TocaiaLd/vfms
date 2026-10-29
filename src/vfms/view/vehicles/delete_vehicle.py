# external libs
import questionary as q

# Utilities
from vfms.utilities.clear_screen import clear_screen

# Project imports
from vfms.depedencies import MasterController

def delete_vehicle():
    running = True
    
    while running:
        input = q.select(
            "What type of vehicle do you want to delete?",
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

        
        loop_delete = True

        while loop_delete:
            response = MasterController.VEHICLE_CONTROLLER.value.show_vehicles(what=input)
            
            print(response)

            delete_input = q.text("Write the vehicle plate that you want to delete: ").ask()

            response = MasterController.VEHICLE_CONTROLLER.value.delete_vehicle(what=input, plate=delete_input)

            loop_delete = q.confirm(f"{response}. Do you want to continue?").ask()

            clear_screen()
