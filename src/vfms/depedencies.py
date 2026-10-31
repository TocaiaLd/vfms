# standart libs
from enum import Enum

# Repo connection (SQLITE3)
from vfms.repos.repo import Repo
repo = Repo()

# VEHICLES
# Car imports
from vfms.repos.vehicles.car_repo import CarRepo
from vfms.controllers.vehicles.car_controller import CarController
car_repo        = CarRepo(repo)
car_controller  = CarController(car_repo)

# Truck imports
from vfms.repos.vehicles.truck_repo import TruckRepo
from vfms.controllers.vehicles.truck_controller import TruckController
truck_repo        = TruckRepo(repo)
truck_controller  = TruckController(truck_repo)

# Motorcycle imports
from vfms.repos.vehicles.motorcycle_repo import MotorcycleRepo
from vfms.controllers.vehicles.motorcycle_controller import MotorcycleController 
motorcycle_repo        = MotorcycleRepo(repo)
motorcycle_controller  = MotorcycleController(motorcycle_repo)

# driver classes imports
from vfms.repos.driver_repo import DriverRepo
from vfms.controllers.driver_controller import DriverController

driver_repo         = DriverRepo(repo)
driver_controller   = DriverController(driver_repo)

# maintenance classes imports
from vfms.repos.refuel_repo import RefuelRepo
from vfms.controllers.refuel_controller import RefuelController

refuel_repo        = RefuelRepo(repo)
refuel_controller  = RefuelController(refuel_repo)

# trip classes imports
from vfms.repos.trip_repo import TripRepo
from vfms.controllers.trip_controller import TripController

trip_repo           = TripRepo(repo)
trip_controller     = TripController(trip_repo)

class MasterController(Enum):
    CAR_CONTROLLER                = car_controller
    TRUCK_CONTROLLER            = truck_controller
    MOTORCYCLE_CONTROLLER  = motorcycle_controller
    DRIVER_CONTROLLER          = driver_controller
    REFUEL_CONTROLLER          = refuel_controller
    TRIP_CONTROLLER              = trip_controller