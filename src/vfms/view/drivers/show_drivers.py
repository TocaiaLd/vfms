# external libs
import questionary as q
from tabulate import tabulate

# Project imports
from vfms.depedencies import MasterController

def page_show_drivers():
    response = MasterController.DRIVER_CONTROLLER.value.show_drivers()

    collumns = ["Name", "CPF", "License", "Experience", "Status", "Trips History"]
    data = []

    for d in response:
        data.append([d.name, d.cpf, d.license.name, d.xp, d.status.name, d.trip_history])
    
    print(tabulate(data, headers=collumns, tablefmt="fancy_grid"))

    q.text("Press a key to quit").ask()

