from vfms.enums.enum_maintenance import EnumMaintenance
import datetime

class Maintenance:
    def __init__(
        self, 
        type  : EnumMaintenance,
        coast : float,
        description : str,
        date  = datetime.datetime.now(),
    ):
        self.type = type
        self.coast = coast
        self.description = description

