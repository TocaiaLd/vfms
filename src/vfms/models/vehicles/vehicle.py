from vfms.enums.vehicle_status import VehicleStatus

class Vehicle:
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
    ):
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


    # Plate encapsulation
    @property
    def plate(self):
        return self._plate

    @plate.setter
    def plate(self, p):
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
    def mileage(self):
        return self._mileage

    @mileage.setter
    def mileage(self, value):
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
    def year(self):
        return self._year

    @year.setter
    def year(self, value):
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
    def average_consumption(self):
        return self._average_consumption

    @average_consumption.setter
    def average_consumption(self, value):
        new_value = value

        if not isinstance(new_value, float):
            try:
                new_value = float(new_value)
            except:
                raise ValueError("Not a float")

        self._average_consumption= new_value

    # fuel encapsulation
    @property
    def fuel(self):
        return self._fuel

    @fuel.setter
    def fuel(self, value):
        new_value = value

        if not isinstance(new_value, float):
            try:
                new_value = float(new_value)
            except:
                raise ValueError("Not a float")

        if new_value < 0:
            raise Exception("Cannot be less than 0")

        self._fuel= new_value

    # Vehicle status encapsulation
    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
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

    def to_dict(self) -> dict:
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
    def __eq__(self, other : Vehicle) -> bool:
        return self.plate == other.plate

    # special method to sort vehicles by mileage
    def __lt__(self, other : Vehicle) -> bool:
        return self.mileage < other.mileage


