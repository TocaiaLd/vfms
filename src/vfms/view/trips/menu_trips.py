# External libs
import questionary as q
from vfms.config.depedencies import MasterController

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
                title="Complete a trip",
                value=complete_trip,
            ),
            q.Choice(
                title   = "Back to main menu", 
                value   = False
            ), 
        ]
    ).ask()

    if input:
        input()

def complete_trip():
    trip_id = q.text("Trip ID:").ask()
    try:
        MasterController.TRIP_CONTROLLER.value.finish_trip(trip_id)
        q.text("Trip completed; the driver and vehicle are available again.").ask()
    except (ValueError, KeyError) as error:
        q.text(str(error)).ask()
