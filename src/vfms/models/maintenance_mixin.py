# standard libs
import datetime

from vfms.enums.enum_maintenance import EnumMaintenance

class MaintenanceMixin:
    def new_maintenance(
        self        : MaintenanceMixin, 
        type        : EnumMaintenance,
        price       : float,
        description : str,
        date        : datetime.datetime | str | None = None,
    ) -> tuple[str, EnumMaintenance, float, str, str, str]:
        plate = getattr(self, 'plate', "")
        
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
        self.date_init = date or datetime.datetime.now().isoformat(timespec="seconds")
        self.date_end = "..."

        return (plate, self.type.value, self.price, self.description, self.date_init, self.date_end)

