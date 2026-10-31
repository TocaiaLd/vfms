# External libs
import questionary as q

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
                    title   = "Back to main menu", 
                    value   = False
                ), 
            ]
        ).ask()

        if not input:
            running = False
            return True

        input()