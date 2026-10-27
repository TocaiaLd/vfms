# External libs
import questionary as q
from tabulate import tabulate

from vfms.view.trips.add_trip import get_vehicles

def page_vehicle_status_report():
    vehicles = get_vehicles()

    if not vehicles:
        q.text("there are no vehicles, please add at least one to use the reports page. Press any key to go back to the menu").ask()

    collumns = ["Plate", "Model", "Brand", "Year", "Mileage", "Consumption", "Status", "Fuel", "Maintenances", "Trips"]
    data = []


    for v in vehicles:
        data.append([v.plate, v.model, v.brand, v.year, v.mileage, v.average_consumption, v.status.name, v.fuel, v.maintenance_h, v.trips])

    return collumns, data

def page_reports():
    i = q.select(
        "Choose a report type:",
        choices = [
            q.Choice(
                title   = "Report - All vehicles", 
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