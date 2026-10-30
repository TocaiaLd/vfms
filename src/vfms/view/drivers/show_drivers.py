# external libs
import questionary as q

# Project imports
from vfms.utilities.clear_screen import clear_screen
from vfms.depedencies import MasterController

def page_show_drivers():
    response = MasterController.DRIVER_CONTROLLER.value.show_drivers()

    print(response)

    q.text("Press a key to quit").ask()
    
    clear_screen()

