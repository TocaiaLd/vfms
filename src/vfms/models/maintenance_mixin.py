# standard libs
import datetime

from vfms.enums.enum_maintenance import EnumMaintenance

class MaintenanceMixin:
    @property
    def type(self) -> EnumMaintenance:
        return self._type

    @type.setter
    def type(self, value: EnumMaintenance) -> None:
        if not isinstance(value, EnumMaintenance):
            raise TypeError("type must be an EnumMaintenance")
        self._type = value

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        amount = float(value)
        if amount < 0:
            raise ValueError("Cost cannot be negative")
        self._price = amount

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        self._description = str(value)

    @property
    def date_init(self) -> datetime.datetime | str:
        return self._date_init

    @date_init.setter
    def date_init(self, value: datetime.datetime | str) -> None:
        if not isinstance(value, (datetime.datetime, str)):
            raise TypeError("date_init must be a datetime or string")
        self._date_init = value

    @property
    def date_end(self) -> str:
        return self._date_end

    @date_end.setter
    def date_end(self, value: str) -> None:
        self._date_end = str(value)

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
        self.price = price
        self.description = str(description)
        self.date_init = date or datetime.datetime.now().isoformat(timespec="seconds")
        self.date_end = "..."

        return (plate, self.type.value, self.price, self.description, self.date_init, self.date_end)

