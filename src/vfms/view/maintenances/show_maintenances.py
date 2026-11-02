# external libs
import questionary as q

# Project imports
from vfms.utilities.clear_screen import clear_screen
from vfms.depedencies import MasterController

def show_maintenances() -> None:
    response = MasterController.MAINTENANCE_CONTROLLER.value.show_maintenances()

    print(response)

    q.text("Press a key to quit").ask()
    
    clear_screen()

