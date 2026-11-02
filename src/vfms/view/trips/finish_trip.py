# external libs
import questionary as q

# Utilities
from vfms.utilities.clear_screen import clear_screen

# Project imports
from vfms.depedencies import MasterController

def finish_trip() -> None:
    loop_finish = True

    while loop_finish:
        response = MasterController.TRIP_CONTROLLER.value.show_trips()

        print(response)

        trip_to_finish = q.text("Write the id trip that you want to finish: ").ask()

        response = MasterController.TRIP_CONTROLLER.value.finish_trip(trip_to_finish)

        loop_finish = q.confirm(f"{response}. Do you want to continue?").ask()

        clear_screen()
