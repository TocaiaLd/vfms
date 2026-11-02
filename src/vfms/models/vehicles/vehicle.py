from vfms.models.maintenance_mixin import MaintenanceMixin
from vfms.models.refuel_mixin import RefuelMixin
from vfms.enums.vehicle_status import VehicleStatus
from vfms.enums.vehicle_license import VehicleLicense

class Vehicle(RefuelMixin, MaintenanceMixin):
    def __init__(
        self                : Vehicle,
        plate               : str,
        model               : str,
        brand               : str,
        year                : int,
        mileage             : float,
        average_consumption : float,
        status              : VehicleStatus,
        max_fuel            : float,
        fuel                : float,
    ) -> None:
        if type(self) is Vehicle:
            raise TypeError("You cannot create a Vehicle object directly")

        self.plate                  = plate
        self.model                  = model
        self.brand                  = brand
        self.year                   = year
        self.mileage                = mileage
        self.average_consumption    = average_consumption
        self.status                 = status
        self.max_fuel               = max_fuel
        self.fuel                   = fuel

    @property
    def model(self) -> str:
        return self._model

    @model.setter
    def model(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("model must be a string")
        self._model = value

    @property
    def brand(self) -> str:
        return self._brand

    @brand.setter
    def brand(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("brand must be a string")
        self._brand = value

    @property
    def license_category(self) -> VehicleLicense:
        return self.license

    @property
    def license(self) -> VehicleLicense:
        return self._license

    @license.setter
    def license(self, value: VehicleLicense | str) -> None:
        try:
            if isinstance(value, VehicleLicense):
                self._license = value
            else:
                self._license = VehicleLicense[value] if value in VehicleLicense.__members__ else VehicleLicense(value)
        except (TypeError, ValueError):
            raise ValueError("Not a Vehicle License") from None


    # Plate encapsulation
    @property
    def plate(self) -> str:
        return self._plate

    @plate.setter
    def plate(self, p: str) -> None:
        l = len(p)
        number_positions = [4, 6, 7]

        if l < 8 or l > 8:
            raise IndexError(f"Wrong size of string")


        for i, letter in enumerate(p):
            if i in number_positions:
                try:
                    letter = int(letter)
                except:
                    raise ValueError(f"position {i} must be a integer")
            elif i == 3:
                if not letter == "-":
                    raise ValueError("Not a valid plate")
            else:
                if letter.isdigit():
                    raise ValueError(f"position {i} must be a char")

        self._plate = p

    # Mileage encapsulation
    @property
    def mileage(self) -> float:
        return self._mileage

    @mileage.setter
    def mileage(self, value: int | float | str) -> None:
        new_value = value

        if not isinstance(new_value, float):
            try:
                new_value = float(new_value)
            except:
                raise ValueError("Not a float")

        if new_value < 0:
            raise ValueError("Mileage cannot be less than zero!")

        self._mileage = new_value

    # Year encapsulation
    @property
    def year(self) -> int:
        return self._year

    @year.setter
    def year(self, value: int | float | str) -> None:
        if not isinstance(value, int):
            try:
                n_value = float(value)
                value = int(value)

                r = n_value - value

                if r != 0:
                    raise ValueError("Not a int")

            except:
                raise ValueError("Not a int")

        # the firts car was created at 1888
        if value < 1888:
            raise ValueError("the year of the car must be >= 1888")

        self._year = value

    # Average consumption encapsulation
    @property
    def average_consumption(self) -> float:
        return self._average_consumption

    @average_consumption.setter
    def average_consumption(self, value: int | float | str) -> None:
        new_value = value

        if not isinstance(new_value, float):
            try:
                new_value = float(new_value)
            except:
                raise ValueError("Not a float")

        self._average_consumption= new_value

    # fuel encapsulation
    @property
    def fuel(self) -> float:
        return self._fuel

    @fuel.setter
    def fuel(self, value: int | float | str) -> None:
        new_value = value

        if not isinstance(new_value, float):
            try:
                new_value = float(new_value)
            except:
                raise ValueError("Not a float")

        if new_value < 0:
            raise Exception("Cannot be less than 0")

        if new_value > self.max_fuel:
            raise Exception("Cannot be bigger than max_fuel")

        self._fuel = new_value

    # max_fuel encapsulation
    @property
    def max_fuel(self) -> float:
        return self._max_fuel

    @max_fuel.setter
    def max_fuel(self, value: int | float | str) -> None:
        new_value = value

        if not isinstance(new_value, float):
            try:
                new_value = float(new_value)
            except:
                raise ValueError("Not a float")

        if new_value < 0:
            raise Exception("Cannot be less than 0")

        self._max_fuel= new_value

    # Vehicle status encapsulation
    @property
    def status(self) -> VehicleStatus:
        return self._status

    @status.setter
    def status(self, value: VehicleStatus | str) -> None:
        new_value = value

        if not isinstance(new_value, VehicleStatus):
            if new_value == VehicleStatus.AVAILABLE.name:
                new_value = VehicleStatus.AVAILABLE
            elif new_value == VehicleStatus.INACTIVE.name:
                new_value = VehicleStatus.INACTIVE
            elif new_value == VehicleStatus.MAINTENANCE.name:
                new_value = VehicleStatus.MAINTENANCE
            elif new_value == VehicleStatus.ON_TRIP.name:
                new_value = VehicleStatus.ON_TRIP
            else:
                raise ValueError("Not a Vehicle Status")

        self._status = new_value

    def to_dict(self) -> dict[str, dict[str, str | int | float]]:
        return {
            self.plate: {
                "model"                 : self.model,
                "brand"                 : self.brand,
                "year"                  : self.year,
                "mileage"               : self.mileage,
                "average_consumption"   : self.average_consumption,
                "status"                : self.status.name,
                "license_category"      : self.license_category.name,
                "max_fuel"              : self.max_fuel,
                "fuel"                  : self.fuel
            }
        }

    # Special method to uses with print(v), where v is a Vehicle class
    def __str__(self) -> str:
        return f"""Plate: {self.plate}
Model: {self.model}
Brand: {self.brand}
Year: {self.year}
Mileage: {self.mileage} km
Average Consumption: {self.average_consumption} l/km
Status: {self.status.name}
Max Fuel: {self.max_fuel} l
Fuel: {self.fuel} l"""

    # Special method to uses with print(repr(v)), where v is a Vehicle class
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(plate={self.plate}, model={self.model}, brand={self.brand}, year={self.year}, mileage={self.mileage}km, average_consumption={self.average_consumption}l/km, status={self.status.name}, fuel={self.fuel}l, max_fuel={self.max_fuel}l)"


    # Special method to compare objects using the plate (Ex: v1 == v2 -> v1.plate == v2.plate, where v1 and v2 are from Vehicle class)
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vehicle):
            return NotImplemented
        return self.plate == other.plate

    # special method to sort vehicles by mileage
    def __lt__(self, other : Vehicle) -> bool:
        return self.mileage < other.mileage


