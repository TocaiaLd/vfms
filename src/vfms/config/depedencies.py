# standart libs
from enum import Enum

# vehicles classes imports
from vfms.repos.vehicle_repo import VehicleRepo
from vfms.controllers.vehicle_controller import VehicleController

vehicle_repo        = VehicleRepo()
vehicle_controller  = VehicleController(vehicle_repo)

# driver classes imports
from vfms.repos.driver_repo import DriverRepo
from vfms.controllers.driver_controller import DriverController

driver_repo         = DriverRepo()
driver_controller   = DriverController(driver_repo)

# trip classes imports
from vfms.repos.trip_repo import TripRepo
from vfms.controllers.trip_controller import TripController

trip_repo           = TripRepo()
trip_controller     = TripController(trip_repo)

class MasterController(Enum):
    VEHICLE_CONTROLLER = vehicle_controller
    DRIVER_CONTROLLER   = driver_controller
    TRIP_CONTROLLER       = trip_controller