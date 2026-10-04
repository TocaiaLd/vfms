from vfms.models.maintenance import Maintenance
from vfms.models.vehicles.vehicle import Vehicle
from vfms.enums.vehicle_status import VehicleStatus
from vfms.enums.license_type import VehicleLicense

class Car(Vehicle):
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
        maintenance_h       : Maintenance,
        ports               : int
    ):
        super().__init__(plate, model, brand, year, mileage, average_consumption, status, license_category, maintenance_h)
        self.ports = ports