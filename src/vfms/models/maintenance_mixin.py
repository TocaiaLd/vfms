# standard libs
import datetime

from vfms.enums.enum_maintenance import EnumMaintenance

class MaintenanceMixin:
    def __init__(
        self, 
        type  : EnumMaintenance,
        price : float,
        description : str,
        date  = None,
    ):
        if not isinstance(type, EnumMaintenance):
            try:
                type = EnumMaintenance(type)
            except (TypeError, ValueError):
                raise ValueError("Invalid maintenance type") from None
        self.type = type
        self.price = float(price)
        if self.price < 0:
            raise ValueError("Cost cannot be negative")
        self.description = str(description)
        self.date = date or datetime.datetime.now().isoformat(timespec="seconds")

    def to_dict(self):
        return {"type": self.type.value, "price": self.price,
                "description": self.description, "date": self.date}

