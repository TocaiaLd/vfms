# Standard libs
import os

# External libs
import questionary as q

# Project imports
from vfms.view.reports.menu_reports import menu_reports
from vfms.view.trips.menu_trips import menu_trips
from vfms.view.drivers.menu_drivers import menu_drivers
from vfms.view.vehicles.menu_vehicles import menu_vehicles

RUNNING = True

def clear_screen() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')

def page_close_or_come_back() -> None:
    global RUNNING

    sure = q.confirm("Are you sure to close the program?").ask()

    if sure:
        RUNNING = False

def menu():
    
    while RUNNING: 
        input = q.select(
            message         = "|----- Main Menu -----|",
            choices= [
                q.Choice(
                    title   = "Vehicles",
                    value   = menu_vehicles
                ), 
                q.Choice(
                    title   = "Reports",
                    value   = menu_reports
                ), 
                q.Choice(
                    title   = "Drivers",
                    value   = menu_drivers
                ), 
                q.Choice(
                    title   = "Trips",
                    value   = menu_trips
                ), 
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
                    value   = page_close_or_come_back
                ), 
            ]
        ).ask()

        clear_screen()

        input()

        clear_screen()



