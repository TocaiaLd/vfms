# external libs
import questionary as q

# Utilities
from vfms.enums.driver_status import DriverStatus
from vfms.enums.vehicle_license import VehicleLicense
from vfms.utilities.clear_screen import clear_screen

# Project imports
from vfms.depedencies import MasterController

def update_driver() -> None:
    loop_update = True

    while loop_update:
        response = MasterController.DRIVER_CONTROLLER.value.show_drivers()

        print(response)

        driver_to_update = q.text("Write the cpf of the driver that you want to update: ").ask()

        driver = MasterController.DRIVER_CONTROLLER.value.get_by_cpf(driver_to_update)

        if not driver:
            loop_update = q.confirm("This driver does not exist. Do you want to update another driver?").ask()
            clear_screen()
            continue

        if driver.status != DriverStatus.ON_TRIP:
            name        = q.text(f"New name: (old is {driver.name})").ask()
            license     = q.select(
                f"New license category: (old is {driver.license.name})",
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
            
            status = q.select(
                f"New status: (old is {driver.status.name})",
                [
                    q.Choice(
                        title   = "AVAILABLE",
                        value   = DriverStatus.AVAILABLE
                    ), 
                    q.Choice(
                        title   = "INACTIVE",
                        value   = DriverStatus.INACTIVE
                    ), 
                ]
            ).ask()

            xp          = q.text(f"New experience: (old is {driver.xp})").ask()

            response = MasterController.DRIVER_CONTROLLER.value.update_driver(name, driver_to_update, license, xp, status)

            loop_update = q.confirm(f"{response}. Do you want to edit another?").ask()
            clear_screen()
        else:
            loop_update = q.confirm("This driver is on trip, cannot change it. Do you want to update another driver?").ask()
            clear_screen()
