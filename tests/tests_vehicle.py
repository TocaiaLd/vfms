from typing import Any
import pytest

from vfms.models.vehicles.vehicle import Vehicle
from vfms.models.vehicles.car import Car
from vfms.models.vehicles.truck import Truck
from vfms.models.vehicles.motorcycle import Motorcycle

from vfms.enums.vehicle_license import VehicleLicense
from vfms.enums.vehicle_status import VehicleStatus


# Creation of Vehicle, Car, Truck, and Motorcycle objects
def test_vehicle_cannot_be_instantiated_directly() -> None:
    with pytest.raises(TypeError):
        Vehicle(
            plate="ABC-1D34",
            model="Onix",
            brand="Chevrolet",
            year=2020,
            mileage=10000.0,
            average_consumption=10.0,
            status=VehicleStatus.AVAILABLE,
            max_fuel=50.0,
            fuel=0.0
        )

@pytest.fixture
def car() -> Any:
    return Car(
        plate               = "ABC-1D34",
        model               = "Onix",
        brand               = "Chevrolet",
        year                = 2020,
        mileage             = 10000.0,
        average_consumption = 10.0,
        status              = VehicleStatus.AVAILABLE,
        max_fuel            = 50.0,
        fuel                = 0.0,
        ports               = 4,
    )
def test_car_creation(car: Any) -> None:
    assert isinstance(car, Car)
    assert car.plate                == "ABC-1D34"
    assert car.model                == "Onix"
    assert car.brand                == "Chevrolet"
    assert car.year                 == 2020
    assert car.mileage              == 10000.0
    assert car.average_consumption  == 10.0
    assert car.status               == VehicleStatus.AVAILABLE
    assert car.ports                == 4
    assert car.fuel                 == 0.0
    assert car.license_category     == VehicleLicense.B

@pytest.fixture
def truck() -> Any:
    return Truck(
        plate                   = "XYZ-4E65",
        model                   = "Accelo",
        brand                   = "Mercedes-Benz",
        year                    = 2024,
        mileage                 = 4800.0,
        average_consumption     = 8.0,
        status                  = VehicleStatus.AVAILABLE,
        max_fuel                = 300.0,
        fuel                    = 0.0,
        max_weight              = 15.5
    )
def test_truck_creation(truck: Any) -> None:
    assert isinstance(truck, Truck)
    assert truck.plate                  == "XYZ-4E65"
    assert truck.model                  == "Accelo"
    assert truck.brand                  == "Mercedes-Benz"
    assert truck.year                   == 2024
    assert truck.mileage                == 4800.0
    assert truck.average_consumption    == 8.0
    assert truck.status                 == VehicleStatus.AVAILABLE
    assert truck.max_weight             == 15.5
    assert truck.fuel                   == 0.0
    assert truck.license_category       == VehicleLicense.C


@pytest.fixture
def motorcycle() -> Any:
    return  Motorcycle(
        plate               = "OSU-1E23",
        model               = "Factor 150",
        brand               = "Yamaha",
        year                = 2016,
        mileage             = 423425.3125,
        average_consumption = 20.5,
        status              = VehicleStatus.AVAILABLE,
        max_fuel            = 20.0,
        fuel                = 0.0,
        cc                  = 150
    )
def test_motorcycle_creation(motorcycle: Any) -> None:
    assert isinstance(motorcycle, Motorcycle)
    assert motorcycle.plate                 == "OSU-1E23"
    assert motorcycle.model                 == "Factor 150"
    assert motorcycle.brand                 == "Yamaha"
    assert motorcycle.year                  == 2016
    assert motorcycle.mileage               == 423425.3125
    assert motorcycle.average_consumption   == 20.5
    assert motorcycle.status                == VehicleStatus.AVAILABLE
    assert motorcycle.cc                    == 150
    assert motorcycle.fuel                  == 0.0
    assert motorcycle.license_category      == VehicleLicense.A


