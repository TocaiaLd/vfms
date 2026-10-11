# external libs
import questionary as q

# Project imports
from vfms.config.depedencies import MasterController

def page_show_driver_by_cpf():
    search_cpf = q.text("Digit the cpf:").ask()
    
    response = MasterController.DRIVER_CONTROLLER.value.show_driver_by_cpf(search_cpf)
    
    if response:
        print(repr(response))
    else:
        q.text("There is no driver with this cpf")

    q.text("Press any key to continue...").ask()


