# external libs
import questionary as q

# Project imports
from vfms.config.depedencies import MasterController

def page_show_drivers():
    response = MasterController.DRIVER_CONTROLLER.value.show_drivers()

    for item in response:
        print(repr(item))

    q.text("Press a key to quit").ask()

