# external libs
import questionary as q
from tabulate import tabulate

# Project imports
from vfms.depedencies import MasterController

def page_show_driver_by_cpf():
    search_cpf = q.text("Digit the cpf:").ask()
    
    response = MasterController.DRIVER_CONTROLLER.value.show_driver_by_cpf(search_cpf)
    
    if response:
        collumns = ["Name", "CPF", "License", "Experience", "Status", "Trips History"]
        data = []

        
        data.append([response.name, response.cpf, response.license.name, response.xp, response.status.name, response.trip_history])
    
        print(tabulate(data, headers=collumns, tablefmt="fancy_grid"))
    else:
        q.text("There is no driver with this cpf")

    q.text("Press any key to continue...").ask()


