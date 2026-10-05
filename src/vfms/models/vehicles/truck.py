from vfms.models.maintenance import Maintenance
from vfms.models.vehicles.vehicle import Vehicle
from vfms.enums.vehicle_status import VehicleStatus
from vfms.enums.vehicle_license import VehicleLicense

class Truck(Vehicle):
    def __init__(
        self,
        plate               : str | None,
        model               : str,
        brand               : str,
        year                : int,
        mileage             : float,
        average_consumption : float,
        status              : VehicleStatus,
        maintenance_h       : list[Maintenance] | [],
        max_weight          : float,
        license_category    = VehicleLicense.D,
    ):
        super().__init__(plate, model, brand, year, mileage, average_consumption, status, maintenance_h)
        self.max_weight = max_weight
        self.license_category = license_category

    """
    cc encapsulation
    """
    @property
    def max_weight(self):
        return self._max_weight

    @max_weight.setter
    def max_weight(self, value):
        new_value = value

        if not isinstance(new_value, float):
            try:
                new_value = float(new_value)
            except:
                raise ValueError("Not a float")
        
        self._max_weight= new_value

    """
    Special method to uses with print(v), where v is a Motorcile class
    """
    def __str__(self) -> str:
        text = super().__str__()
        text = text.replace(")", "")
        return f"""{text}
license category: {self.license_category.name}
max_weight: {self.max_weight}t"""
    
    """
    Special method to uses with print(repr(v)), where v is a Motorcile class
    """
    def __repr__(self) -> str:
        text = super().__repr__()
        text = text.replace(")", "")
        return f"{text}, license_category={self.license_category.name}, max_weight={self.max_weight}t)"