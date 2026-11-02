# external libs
import questionary as q

# Utilities
from vfms.utilities.clear_screen import clear_screen

# Project imports
from vfms.depedencies import MasterController

def finish_maintenance() -> None:
    loop_finish = True

    while loop_finish:
        response = MasterController.MAINTENANCE_CONTROLLER.value.show_maintenances()

        print(response)

        maintenance_to_finish = q.text("Write the maintenance id that you want to finish: ").ask()

        response = MasterController.MAINTENANCE_CONTROLLER.value.finish_maintenance(maintenance_to_finish)

        loop_finish = q.confirm(f"{response}. Do you want to continue?").ask()

        clear_screen()
