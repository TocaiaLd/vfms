from vfms.enums.driver_status import DriverStatus
from vfms.models.trip import Trip
from vfms.enums import VehicleLicense
from vfms.models.users.person import Person

"""represents a driver signed on system"""
class Driver(Person):
    def __init__(
        self,
        name            : str,
        cpf             : int,
        license         : VehicleLicense,
        xp              : int,
        status          : DriverStatus,
        trip_history    : list[Trip] | []
    ):
        super().__init__(name, cpf)
        self.license = license,
        self.xp                             = xp
        self.status                         = status
        self.trip_history                   = trip_history

    """
    Special method to uses with print(d), where d is a Driver class
    """
    def __str__(self) -> str:
        return f"""Name: {self.name}
cpf: {self.cpf}
license: {self.license}
experience: {self.xp}
status: {self.status.name}
trip_history: {self.trip_history}
"""
    
    """
    Special method to uses with print(repr(d)), where d is a Driver class
    """
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name}, cpf={self.cpf}, license={self.license}, xp={self.xp}), status={self.status}, trip_history={self.trip_history}"

    """
    Special method to compare objects using the cpf (Ex: d1 == d2 -> d1.cpf == v2.cpf, where d1 and d2 are from Driver class)
    """
    def __eq__(self, other : Driver) -> bool:
        return self.cpf == other.cpf

    """
    special method to sort vehicles by mileage
    """
    def __lt__(self, other : Driver) -> bool:
        return self.xp < other.xp

    """
    Special method to iterate the vehicle maintenances
    """
    def __iter__(self) -> list[Trip]:
        return iter(self.trip_history)