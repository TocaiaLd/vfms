from vfms.models.vehicles.vehicle import Vehicle
from vfms.enums.vehicle_status import VehicleStatus
from vfms.enums.license_type import VehicleLicense

class Motorcicle(Vehicle):
    def __init__(
        self,
        plate               : str | None,
        model               : str,
        brand               : str,
        year                : int,
        mileage             : float,
        average_consumption : float,
        status              : VehicleStatus,
        license_category    : VehicleLicense,
        cc                  : int
    ):
        super().__init__(plate, model, brand, year, mileage, average_consumption, status, license_category)
        self.cc = cc