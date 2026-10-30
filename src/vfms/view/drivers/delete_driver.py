# external libs
import questionary as q

# Utilities
from vfms.utilities.clear_screen import clear_screen

# Project imports
from vfms.depedencies import MasterController

def delete_driver():
    loop_delete = True

    while loop_delete:
        response = MasterController.DRIVER_CONTROLLER.value.show_drivers()

        print(response)

        driver_to_delete = q.text("Write the cpf of the driver that you want to delete: ").ask()

        response = MasterController.DRIVER_CONTROLLER.value.delete_driver(driver_to_delete)

        loop_delete = q.confirm(f"{response}. Do you want to continue?").ask()

        clear_screen()
