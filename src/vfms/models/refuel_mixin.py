import datetime


class RefuelMixin:
    """Represents a fuel refill record."""

    def __init__(self, liters, price_per_liter=0, date=None):
        self.liters = float(liters)
        self.price_per_liter = float(price_per_liter)
        if self.liters <= 0 or self.price_per_liter < 0:
            raise ValueError("Liters must be positive and price cannot be negative")
        self.date = date or datetime.datetime.now().isoformat(timespec="seconds")

    @property
    def total(self):
        return self.liters * self.price_per_liter

    def to_dict(self):
        return {"liters": self.liters, "price_per_liter": self.price_per_liter,
                "total": self.total, "date": self.date}
