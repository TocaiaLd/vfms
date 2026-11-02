from typing import Any

# External libs
import questionary as q
from tabulate import tabulate

from vfms.depedencies import MasterController

def page_vehicle_status_report() -> tuple[list[str], list[list[Any]]]:
    vehicle_rows = []
    for controller, show_method in (
        (MasterController.CAR_CONTROLLER.value, "show_cars"),
        (MasterController.TRUCK_CONTROLLER.value, "show_trucks"),
        (MasterController.MOTORCYCLE_CONTROLLER.value, "show_motorcycles"),
    ):
        vehicle_rows.extend(getattr(controller.repo, show_method)())

    if not vehicle_rows:
        q.text("there are no vehicles, please add at least one to use the reports page. Press any key to go back to the menu").ask()
        return ["Plate", "Model", "Brand", "Year", "Mileage", "Consumption", "Status", "Max fuel", "Fuel"], []

    collumns = ["Plate", "Model", "Brand", "Year", "Mileage", "Consumption", "Status", "Max fuel", "Fuel"]
    data = [list(row[:9]) for row in vehicle_rows]

    return collumns, data

def page_reports() -> None:
    i = q.select(
        "Choose a report type:",
        choices = [
            q.Choice(
                title   = "Report - All vehicles", 
                value   = page_vehicle_status_report
            ), 
            q.Choice(
                title   = "Back to homepage", 
                value   = 0
            ), 
        ]
    ).ask()
        
    if not callable(i):
        return

    collumns, data = i()

    print(tabulate(data, headers=collumns, tablefmt="fancy_grid"))

    save = q.confirm("Do you want to save the report?").ask()

    if save:
        print("Still in development")

    q.text("Press any key to go to the menu").ask()
