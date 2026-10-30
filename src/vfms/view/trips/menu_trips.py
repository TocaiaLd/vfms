# External libs
import questionary as q
from vfms.depedencies import MasterController

from vfms.view.trips.add_trip import add_trip

def menu_trips():
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

    if input:
        input()

