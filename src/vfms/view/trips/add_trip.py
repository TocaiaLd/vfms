# external libs
import questionary as q

# utilities
from vfms.utilities.clear_screen import clear_screen

# project imports
from vfms.models.users.driver import Driver
from vfms.models.vehicles.vehicle import Vehicle
from vfms.depedencies import MasterController

def show_drivers() -> None:
    response = MasterController.DRIVER_CONTROLLER.value.show_drivers()

    print(response)

def show_vehicles(type) -> str:
    response = None

    if type == "cars":
        response = MasterController.CAR_CONTROLLER.value.show_cars()
    elif type == "trucks":
        response = MasterController.TRUCK_CONTROLLER.value.show_trucks()
    elif type == "motorcycles":
        response = MasterController.MOTORCYCLE_CONTROLLER.value.show_motorcycles()

    print(response)

def loop_driver() -> bool:
    while loop_driver:
        show_drivers()
        driver_to_add_trip = q.text("Write the cpf of the driver that you want to add a trip: ").ask()
        driver_exists = MasterController.DRIVER_CONTROLLER.value.driver_exists(driver_to_add_trip)

        if not driver_exists:
            q.text("This driver does not exists, please digit the corret cpf. press any key to continue").ask()
        elif driver_exists:
            driver_available = MasterController.DRIVER_CONTROLLER.value.driver_is_available(driver_to_add_trip)

            if driver_available:
                return False
            else:
                q.text("This driver is not available, please select other driver. press any key to continue").ask()

        clear_screen()

def loop_vehicle(input) -> bool:
    vehicle_controller = None

    if input == "cars":
        vehicle_controller = MasterController.CAR_CONTROLLER.value
    elif input == "trucks":
        vehicle_controller = MasterController.TRUCK_CONTROLLER.value
    elif input == "motorcycles":
        vehicle_controller = MasterController.MOTORCYCLE_CONTROLLER.value
    
    while loop_vehicle:
        show_vehicles(input)
        vehicle_to_add_trip = q.text(f"Write the plate of the {input} that you want to add a trip: ").ask()
        vehicle_exists = vehicle_controller.vehicle_exists(vehicle_to_add_trip)

        if not vehicle_exists:
            q.text("This vehicle does not exists, please digit the corret plate. press any key to continue").ask()
        elif vehicle_exists:
            vehicle_available = vehicle_controller.vehicle_is_available(vehicle_to_add_trip)

            if vehicle_available:
                return False
            else:
                q.text("This vehicle is not available, please select other vehicle. press any key to continue").ask()

        clear_screen()

def add_trip():
    running = True

    while running:
        input = q.select(
            "Choose a vehicle type to add a trip:",
            choices = [
                q.Choice(
                    title   = "Car", 
                    value   = "cars"
                ), 
                q.Choice(
                    title   = "Truck", 
                    value   = "trucks"
                ), 
                q.Choice(
                    title   = "Motorcycle", 
                    value   = "motorcycles"
                ), 
                q.Choice(
                    title   = "Back to the previous page", 
                    value   = False
                ), 
            ]
        ).ask()
        
        if not input:
            running = False
            return not running

        checks_vehicle  = loop_vehicle(input)
        checks_driver   = loop_driver()

        if not checks_vehicle and not checks_driver:
            print(checks_vehicle)
            print(checks_driver)
            # save trip here
        
        # q.text(f"{response}. Press any key to continue...").ask()

        # clear_screen()
