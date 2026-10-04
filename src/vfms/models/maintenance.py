from vfms.enums.enum_maintenance import EnumMaintenance
import datetime

class Maintenance:
    def __init__(
        self, 
        date  : datetime.date,
        type  : EnumMaintenance,
        coast : float,
        description : str,
    ):
        self.date = datetime.datetime.now()
        self.type = type
        self.coast = coast
        self.description = description
