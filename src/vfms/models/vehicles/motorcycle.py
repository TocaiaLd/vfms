from vfms.models.vehicles.vehicle import Vehicle
from vfms.enums.vehicle_status import VehicleStatus
from vfms.enums.vehicle_license import VehicleLicense

class Motorcycle(Vehicle):
    def __init__(
        self                : Motorcycle,
        plate               : str,
        model               : str,
        brand               : str,
        year                : int,
        mileage             : float,
        average_consumption : float,
        status              : VehicleStatus,
        max_fuel            : float,
        fuel                : float,
        cc                  : int,
        license             = VehicleLicense.A,
    ):
        super().__init__(plate, model, brand, year, mileage, average_consumption, status, max_fuel, fuel)
        self.cc = cc
        self.license = license

    # CC encapsulation
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

    def to_dict(self) -> dict:
        d = super().to_dict()
    
        for plate, data in d.items():
            data.update({
            "cc"                : self.cc,
            "license"           : self.license.name
            })

        return d
        
    # Special method used by print(v), where v is a Motorcycle object
    def __str__(self) -> str:
        text = super().__str__()
        text = text.replace(")", "")
        return f"""{text}
license category: {self.license.name}
cc: {self.cc}"""
    
    # Special method used by repr(v), where v is a Motorcycle object
    def __repr__(self) -> str:
        text = super().__repr__()
        text = text.replace(")", "")
        return f"{text}, license_category={self.license.name}, cc={self.cc})"
