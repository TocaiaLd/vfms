import pytest

from vfms.models.vehicles.truck import Truck
from vfms.models.vehicles.motorcicle import Motorcicle
from vfms.models.vehicles.car import Car

from vfms.enums import VehicleStatus

# v = Vehicle("HPM-2A74", "Gol", "Volkswagen", 1990, 1000000, 8.9, VehicleStatus.AVAILABLE, VehicleLicense.A, [])

# v = Car("HPM-2A74", "Gol", "Volkswagen", 1990, 1000000, 8.9, VehicleStatus.AVAILABLE, [], 4)

v = Motorcicle("HPM-2A74", "Gol", "Volkswagen", 1990, 1000000, 8.9, VehicleStatus.AVAILABLE, [], 150)

# v = Truck("HPM-2A74", "Gol", "Volkswagen", 1990, 1000000, 8.9, VehicleStatus.AVAILABLE, [], 150)

# print(v)
# print(repr(v))

print(repr(v))

