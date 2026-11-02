# External libs
import questionary as q
from vfms.utilities.clear_screen import clear_screen

from vfms.view.maintenances.show_maintenances import show_maintenances
from vfms.view.maintenances.finish_maintenance import finish_maintenance
from vfms.view.maintenances.add_maintenance import add_maintenance_vehicle

def menu_maintenances() -> bool | None:
    while True:
        clear_screen()
        selection = q.select(
            message = "|----- Maintenances Menu -----|",
            choices = [
                q.Choice(
                    title   = "Show Maintenances",
                    value   = show_maintenances
                ),
                q.Choice(
                    title   = "Add a maintenance to a vehicle",
                    value   = add_maintenance_vehicle
                ),
                q.Choice(
                    title   = "Finish a maintenance",
                    value   = finish_maintenance
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
