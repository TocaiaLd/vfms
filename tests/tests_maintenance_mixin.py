from datetime import datetime

import pytest

from vfms.enums.enum_maintenance import EnumMaintenance
from vfms.models.maintenance_mixin import MaintenanceMixin


class VehicleWithMaintenance(MaintenanceMixin):
    plate = "ABC-1D34"


@pytest.fixture
def maintenance():
    return VehicleWithMaintenance()


def test_new_maintenance_creates_record_and_sets_properties(maintenance):
    record = maintenance.new_maintenance(
        EnumMaintenance.PREVENTIVE,
        125.50,
        "Oil change",
        "2026-01-02 09:30:00",
    )

    assert record == (
        "ABC-1D34",
        "preventive",
        125.50,
        "Oil change",
        "2026-01-02 09:30:00",
        "...",
    )
    assert maintenance.type == EnumMaintenance.PREVENTIVE
    assert maintenance.price == 125.50
    assert maintenance.description == "Oil change"
    assert maintenance.date_init == "2026-01-02 09:30:00"
    assert maintenance.date_end == "..."


@pytest.mark.parametrize("value", ["preventive", "corrective"])
def test_new_maintenance_accepts_enum_values(maintenance, value):
    record = maintenance.new_maintenance(value, 0, "Inspection")

    assert record[1] == value
    assert record[2] == 0.0
    assert record[3] == "Inspection"
    assert isinstance(record[4], str)


def test_new_maintenance_without_plate_uses_empty_string():
    maintenance = MaintenanceMixin()

    record = maintenance.new_maintenance(EnumMaintenance.CORRECTIVE, 10, "Repair")

    assert record[0] == ""


def test_new_maintenance_rejects_invalid_type(maintenance):
    with pytest.raises(ValueError):
        maintenance.new_maintenance("unknown", 10, "Repair")


def test_new_maintenance_rejects_negative_price(maintenance):
    with pytest.raises(ValueError):
        maintenance.new_maintenance(EnumMaintenance.CORRECTIVE, -1, "Repair")


def test_maintenance_price_setter_converts_numeric_values(maintenance):
    maintenance.price = "12.75"

    assert maintenance.price == 12.75


def test_maintenance_price_setter_rejects_non_numeric_values(maintenance):
    with pytest.raises(ValueError):
        maintenance.price = "invalid"


def test_maintenance_date_init_accepts_datetime(maintenance):
    date = datetime(2026, 2, 3, 8, 15)
    maintenance.date_init = date

    assert maintenance.date_init == date


def test_maintenance_date_init_rejects_other_types(maintenance):
    with pytest.raises(TypeError):
        maintenance.date_init = 123
