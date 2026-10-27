# External libs
import questionary as q

from .new_vehicle import page_create_vehicle
from .show_all_vehicles import page_select_vehicles_to_show

def menu_vehicles():
    input = q.select(
        message = "|----- Vehicles Menu -----|",
        choices = [
            q.Choice(
                title   = "New vehicle",
                value   = page_create_vehicle
            ), 
            q.Choice(
                title   = "Show vehicles",
                value   = page_select_vehicles_to_show
            ), 
            q.Choice(
                title   = "Back to main menu", 
                value   = False
            ), 
        ]
    ).ask()

    if input:
        input()