@pytest.mark.parametrize(
    "vehicle_fixture, subtype_key, subtype_value, license",
    [
        ("car", "ports", 4, "B"),
        ("motorcycle", "cc", 150, "A"),
        ("truck", "max_weight", 15.5, "C"),
    ],
)
def test_vehicle_subclass_serialization(request: Any, vehicle_fixture: Any, subtype_key: Any, subtype_value: Any, license: Any) -> None:
    vehicle = request.getfixturevalue(vehicle_fixture)
    data = vehicle.to_dict()[vehicle.plate]

    assert data["model"] == vehicle.model
    assert data["status"] == vehicle.status.name
    assert data["license"] == license
    assert data[subtype_key] == subtype_value


def test_vehicle_status_transitions_allow_business_flow(car: Any) -> None:
    car.status = VehicleStatus.MAINTENANCE
    car.status = VehicleStatus.AVAILABLE
    car.status = VehicleStatus.INACTIVE
    car.status = VehicleStatus.AVAILABLE
    car.status = VehicleStatus.ON_TRIP
    car.status = VehicleStatus.MAINTENANCE

    assert car.status == VehicleStatus.MAINTENANCE


@pytest.mark.parametrize(
    "start, end",
    [
        (VehicleStatus.INACTIVE, VehicleStatus.ON_TRIP),
        (VehicleStatus.MAINTENANCE, VehicleStatus.ON_TRIP),
        (VehicleStatus.ON_TRIP, VehicleStatus.INACTIVE),
    ],
)
def test_vehicle_status_transitions_reject_invalid_changes(car: Any, start: Any, end: Any) -> None:
    car.status = start
    with pytest.raises(ValueError):
        car.status = end


# Setter tests
@pytest.mark.parametrize(
    "value, expected",
    [
        (20000.0, 20000.0),
        ("20000.0", 20000.0),
        (100, 100.0),
    ],
)
def test_mileage_setter_valid(car: Any, value: Any, expected: Any) -> None:
    car.mileage = value

    assert car.mileage == expected

@pytest.mark.parametrize(
    "value",
    [
        -100,
        -1,
        "a",
        "abc"
    ],
)
def test_mileage_setter_invalid(car: Any, value: Any) -> None:
    with pytest.raises(ValueError):
        car.mileage = value

@pytest.mark.parametrize(
    "value",
    [
        "AB1-2C34",
        "XYZ-A1BC",
        "ABC-1234",
        "AAAA-111",
        "BR-2E26",
    ],
)
def test_plate_setter_invalid(car: Any, value: Any) -> None:
    with pytest.raises((ValueError, IndexError)):
        car.plate = value

@pytest.mark.parametrize(
    "value", 
    [
        "ABC-2C34",
        "XYZ-1A43",
        "ABC-1C34",
        "AAA-1L11",
        "BRC-2E26",
    ],
)
def test_plate_setter_valid(car: Any, value: Any) -> None:
    car.plate = value

    assert car.plate == value

@pytest.mark.parametrize(
    "value, expected", 
    [
        ("1888", 1888),
        ("2000", 2000),
        (2026, 2026),
    ],
)
def test_year_setter_valid(car: Any, value: Any, expected: Any) -> None:
    car.year = value

    assert car.year == expected

@pytest.mark.parametrize(
    "value", 
    [
        1887,
        -1000,
        0,
        1888.1,
        25,
        2026.5
    ],
)
def test_year_setter_invalid(car: Any, value: Any) -> None:
    with pytest.raises(ValueError):
        car.year = value


@pytest.mark.parametrize("value, expected", [(5, 5), ("5", 5), (5.0, 5)])
def test_ports_setter_accepts_only_whole_positive_values(car: Any, value: Any, expected: Any) -> None:
    car.ports = value
    assert car.ports == expected


@pytest.mark.parametrize("value", [2.5, "2.5", 0, -1, True])
def test_ports_setter_rejects_invalid_values(car: Any, value: Any) -> None:
    with pytest.raises(ValueError):
        car.ports = value
