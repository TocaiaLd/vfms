from vfms.enums.license_type import VehicleLicense
from vfms.enums.vehicle_status import VehicleStatus

from vfms.models.vehicles.vehicle import Vehicle

v = Vehicle("palte", "123", "123", 123, 123, 123, VehicleStatus.AVAILABLE, VehicleLicense.A)
v2 = Vehicle("teste", "123", "123", 123, 123, 123, VehicleStatus.AVAILABLE, VehicleLicense.A)

print(v)

print(repr(v))

print(v == v2)
