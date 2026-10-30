# External libs
import questionary as q

from vfms.view.drivers.delete_driver import delete_driver
from vfms.view.drivers.show_drivers import page_show_drivers
from vfms.view.drivers.new_driver import page_new_driver
from vfms.view.drivers.show_driver_by_cpf import page_show_driver_by_cpf

def menu_drivers():
    running = True

    while running:
        input = q.select(
            message = "|----- Drivers Menu -----|",
            choices = [
                q.Choice(
                    title   = "New driver",
                    value   = page_new_driver
                ), 
                q.Choice(
                    title   = "Show drivers",
                    value   = page_show_drivers
                ), 
                q.Choice(
                    title   = "Search driver by cpf",
                    value   = page_show_driver_by_cpf
                ), 
                q.Choice(
                    title   = "Delete a driver", 
                    value   = delete_driver
                ), 
                q.Choice(
                    title   = "Back to main menu", 
                    value   = False
                ),
            ]
        ).ask()

        if not input:
            running = False
            return False

        input()    

        