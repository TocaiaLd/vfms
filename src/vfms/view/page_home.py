# Standard libs
import os

# External libs
import questionary as q

# Project imports
from vfms.view.page_new_vehicle import page_create_vehicle
from vfms.view.page_show_all_vehicles import page_select_vehicles_to_show
from vfms.view.page_new_driver import page_new_driver
from vfms.view.page_show_driver_by_cpf import page_show_driver_by_cpf
from vfms.view.page_show_drivers import page_show_drivers
from vfms.view.page_add_trip import add_trip
from vfms.view.page_reports import page_reports

RUNNING = True

def page_close_or_come_back() -> bool:
    global RUNNING

    sure = q.confirm("Are you sure?").ask()

    if sure:
        RUNNING = False

def menu():
    
    while RUNNING: 
        input = q.select(
            message         = "|----- Main Menu -----|",
            choices= [
                q.Choice(
                    title   = "New vehicle",
                    value   = page_create_vehicle
                ), 
                q.Choice(
                    title   = "Show vehicles",
                    value   = page_select_vehicles_to_show
                ), 
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
                    title   = "Add trip",
                    value   = add_trip
                ),
                q.Choice(
                    title   = "Reports",
                    value   = page_reports
                ), 
                q.Choice(
                    title   = "Close Program", 
                    value   = page_close_or_come_back
                ), 
            ]
        ).ask()

        input()

        os.system('cls' if os.name == 'nt' else 'clear')


