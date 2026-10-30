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

        
        loop_delete = True

        controllers = []

        if input == "cars":
            controllers.append(MasterController.CAR_CONTROLLER.value.show_cars)
            controllers.append(MasterController.CAR_CONTROLLER.value.delete_car)
        elif input == "trucks":
            controllers.append(MasterController.TRUCK_CONTROLLER.value.show_trucks)
            controllers.append(MasterController.TRUCK_CONTROLLER.value.delete_truck)
        elif input == "motorcycles":
            controllers.append(MasterController.MOTORCYCLE_CONTROLLER.value.show_motorcycles)
            controllers.append(MasterController.MOTORCYCLE_CONTROLLER.value.delete_motorcycle)

        while loop_edit:
            response = controllers[0]()
            
            print(response)

            plate_to_edit = q.text("Write the vehicle plate that you want to delete: ").ask()

            response = controllers[1](plate_to_edit)

            loop_edit = q.confirm(f"{response}. Do you want to continue?").ask()

            clear_screen()
