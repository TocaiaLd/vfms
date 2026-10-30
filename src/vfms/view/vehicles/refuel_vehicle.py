# external libs
import questionary as q

# Utilities
from vfms.utilities.clear_screen import clear_screen

# Project imports
from vfms.depedencies import MasterController

def refuel_vehicle():
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

        
        loop_delete = True

        controllers = []

        if input == "cars":
            controllers.append(MasterController.CAR_CONTROLLER.value.show_cars)
            controllers.append(MasterController.CAR_CONTROLLER.value.refuel_car)
        elif input == "trucks":
            controllers.append(MasterController.TRUCK_CONTROLLER.value.show_trucks)
            controllers.append(MasterController.TRUCK_CONTROLLER.value.refuel_truck)
        elif input == "motorcycles":
            controllers.append(MasterController.MOTORCYCLE_CONTROLLER.value.show_motorcycles)
            controllers.append(MasterController.MOTORCYCLE_CONTROLLER.value.refuel_motorcycle)

        while loop_delete:
            response = controllers[0]()
            
            print(response)

            plate_to_refuel = q.text("Write the vehicle plate that you want to refuel: ").ask()
            liters          = q.text("Write how many litters to refuel: ").ask()
            price_per_liter = q.text("Write the price per liter: ").ask()

            response = controllers[1](plate_to_refuel, liters, price_per_liter)

            MasterController.REFUEL_CONTROLLER.value.save_refuel(response[1])

            loop_delete = q.confirm(f"{response[0]}. Do you want to continue?").ask()

            clear_screen()
