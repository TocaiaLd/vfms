# External libs
import questionary as q

# Project imports
from vfms.utilities.clear_screen import clear_screen
from vfms.utilities.close_program import close_program
# from vfms.view.reports.menu_reports import menu_reports
# from vfms.view.trips.menu_trips import menu_trips
# from vfms.view.drivers.menu_drivers import menu_drivers
from vfms.view.vehicles.menu_vehicles import menu_vehicles

def menu():    
    running = True

    while running: 
        input = q.select(
            message = "|----- Main Menu -----|",
            choices = [
                q.Choice(
                    title   = "Vehicles",
                    value   = menu_vehicles
                ), 
                # q.Choice(
                #     title   = "Reports",
                #     value   = menu_reports
                # ), 
                # q.Choice(
                #     title   = "Drivers",
                #     value   = menu_drivers
                # ), 
                # q.Choice(
                #     title   = "Trips",
                #     value   = menu_trips
                # ), 
                # q.Choice(
                #     title   = "New driver",
                #     value   = page_new_driver
                # ), 
                # q.Choice(
                #     title   = "Show drivers",
                #     value   = page_show_drivers
                # ), 
                # q.Choice(
                #     title   = "Search driver by cpf",
                #     value   = page_show_driver_by_cpf
                # ), 
                q.Choice(
                    title   = "Close Program", 
                    value   = close_program
                ), 
            ]
        ).ask()

        clear_screen()
        running = input()




