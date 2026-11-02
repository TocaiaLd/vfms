from typing import Any
from datetime import datetime

import pytest

from vfms.models.refuel_mixin import RefuelMixin


class VehicleWithFuel(RefuelMixin):
    def __init__(self, fuel: Any=10.0, max_fuel: Any=50.0, plate: Any="ABC-1D34") -> None:
        self.fuel = fuel
        self.max_fuel = max_fuel
        self.plate = plate


@pytest.fixture
def vehicle() -> Any:
    return VehicleWithFuel()


def test_refuel_updates_fuel_and_returns_record(vehicle: Any) -> None:
    record = vehicle.refuel(5, 6.25)

    assert vehicle.fuel == 15.0
    assert record[:4] == ("ABC-1D34", 5.0, 6.25, 31.25)
    assert isinstance(record[4], datetime)


def test_refuel_caps_amount_at_max_fuel(vehicle: Any, capsys: Any) -> None:
    record = vehicle.refuel(60, 2.0)

    assert vehicle.fuel == 50.0
    assert record[1:4] == (40.0, 2.0, 80.0)
    assert "excede a capacidade" in capsys.readouterr().out


@pytest.mark.parametrize("liters", [0, -1])
def test_refuel_rejects_non_positive_amount(vehicle: Any, liters: Any, capsys: Any) -> None:
    assert vehicle.refuel(liters, 2.0) is None
    assert vehicle.fuel == 10.0
    assert "quantidade menor ou igual a zero" in capsys.readouterr().out


def test_refuel_rejects_negative_price(vehicle: Any) -> None:
    with pytest.raises(ValueError):
        vehicle.refuel(1, -0.01)

    assert vehicle.fuel == 10.0


def test_refuel_when_tank_is_full_returns_none(vehicle: Any, capsys: Any) -> None:
    vehicle.fuel = vehicle.max_fuel

    assert vehicle.refuel(1, 2.0) is None
    assert vehicle.fuel == 50.0
    assert "quantidade menor ou igual a zero" in capsys.readouterr().out


def test_refuel_without_vehicle_attributes_uses_unlimited_capacity() -> None:
    mixin = RefuelMixin()

    record = mixin.refuel(2, 3)

    assert record[:4] == (None, 2.0, 3.0, 6.0)
    assert isinstance(record[4], datetime)
