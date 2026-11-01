# external libs
import questionary as q

# Utilities
from vfms.utilities.clear_screen import clear_screen

# Project imports
from vfms.depedencies import MasterController

def add_maintenance_vehicle():
    running = True
    
    while running:
        input = q.select(
            "What type of vehicle do you want to refuel?",
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

        
        loop = True

        controllers = []

        if input == "cars":
            controllers.append(MasterController.CAR_CONTROLLER.value.show_cars)
            controllers.append(MasterController.CAR_CONTROLLER.value.add_maintenance_car)
        elif input == "trucks":
            controllers.append(MasterController.TRUCK_CONTROLLER.value.show_trucks)
            controllers.append(MasterController.TRUCK_CONTROLLER.value.add_maintenance_truck)
        elif input == "motorcycles":
            controllers.append(MasterController.MOTORCYCLE_CONTROLLER.value.show_motorcycles)
            controllers.append(MasterController.MOTORCYCLE_CONTROLLER.value.add_maintenance_motorcycle)

        while loop:
            response = controllers[0]()
            
            print(response)

            plate_to_add_maintenance = q.text("Write the vehicle plate that you want to add a maintenance: ").ask()
            
            # response = controllers[1](plate_to_refuel, liters, price_per_liter)

            # MasterController.REFUEL_CONTROLLER.value.save_refuel(response[1])

            # loop = q.confirm(f"{response[0]}. Do you want to continue?").ask()

            clear_screen()
