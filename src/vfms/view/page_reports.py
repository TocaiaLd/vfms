# External libs
import questionary as q
from tabulate import tabulate

from vfms.view.page_add_trip import get_vehicles

def page_vehicle_status_report():
    vehicles = get_vehicles()

    if not vehicles:
        q.text("there are no vehicles, please add at least one to use the reports page. Press any key to go back to the menu").ask()
    

    collumns = ["Plate", "Model", "Status"]
    data = []

    for v in vehicles:
        data.append([v.plate, v.model, v.status.name])

    return collumns, data

def page_reports():
    i = q.select(
        "Choose a vehicle type:",
        choices = [
            q.Choice(
                title   = "Vehicles Status Report", 
                value   = page_vehicle_status_report
            ), 
            # q.Choice(
            #     title   = "Truck", 
            #     value   = truck_asks
            # ), 
            # q.Choice(
            #     title   = "Motorcycle", 
            #     value   = motorcycle_asks
            # ), 
            q.Choice(
                title   = "Back to homepage", 
                value   = 0
            ), 
        ]
    ).ask()
        
    if i == 0:
        return

    collumns, data = i()

    print(tabulate(data, headers=collumns, tablefmt="fancy_grid"))

    save = q.confirm("Do you want to save the report?").ask()

    if save:
        print("Still in development")

    q.text("Press any key to go to the menu").ask()