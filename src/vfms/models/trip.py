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
    ):
        self.driver_cpf     = driver_cpf
        self.vehicle_plate  = vehicle_plate
        self.origin         = origin
        self.destiny        = destiny
        self.distance       = distance
        self.status         = status


    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        new_value = value
        
        if not isinstance(new_value, EnumTrip):
            if new_value == "In progress" or new_value == "IN_PROGRESS":
                new_value = EnumTrip.IN_PROGRESS
            elif new_value == "Ended" or new_value == "ENDED":
                new_value = EnumTrip.ENDED
            else:
                raise TypeError("the status trip is not from EnumTrip type")
        
        self._status = new_value

    def set_date_init(self):
        self.date_init= datetime.now()

    def set_date_end(self):
        self.date_end = datetime.now()
