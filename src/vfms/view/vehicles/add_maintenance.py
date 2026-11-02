# external libs
from vfms.enums.enum_maintenance import EnumMaintenance
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
            controllers.append(MasterController.CAR_CONTROLLER.value.add_maintenance)
            controllers.append(MasterController.CAR_CONTROLLER.value.get_by_plate)
        elif input == "trucks":
            controllers.append(MasterController.TRUCK_CONTROLLER.value.show_trucks)
            controllers.append(MasterController.TRUCK_CONTROLLER.value.add_maintenance)
            controllers.append(MasterController.TRUCK_CONTROLLER.value.get_by_plate)
        elif input == "motorcycles":
            controllers.append(MasterController.MOTORCYCLE_CONTROLLER.value.show_motorcycles)
            controllers.append(MasterController.MOTORCYCLE_CONTROLLER.value.add_maintenance)
            controllers.append(MasterController.MOTORCYCLE_CONTROLLER.value.get_by_plate)

        while loop:
            response = controllers[0]()
            
            print(response)

            plate_to_add_maintenance = q.text("Write the vehicle plate that you want to add a maintenance: ").ask()
            
            vehicle_obj = controllers[2](plate_to_add_maintenance)

            if not vehicle_obj: 
                 q.text("This vehicle doesnt exists, press any key to try again.").ask()
            elif vehicle_obj.status.value == 1:
                type_maintenance = q.select(
                "What type of maintenance it will be?",
                choices = [
                    q.Choice(
                        title   = "Preventive", 
                        value   = EnumMaintenance.PREVENTIVE
                    ), 
                    q.Choice(
                        title   = "Corrective", 
                        value   = EnumMaintenance.CORRECTIVE
                    ), 

                    ]
                ).ask()

                price = q.text("How much it will cost?").ask()
                price = float(price)

                description = q.text("Write a description for the maintenance: ").ask()
                
                response = controllers[1](plate_to_add_maintenance, type_maintenance, price, description)

                response = MasterController.MAINTENANCE_CONTROLLER.value.save_maintenance(response)

                loop = q.confirm(f"{response}. Do you want to continue in maintenance session?").ask()

                clear_screen()
            else:
                loop = q.confirm(f"The vehicle must be available to add a maintenance. Do you want to continue in maintenance session?").ask()