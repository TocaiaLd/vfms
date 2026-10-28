from vfms.models.vehicles.vehicle import Vehicle
from vfms.enums.vehicle_status import VehicleStatus
from vfms.enums.vehicle_license import VehicleLicense

class Car(Vehicle):
    def __init__(
        self                : Car,
        plate               : str,
        model               : str,
        brand               : str,
        year                : int,
        mileage             : float,
        average_consumption : float,
        status              : VehicleStatus,
        max_fuel            : float,
        fuel                : float,
        ports               : int,
        license             = VehicleLicense.B,
    ):
        super().__init__(plate, model, brand, year, mileage, average_consumption, status, max_fuel, fuel)
        
        self.ports      = ports
        self.license    = license

    # Ports encapsulation
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

    def to_dict(self) -> dict:
        d = super().to_dict()
        
        for plate, data in d.items():
            data.update({
            "ports"     : self.ports,
            "license"   : self.license_category.name
            })

        return d

    # Special method used by print(v), where v is a Car object
    def __str__(self) -> str:
        text = super().__str__()
        text = text.replace(")", "")
        return f"""{text}
License: {self.license_category.name}
Number of ports: {self.ports}"""
    
    # Special method used by repr(v), where v is a Car object
    def __repr__(self) -> str:
        text = super().__repr__()
        text = text.replace(")", "")
        return f"{text}, license_category={self.license_category.name}, ports={self.ports})"
