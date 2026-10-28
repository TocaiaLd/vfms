# Standard libs
from vfms.enums.vehicle_license import VehicleLicense
from vfms.depedencies import MasterController
import questionary as q

# Project imports
from vfms.enums.driver_status import DriverStatus

def page_new_driver():
    name        = q.text("name: ").ask()
    cpf         = q.text("cpf: ").ask()
    license     = q.select(
        "license category:",
        [
            q.Choice(
                title   = "A",
                value   = VehicleLicense.A
            ), 
            q.Choice(
                title   = "B",
                value   = VehicleLicense.B
            ), 
            q.Choice(
                title   = "D", 
                value   = VehicleLicense.D
            ), 
            q.Choice(
                title   = "AB",
                value   = VehicleLicense.AB
            ), 
            q.Choice(
                title   = "AD",
                value   = VehicleLicense.AD
            ), 
        ]
    ).ask()
    xp          = q.text("experience: ").ask()


    request = {
        "name"                  : name,
        "cpf"                   : cpf,
        "license"               : license,
        "xp"                    : xp,
        "status"                : DriverStatus.AVAILABLE,
        "trip_history"          : []
    }

    MasterController.DRIVER_CONTROLLER.value.new_driver(request)
        
    
    
