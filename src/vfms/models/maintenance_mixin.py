# standard libs
import datetime
from math import isfinite

from vfms.enums.enum_maintenance import EnumMaintenance
from vfms.exceptions import ManutencaoInvalidaError

class MaintenanceMixin:
    # Create and expose maintenance records for a vehicle.
    @property
    def type(self) -> EnumMaintenance:
        return self._type

    @type.setter
    def type(self, value: EnumMaintenance) -> None:
        if not isinstance(value, EnumMaintenance):
            raise ManutencaoInvalidaError("type must be an EnumMaintenance")
        self._type = value

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        amount = float(value)
        if not isfinite(amount) or amount < 0:
            raise ManutencaoInvalidaError("Cost must be a finite non-negative number")
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
        type        : EnumMaintenance | str,
        price       : float,
        description : str,
        date        : datetime.datetime | str | None = None,
    ) -> tuple[str, str, float, str, str, str, float]:
        plate = getattr(self, 'plate', "")
        
        if not isinstance(type, EnumMaintenance):
            try:
                type = EnumMaintenance(type)
            except (TypeError, ValueError):
                raise ManutencaoInvalidaError("Invalid maintenance type") from None
        
        self.type = type
        self.price = price
        self.description = str(description)
        self.date_init = date or datetime.datetime.now().isoformat(timespec="seconds")
        self.date_end = "..."
        record_date = (
            self.date_init.isoformat(timespec="seconds")
            if isinstance(self.date_init, datetime.datetime)
            else self.date_init
        )

        return (
            plate,
            self.type.value,
            self.price,
            self.description,
            record_date,
            self.date_end,
            float(getattr(self, "mileage", 0.0)),
        )

