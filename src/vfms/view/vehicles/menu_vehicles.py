# External libs
import questionary as q

# utilities
from vfms.utilities.clear_screen import clear_screen

# pages
from vfms.view.vehicles.new_vehicle import page_create_vehicle
from vfms.view.vehicles.vehicles_to_show import menu_vehicles_to_show
from vfms.view.vehicles.update_vehicle import update_vehicle
from vfms.view.vehicles.delete_vehicle import delete_vehicle
from vfms.view.vehicles.refuel_vehicle import refuel_vehicle

def menu_vehicles() -> bool | None:
    while True:
        clear_screen()
        selection = q.select(
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
                q.Choice(
                    title   = "Refuel a vehicle", 
                    value   = refuel_vehicle
                ),
                q.Choice(
                    title   = "Update a vehicle", 
                    value   = update_vehicle
                ),
                q.Choice(
                    title   = "Back to main menu", 
                    value   = False
                ), 
            ]
        ).ask()

        if selection is None or selection is False:
            clear_screen()
            return True

        selection()
        clear_screen()


