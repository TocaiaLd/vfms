from typing import Any
from datetime import datetime

import pytest

from vfms.enums.enum_trip import EnumTrip
from vfms.models.trip import Trip


@pytest.fixture
def trip() -> Any:
    return Trip(
        driver_cpf="80658405071",
        vehicle_plate="ABC-1D34",
        origin="Fortaleza",
        destiny="Sobral",
        distance=230,
        status=EnumTrip.IN_PROGRESS,
    )


def test_trip_creation(trip: Any) -> None:
    assert trip.driver_cpf == "80658405071"
    assert trip.vehicle_plate == "ABC-1D34"
    assert trip.origin == "Fortaleza"
    assert trip.destiny == "Sobral"
    assert trip.distance == 230.0
    assert trip.status == EnumTrip.IN_PROGRESS


def test_trip_text_fields_are_normalized(trip: Any) -> None:
    trip.driver_cpf = 80658405071
    trip.vehicle_plate = 123
    trip.origin = 42
    trip.destiny = None

    assert trip.driver_cpf == "80658405071"
    assert trip.vehicle_plate == "123"
    assert trip.origin == "42"
    assert trip.destiny == "None"


def test_trip_distance_setter_converts_to_float(trip: Any) -> None:
    trip.distance = "12.5"

    assert trip.distance == 12.5


@pytest.mark.parametrize("value", ["invalid", None])
def test_trip_distance_setter_rejects_non_numeric_values(trip: Any, value: Any) -> None:
    with pytest.raises((TypeError, ValueError)):
        trip.distance = value


@pytest.mark.parametrize(
    "value, expected",
    [
        (EnumTrip.ENDED, EnumTrip.ENDED),
        ("ENDED", EnumTrip.ENDED),
        ("Ended", EnumTrip.ENDED),
        ("IN_PROGRESS", EnumTrip.IN_PROGRESS),
        ("In progress", EnumTrip.IN_PROGRESS),
    ],
)
def test_trip_status_setter_accepts_enum_and_names(trip: Any, value: Any, expected: Any) -> None:
    trip.status = value

    assert trip.status == expected


def test_trip_status_setter_rejects_unknown_status(trip: Any) -> None:
    with pytest.raises(TypeError):
        trip.status = "CANCELLED"


def test_trip_date_setters_and_date_methods(trip: Any) -> None:
    start = datetime(2026, 1, 1, 10, 0)
    end = datetime(2026, 1, 1, 11, 0)
    trip.date_init = start
    trip.date_end = end

    assert trip.date_init == start
    assert trip.date_end == end

    trip.set_date_init()
    trip.set_date_end()

    assert isinstance(trip.date_init, datetime)
    assert isinstance(trip.date_end, datetime)


@pytest.mark.parametrize("attribute", ["date_init", "date_end"])
def test_trip_date_setters_reject_non_datetime_values(trip: Any, attribute: Any) -> None:
    with pytest.raises(TypeError):
        setattr(trip, attribute, "2026-01-01")
