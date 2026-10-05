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
        maintenance_h       : list[Maintenance] | [],
        ports               : int
    ):
        super().__init__(plate, model, brand, year, mileage, average_consumption, status, license_category, maintenance_h)
        self.ports = ports

    """
    ports encapsulation
    """
    @property
    def ports(self):
        return self._ports

    @ports.setter
    def ports(self, value):
        new_value = value

        if not isinstance(new_value, int):
            try:
                new_value = int(new_value)
            except:
                raise ValueError("Not a int")
        
        self._ports= new_value

    """
    Special method to uses with print(v), where v is a Car class
    """
    def __str__(self) -> str:
        text = super().__str__()
        text = text.replace(")", "")
        return f"""{text}
ports: {self.ports})"""
    
    """
    Special method to uses with print(repr(v)), where v is a Car class
    """
    def __repr__(self) -> str:
        text = super().__repr__()
        text = text.replace(")", "")
        return f"{text}, ports={self.ports})"