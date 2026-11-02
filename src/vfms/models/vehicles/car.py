from vfms.models.vehicles.vehicle import Vehicle
from vfms.enums.vehicle_status import VehicleStatus
from vfms.enums.vehicle_license import VehicleLicense

class Car(Vehicle):
    # A passenger car with a configured number of ports.
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
        license             : VehicleLicense = VehicleLicense.B,
    ) -> None:
        super().__init__(plate, model, brand, year, mileage, average_consumption, status, max_fuel, fuel)
        
        self.ports      = ports
        self.license    = license

    # Ports encapsulation
    @property
    def ports(self) -> int:
        return self._ports

    @ports.setter
    def ports(self, value: int | float | str) -> None:
        if isinstance(value, bool):
            raise ValueError("Ports must be an integer")
        new_value = value
        if not isinstance(value, int):
            try:
                number = float(value)
                if not number.is_integer():
                    raise ValueError("Ports must be an integer")
                new_value = int(number)
            except (TypeError, ValueError, OverflowError) as exc:
                raise ValueError("Not an int") from exc
        if new_value <= 0:
            raise ValueError("Ports must be greater than zero")
        
        self._ports= new_value

    def to_dict(self) -> dict[str, dict[str, str | int | float]]:
        d = super().to_dict()
        
        for plate, data in d.items():
            data.update({
            "ports"     : self.ports,
            "license"   : self.license.name
            })

        return d

    # Special method used by print(v), where v is a Car object
    def __str__(self) -> str:
        text = super().__str__()
        return f"""{text}
License: {self.license.name}
Number of ports: {self.ports}"""
    
    # Special method used by repr(v), where v is a Car object
    def __repr__(self) -> str:
        text = super().__repr__()
        text = text.replace(")", "")
        return f"{text}, license_category={self.license.name}, ports={self.ports})"
