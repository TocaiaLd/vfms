from vfms.models.vehicles.vehicle import Vehicle
from vfms.enums.vehicle_status import VehicleStatus
from vfms.enums.vehicle_license import VehicleLicense

class Motorcycle(Vehicle):
    # A motorcycle with engine capacity in cubic centimeters.
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
        license             : VehicleLicense = VehicleLicense.A,
    ) -> None:
        super().__init__(plate, model, brand, year, mileage, average_consumption, status, max_fuel, fuel)
        self.cc = cc
        self.license = license

    # CC encapsulation
    @property
    def cc(self) -> int:
        return self._cc

    @cc.setter
    def cc(self, value: int | float | str) -> None:
        if isinstance(value, bool):
            raise ValueError("Engine capacity must be an integer")
        new_value = value
        if not isinstance(value, int):
            try:
                number = float(value)
                if not number.is_integer():
                    raise ValueError("Engine capacity must be an integer")
                new_value = int(number)
            except (TypeError, ValueError, OverflowError) as exc:
                raise ValueError("Not an int") from exc
        if new_value <= 0:
            raise ValueError("Engine capacity must be greater than zero")
        
        self._cc= new_value

    def to_dict(self) -> dict[str, dict[str, str | int | float]]:
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
        return f"""{text}
license category: {self.license.name}
cc: {self.cc}"""
    
    # Special method used by repr(v), where v is a Motorcycle object
    def __repr__(self) -> str:
        text = super().__repr__()
        text = text.replace(")", "")
        return f"{text}, license_category={self.license.name}, cc={self.cc})"
