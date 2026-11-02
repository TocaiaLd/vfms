from vfms.models.vehicles.vehicle import Vehicle
from vfms.enums.vehicle_status import VehicleStatus
from vfms.enums.vehicle_license import VehicleLicense
from math import isfinite

class Truck(Vehicle):
    # A truck with a maximum cargo weight.
    def __init__(
        self                : Truck,
        plate               : str,
        model               : str,
        brand               : str,
        year                : int,
        mileage             : float,
        average_consumption : float,
        status              : VehicleStatus,
        max_fuel            : float,
        fuel                : float,
        max_weight          : float,
        license             : VehicleLicense = VehicleLicense.C,
    ) -> None:
        super().__init__(plate, model, brand, year, mileage, average_consumption, status, max_fuel, fuel)
        self.max_weight = max_weight
        self.license = license

    # Max weight encapsulation
    @property
    def max_weight(self) -> float:
        return self._max_weight

    @max_weight.setter
    def max_weight(self, value: int | float | str) -> None:
        new_value = value

        if not isinstance(new_value, float):
            try:
                new_value = float(new_value)
            except (TypeError, ValueError, OverflowError) as exc:
                raise ValueError("Not a float") from exc
        if not isfinite(new_value) or new_value <= 0:
            raise ValueError("Maximum weight must be greater than zero")
        
        self._max_weight= new_value

    def to_dict(self) -> dict[str, dict[str, str | int | float]]:
        d = super().to_dict()
        
        for plate, data in d.items():
            data.update({
            "license"           : self.license.name,
            "max_weight"        : self.max_weight
            })

        return d

    # Special method used by print(v), where v is a Truck object
    def __str__(self) -> str:
        text = super().__str__()
        return f"""{text}
license category: {self.license.name}
max_weight: {self.max_weight}t"""
    
    # Special method used by repr(v), where v is a Truck object
    def __repr__(self) -> str:
        text = super().__repr__()
        text = text.replace(")", "")
        return f"{text}, license={self.license.name}, max_weight={self.max_weight}t)"
