# external libs
import questionary as q
from tabulate import tabulate

# Project imports
from vfms.config.depedencies import MasterController

def page_select_vehicles_to_show():
    i = q.select(
        "Choose a vehicle type:",
        choices = [
            q.Choice(
                title   = "Show only cars", 
                value   = "Car"
            ), 
            q.Choice(
                title   = "Show only trucks", 
                value   = "Truck"
            ), 
            q.Choice(
                title   = "Show only motorcycles", 
                value   = "Motorcycle"
            ),
            q.Choice(
                title   = "Show all vehicles", 
                value   = "vehicles"
            ),  
            q.Choice(
                title   = "Back to homepage", 
                value   = 0
            ), 
        ]
    ).ask()

    if i == 0:
        return
    else:
        response = MasterController.VEHICLE_CONTROLLER.value.show_vehicles(what=i)

    collumns = ["Plate", "Model", "Brand", "Year", "Mileage", "Consumption", "Status", "Fuel"]
    data = []

    for v in response:
        data.append([v.plate, v.model, v.brand, v.year, v.mileage, v.average_consumption, v.status.name, v.fuel])
    
    print(tabulate(data, headers=collumns, tablefmt="fancy_grid"))

    q.text("Press a key to go back").ask()
