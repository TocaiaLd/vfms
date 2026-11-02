# External libs
import questionary as q
from vfms.utilities.clear_screen import clear_screen

from vfms.view.trips.show_trips import show_trips
from vfms.view.trips.finish_trip import finish_trip
from vfms.view.trips.add_trip import add_trip

def menu_trips() -> bool | None:
    while True:
        clear_screen()
        selection = q.select(
            message = "|----- Trips Menu -----|",
            choices = [
                q.Choice(
                    title   = "Add a trip",
                    value   = add_trip
                ),
                q.Choice(
                    title   = "Show trips",
                    value   = show_trips
                ), 
                q.Choice(
                    title   = "Finish a trip",
                    value   = finish_trip
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
