# standard libs
import datetime

from vfms.enums.enum_maintenance import EnumMaintenance

class MaintenanceMixin:
    def __init__(
        self, 
        type  : EnumMaintenance,
        price : float,
        description : str,
        date  = datetime.datetime.now(),
    ):
        self.type = type
        self.price = price
        self.description = description

