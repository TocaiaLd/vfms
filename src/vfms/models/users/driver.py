from collections.abc import Iterator

from vfms.enums.driver_status import DriverStatus
from vfms.models.trip import Trip
from vfms.enums.vehicle_license import VehicleLicense
from vfms.models.users.person import Person

# represents a driver signed on system
class Driver(Person):
    # A registered driver, including license, status, and trip history.
    def __init__(
        self            : Driver,
        name            : str,
        cpf             : str | int,
        license         : VehicleLicense,
        xp              : int | float | str,
        status          : DriverStatus,
        trip_history    : list[Trip] | None = None,
    ) -> None:
        super().__init__(name, cpf)
        
        self.license                        = license
        self.xp                             = xp
        self.status                         = status
        self.trip_history                   = trip_history if trip_history is not None else []

    @property
    def trip_history(self) -> list[Trip]:
        return self._trip_history

    @trip_history.setter
    def trip_history(self, value: list[Trip]) -> None:
        if not isinstance(value, list):
            raise TypeError("trip_history must be a list")
        self._trip_history = value

    @property
    def license(self) -> VehicleLicense:
        return self._license

    @license.setter
    def license(self, value: VehicleLicense | str) -> None:
        new_value = value
        
        if not isinstance(new_value, VehicleLicense):
            try:
                new_value = (
                    VehicleLicense[new_value]
                    if isinstance(new_value, str) and new_value in VehicleLicense.__members__
                    else VehicleLicense(new_value)
                )
            except (TypeError, ValueError):
                raise TypeError("the license is not from VehicleLicense type") from None
        
        self._license = new_value

    @property
    def xp(self) -> int:
        return self._xp 

    @xp.setter
    def xp(self, value: int | float | str) -> None:
        if isinstance(value, bool):
            raise ValueError("the experience must be an integer")
        if not isinstance(value, int):
            try:
                n_value = float(value)
                value = int(value)
                
                r = n_value - value

                if r != 0:
                    raise ValueError("the experience must be a int number")
                                
            except (TypeError, ValueError, OverflowError) as exc:
                raise ValueError("The experience must be an integer") from exc
        
        # the firts car was created at 1888
        if value < 0:
            raise ValueError("the experience must be greater than zero")

        self._xp = value

    @property
    def status(self) -> DriverStatus:
        return self._status

    @status.setter
    def status(self, value: DriverStatus | str) -> None:
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
    def __lt__(self, other: Driver) -> bool:
        return self.xp < other.xp

    # Special method to iterate the driver trips
    def __iter__(self) -> Iterator[Trip]:
        return iter(self.trip_history)
