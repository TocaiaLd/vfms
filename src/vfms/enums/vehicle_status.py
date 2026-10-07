from enum import Enum

class VehicleStatus(Enum):
    INACTIVE = 0
    AVAILABLE = 1
    ON_TRIP = 2
    MAINTENANCE = 3