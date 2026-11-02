# External libs
import questionary as q

from vfms.view.trips.show_trips import show_trips
from vfms.view.trips.finish_trip import finish_trip
from vfms.view.trips.add_trip import add_trip

def menu_trips():
    running = True

    while running:
        input = q.select(
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

        if not input:
            running = False
            return True

        input()