from datetime import datetime

from vfms.enums.enum_trip import EnumTrip

class Trip:
    # Represents a trip taken by a driver in a vehicle
    def __init__(
        self            : Trip,
        driver_cpf      : str,
        vehicle_plate   : str,
        origin          : str,
        destiny         : str,
        distance        : float,
        status          : EnumTrip,
    ) -> None:
        self.driver_cpf     = driver_cpf
        self.vehicle_plate  = vehicle_plate
        self.origin         = origin
        self.destiny        = destiny
        self.distance       = distance
        self.status         = status

    @property
    def driver_cpf(self) -> str:
        return self._driver_cpf

    @driver_cpf.setter
    def driver_cpf(self, value: str) -> None:
        self._driver_cpf = str(value)

    @property
    def vehicle_plate(self) -> str:
        return self._vehicle_plate

    @vehicle_plate.setter
    def vehicle_plate(self, value: str) -> None:
        self._vehicle_plate = str(value)

    @property
    def origin(self) -> str:
        return self._origin

    @origin.setter
    def origin(self, value: str) -> None:
        self._origin = str(value)

    @property
    def destiny(self) -> str:
        return self._destiny

    @destiny.setter
    def destiny(self, value: str) -> None:
        self._destiny = str(value)

    @property
    def distance(self) -> float:
        return self._distance

    @distance.setter
    def distance(self, value: float) -> None:
        self._distance = float(value)

    @property
    def date_init(self) -> datetime | None:
        return self._date_init

    @date_init.setter
    def date_init(self, value: datetime | None) -> None:
        if value is not None and not isinstance(value, datetime):
            raise TypeError("date_init must be a datetime or None")
        self._date_init = value

    @property
    def date_end(self) -> datetime | None:
        return self._date_end

    @date_end.setter
    def date_end(self, value: datetime | None) -> None:
        if value is not None and not isinstance(value, datetime):
            raise TypeError("date_end must be a datetime or None")
        self._date_end = value


    @property
    def status(self) -> EnumTrip:
        return self._status

    @status.setter
    def status(self, value: EnumTrip | str) -> None:
        new_value = value
        
        if not isinstance(new_value, EnumTrip):
            if new_value == "In progress" or new_value == "IN_PROGRESS":
                new_value = EnumTrip.IN_PROGRESS
            elif new_value == "Ended" or new_value == "ENDED":
                new_value = EnumTrip.ENDED
            else:
                raise TypeError("the status trip is not from EnumTrip type")
        
        self._status = new_value

    def set_date_init(self) -> None:
        self.date_init = datetime.now()

    def set_date_end(self) -> None:
        self.date_end = datetime.now()
