# external libs
import questionary as q
from tabulate import tabulate

# Project imports
from vfms.depedencies import MasterController

def page_show_driver_by_cpf():
    search_cpf = q.text("Digit the cpf:").ask()
    
    response = MasterController.DRIVER_CONTROLLER.value.show_driver_by_cpf(search_cpf)
    
    print(response)

    q.text("Press any key to continue...").ask()


