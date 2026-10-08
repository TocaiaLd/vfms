from enum import Enum

from vfms.repos.repo import Repo
from vfms.repos.vehicle_repo import VehicleRepo
from vfms.services.vehicle_service import VehicleService
from vfms.controllers.vehicle_controller import VehicleController

vehicle_repo        = VehicleRepo()
vehicle_service     = VehicleService(vehicle_repo)
vehicle_controller  = VehicleController(vehicle_service)

class MasterController(Enum):
    VEHICLE_CONTROLLER = vehicle_controller