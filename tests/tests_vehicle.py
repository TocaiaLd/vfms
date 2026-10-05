from vfms.models.vehicles.truck import Truck
from vfms.models.vehicles.motorcicle import Motorcicle
from vfms.models.vehicles.car import Car
import pytest

from vfms.enums import VehicleStatus
from vfms.enums import VehicleLicense
from vfms.models.vehicles.vehicle import Vehicle

v = Vehicle("HPM-2A74", "Gol", "Volkswagen", 1990, 1000000, 8.9, VehicleStatus.AVAILABLE, VehicleLicense.A, [])

v2 = Car("HPM-2A74", "Gol", "Volkswagen", 1990, 1000000, 8.9, VehicleStatus.AVAILABLE, VehicleLicense.A, [], 4)

v3 = Motorcicle("HPM-2A74", "Gol", "Volkswagen", 1990, 1000000, 8.9, VehicleStatus.AVAILABLE, VehicleLicense.A, [], 150)

v4 = Truck("HPM-2A74", "Gol", "Volkswagen", 1990, 1000000, 8.9, VehicleStatus.AVAILABLE, VehicleLicense.A, [], 150)

# print(v)
# print(repr(v))

print(v4)
print(repr(v4))

