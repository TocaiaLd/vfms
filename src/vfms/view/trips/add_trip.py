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

def show_vehicles(vehicle_controller, type) -> str:
    response = None
   
    if type == "cars":
        response = vehicle_controller = MasterController.CAR_CONTROLLER.value.show_cars()
    elif type == "trucks":
        response = vehicle_controller = MasterController.TRUCK_CONTROLLER.value.show_trucks()
    elif type == "motorcycles":
        response = vehicle_controller = MasterController.MOTORCYCLE_CONTROLLER.value.show_motorcycles()

    print(response)

def loop_driver() -> str | False:
    loop = True

    while loop:
        show_drivers()
        driver_to_add_trip = q.text("Write the cpf of the driver that you want to add a trip: ").ask()
        driver_exists = MasterController.DRIVER_CONTROLLER.value.driver_exists(driver_to_add_trip)

        if not driver_exists:
            loop = q.confirm("This driver does not exists. Do you want to select another driver?").ask()
        elif driver_exists:
            driver_available = MasterController.DRIVER_CONTROLLER.value.driver_is_available(driver_to_add_trip)

            if driver_available:
                return driver_to_add_trip
            else:
                loop = q.confirm("This driver is not available. Do you want to select other driver?").ask()

        clear_screen()

    return loop

def loop_vehicle(vehicle_controller, driver_cpf, type) -> str | False:    
    loop = True

    while loop:
        show_vehicles(vehicle_controller, type)
        vehicle_to_add_trip = q.text(f"Write the plate of the {type} that you want to add a trip: ").ask()
        vehicle_exists = vehicle_controller.vehicle_exists(vehicle_to_add_trip)

        if not vehicle_exists:
            loop = q.confirm("This vehicle does not exists. Do you want to select other vehicle?").ask()
        elif vehicle_exists:
            vehicle_available = vehicle_controller.vehicle_is_available(vehicle_to_add_trip)

            if vehicle_available:
                vehicle_obj = vehicle_controller.get_by_plate(vehicle_to_add_trip)
                driver_obj  = MasterController.DRIVER_CONTROLLER.value.get_by_cpf(driver_cpf)

                if vehicle_obj.license.value % driver_obj.license.value == 0:
                    return vehicle_to_add_trip
                else:
                    q.text("The vehicle license is incompatible. Press any key to return to the vehicle type menu.").ask()
                    loop = False
            else:
                q.confirm("This vehicle is not available. Do you want to select another vehicle?").ask()

        clear_screen()
    
    return loop

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
        
        vehicle_controller = None

        if input == "cars":
            vehicle_controller = MasterController.CAR_CONTROLLER.value
        elif input == "trucks":
            vehicle_controller = MasterController.TRUCK_CONTROLLER.value
        elif input == "motorcycles":
            vehicle_controller = MasterController.MOTORCYCLE_CONTROLLER.value

        if not input:
            running = False
            return not running

        cpf = loop_driver()
        
        if cpf:
            plate = loop_vehicle(vehicle_controller, cpf, input)
            
            if plate:
                origin       = q.text("Write the origin").ask()
                destiny      = q.text("Write the destiny").ask()
                distance     = q.text("Write the mileage of the trip").ask()

                dict_trip = {
                    "driver_cpf"      : cpf,
                    "vehicle_plate"   : plate,
                    "origin"          : origin,
                    "destiny"         : destiny,
                    "distance"        : distance
                }

                response = MasterController.TRIP_CONTROLLER.value.new_trip(dict_trip)

                q.text(f"{response} press any key to return to vehicle selection trip").ask()


        clear_screen()
