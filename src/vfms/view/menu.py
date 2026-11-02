# External libs
import questionary as q
import sqlite3

# Project imports
from vfms.utilities.clear_screen import clear_screen
from vfms.utilities.close_program import close_program
from vfms.view.maintenances.menu_maintenances import menu_maintenances
from vfms.view.reports.menu_reports import menu_reports
from vfms.view.trips.menu_trips import menu_trips
from vfms.view.drivers.menu_drivers import menu_drivers
from vfms.view.vehicles.menu_vehicles import menu_vehicles
from vfms.exceptions import RepositorioError

def menu() -> None:
    running = True

    while running:
        clear_screen()
        selection = q.select(
                message = "|----- Main Menu -----|",
                choices = [
                    q.Choice(
                        title   = "Vehicles",
                        value   = menu_vehicles
                    ), 
                    q.Choice(
                        title   = "Maintenances",
                        value   = menu_maintenances
                    ), 
                    q.Choice(
                        title   = "Drivers",
                        value   = menu_drivers
                    ), 
                    q.Choice(
                        title   = "Trips",
                        value   = menu_trips
                    ), 
                    q.Choice(
                        title   = "Reports",
                        value   = menu_reports
                    ),
                    q.Choice(
                        title   = "Close Program", 
                        value   = close_program
                    ), 
                ]
        ).ask()

        if selection is None:
            continue

        if selection is close_program:
            running = selection()
            continue

        try:
            selection()
        except (ValueError, TypeError, sqlite3.Error, RepositorioError) as exc:
            print(f"Operation could not be completed: {exc}")
            q.text("Press any key to return to the main menu").ask()




