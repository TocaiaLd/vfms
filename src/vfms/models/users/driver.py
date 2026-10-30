from vfms.enums.driver_status import DriverStatus
from vfms.models.trip import Trip
from vfms.enums.vehicle_license import VehicleLicense
from vfms.models.users.person import Person

# represents a driver signed on system
class Driver(Person):
    def __init__(
        self            : Driver,
        name            : str,
        cpf             : int,
        license         : VehicleLicense,
        xp              : int,
        status          : DriverStatus,
    ):
        super().__init__(name, cpf)
        
        self.license                        = license
        self.xp                             = xp
        self.status                         = status

    @property
    def license(self):
        return self._license

    @license.setter
    def license(self, value):
        new_value = value
        
        if not isinstance(new_value, VehicleLicense):
            if new_value == "A":
                new_value = VehicleLicense.A
            elif new_value == "B":
                new_value = VehicleLicense.B
            elif new_value == "D":
                new_value = VehicleLicense.D
            elif new_value == "AB":
                new_value = VehicleLicense.AB
            elif new_value == "AD":
                new_value = VehicleLicense.AD
            else:
                raise TypeError("the license is not from VehicleLicense type")
        
        self._license = new_value

    @property
    def xp(self):
        return self._xp 

    @xp.setter
    def xp(self, value):
        if not isinstance(value, int):
            try:
                n_value = float(value)
                value = int(value)
                
                r = n_value - value

                if r != 0:
                    raise ValueError("the experience must be a int number")
                                
            except:
                raise ValueError("The experience cannot be a string")
        
        # the firts car was created at 1888
        if value < 0:
            raise ValueError("the experience must be greater than zero")

        self._xp = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        new_value = value
        
        if not isinstance(new_value, DriverStatus):
            if new_value == "AVAILABLE":
                new_value = DriverStatus.AVAILABLE
            elif new_value == "ON_TRIP":
                new_value = DriverStatus.ON_TRIP
            elif new_value == "INACTIVE":
                new_value = DriverStatus.INACTIVE
            else:
                raise TypeError("the status is not from DriverStatus type")
        
        self._status = new_value

    # Special method to uses with print(d), where d is a Driver class
    def __str__(self) -> str:
        text = super().__str__()
    
        return f"""{text}
license: {self.license.name}
experience: {self.xp}
status: {self.status.name}
trip_history: {self.trip_history}"""
    
    # Special method to uses with print(repr(d)), where d is a Driver class
    def __repr__(self) -> str:
        text = super().__repr__()
        text = text.replace(")", "")
        return f"{text}, license={self.license}, xp={self.xp}, status={self.status}, trip_history={self.trip_history})"

    # Special method to sort drivers by xp
    def __lt__(self, other : Driver) -> bool:
        return self.xp < other.xp

    # Special method to iterate the driver trips
    def __iter__(self) -> list[Trip]:
        return iter(self.trip_history)
