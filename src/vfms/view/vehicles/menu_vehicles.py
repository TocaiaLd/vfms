# External libs
import questionary as q

# utilities
from vfms.utilities.clear_screen import clear_screen

# pages
from vfms.view.vehicles.delete_vehicle import delete_vehicle
from .new_vehicle import page_create_vehicle
from .vehicles_to_show import menu_vehicles_to_show

# def vehicle_maintenance():
#     controller = MasterController.VEHICLE_CONTROLLER.value
#     plate = q.text("Vehicle plate:").ask()
#     action = q.select("Action:", choices=["Record maintenance", "Complete maintenance", "Back"]).ask()
#     try:
#         if action == "Record maintenance":
#             kind = q.select("Type:", choices=["preventive", "corrective"]).ask()
#             cost = q.text("Cost:").ask()
#             description = q.text("Description:").ask()
#             controller.add_maintenance(plate, kind, cost, description)
#             q.text("Maintenance recorded; the vehicle is unavailable for allocation.").ask()
#             q.text("Press any key to continue.").ask()
#         elif action == "Complete maintenance":
#             controller.complete_maintenance(plate)
#             q.text("Maintenance completed; the vehicle is available.").ask()
#             q.text("Press any key to continue.").ask()
#     except (ValueError, TypeError) as error:
#         q.text(str(error)).ask()

# def vehicle_refuel():
#     controller = MasterController.VEHICLE_CONTROLLER.value
#     plate = q.text("Vehicle plate:").ask()
#     liters = q.text("Liters refueled:").ask()
#     price = q.text("Price per liter (optional):").ask() or 0
#     try:
#         record = controller.refuel(plate, liters, price)
#         q.text(f"Refueling recorded: {record.liters:g} L. Fuel level updated.").ask()
#         q.text("Press any key to continue.").ask()
#     except (ValueError, TypeError) as error:
#         q.text(str(error)).ask()

def menu_vehicles():
    running = True
    
    while running:
        input = q.select(
            message = "|----- Vehicles Menu -----|",
            choices = [
                q.Choice(
                    title   = "New vehicle",
                    value   = page_create_vehicle
                ), 
                q.Choice(
                    title   = "Show vehicles",
                    value   = menu_vehicles_to_show
                ),
                q.Choice(
                    title   = "Delete a vehicle", 
                    value   = delete_vehicle
                ),
                # q.Choice(
                #     title="Refuel", 
                #     value=vehicle_refuel
                # ),
                q.Choice(
                    title   = "Back to main menu", 
                    value   = False
                ), 
            ]
        ).ask()

        clear_screen()

        if not input:
            running = False
            return not running
        
        running = input()


