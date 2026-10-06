import enum
from vfms.models.maintenance import Maintenance
from vfms.enums.vehicle_status import VehicleStatus
from vfms.enums.vehicle_license import VehicleLicense

class Vehicle:
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
        fuel                = 0.0
    ):
        if type(self) is Vehicle:
            raise TypeError("You cannot create a Vehicle object directly")

        self.plate = plate
        self.model = model
        self.brand = brand
        self.year = year
        self.mileage = mileage
        self.average_consumption = average_consumption
        self.status = status
        self.maintenance_h = maintenance_h
        self.fuel = fuel

    """
    Plate encapsulation
    """
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
                try:
                    if isinstance(int(letter), int):
                        raise ValueError(f"position {i} must be a char")
                except:
                    pass

        self._plate = p

    """
    Mileage encapsulation
    """
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

    """
    Year encapsulation
    """
    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, value):
        new_value = value

        if not isinstance(new_value, int):
            try:
                new_value = int(new_value)
            except:
                raise ValueError("Not a int")
        
        self._year= new_value
    
    """
    Average consumption encapsulation
    """
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

    """
    fuel encapsulation
    """
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
        
        if value < 0:
            raise Exception("Cannot be less than 0")

        self._fuel= new_value


    """
    Vehicle status encapsulation
    """
    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if not isinstance(value, VehicleStatus):
            raise ValueError("Not a Vehicle Status")
        
        self._status = value
    
    """
    Vehicle maintenance history
    """
    @property
    def maintenance_h(self):
        return self._maintenance_h
        
    @maintenance_h.setter
    def maintenance_h(self, value):
        if not isinstance(value, list):
            raise ValueError("It's not a list")
        
        for m in value:
            if not isinstance(m, Maintenance):
                raise ValueError("The list of maintenances has one or more objects that are not from Maintenance class")

        self._maintenance_h = value

    """
    Special method to uses with print(v), where v is a Vehicle class
    """
    def __str__(self) -> str:
        return f"""Plate: {self.plate}
Model: {self.model}
Brand: {self.brand}
Year: {self.year}
Mileage: {self.mileage} km
Average Consumption: {self.average_consumption} l/km
Status: {self.status.name}
Maintenances: {self.maintenance_h}
Fuel: {self.fuel}"""
    
    """
    Special method to uses with print(repr(v)), where v is a Vehicle class
    """
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(plate={self.plate}, model={self.model}, brand={self.brand}, year={self.year}, mileage={self.mileage}km, average_consumption={self.average_consumption}l/km, status={self.status.name}, maintenances={self.maintenance_h}, fuel={self.fuel}l)"

    """
    Special method to compare objects using the plate (Ex: v1 == v2 -> v1.plate == v2.plate, where v1 and v2 are from Vehicle class)
    """
    def __eq__(self, other : Vehicle) -> bool:
        return self.plate == other.plate

    """
    special method to sort vehicles by mileage
    """
    def __lt__(self, other : Vehicle) -> bool:
        return self.mileage < other.mileage

    """
    Special method to iterate the vehicle maintenances
    """
    def __iter__(self) -> list[Maintenance]:
        return iter(self.maintenance_h)
            