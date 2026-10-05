from vfms.models.maintenance import Maintenance
from vfms.models.vehicles.vehicle import Vehicle
from vfms.enums.vehicle_status import VehicleStatus
from vfms.enums.vehicle_license import VehicleLicense

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
        maintenance_h       : list[Maintenance] | [],
        cc                  : int,
        license_category    = VehicleLicense.A,
    ):
        super().__init__(plate, model, brand, year, mileage, average_consumption, status, maintenance_h)
        self.cc = cc
        self.license_category = license_category

    """
    cc encapsulation
    """
    @property
    def cc(self):
        return self._cc

    @cc.setter
    def cc(self, value):
        new_value = value

        if not isinstance(new_value, int):
            try:
                new_value = int(new_value)
            except:
                raise ValueError("Not a int")
        
        self._cc= new_value

    """
    Special method to uses with print(v), where v is a Motorcile class
    """
    def __str__(self) -> str:
        text = super().__str__()
        text = text.replace(")", "")
        return f"""{text}
license category: {self.license_category.name}
cc: {self.cc}"""
    
    """
    Special method to uses with print(repr(v)), where v is a Motorcile class
    """
    def __repr__(self) -> str:
        text = super().__repr__()
        text = text.replace(")", "")
        return f"{text}, license_category={self.license_category.name}, cc={self.cc})"