import pytest

from vfms.models.vehicles.vehicle import Vehicle
from vfms.models.vehicles.car import Car
from vfms.models.vehicles.truck import Truck
from vfms.models.vehicles.motorcicle import Motorcicle

from vfms.enums import VehicleLicense
from vfms.enums import VehicleStatus

def test_vehicle_cannot_be_instantiated_directly():
    with pytest.raises(TypeError):
        Vehicle(
            plate="ABC-1D34",
            model="Onix",
            brand="Chevrolet",
            year=2020,
            mileage=10000.0,
            average_consumption=10.0,
            status=VehicleStatus.AVAILABLE,
            maintenance_h=[]
        )

@pytest.fixture
def car():
    return Car(
        plate="ABC-1D34",
        model="Onix",
        brand="Chevrolet",
        year=2020,
        mileage=10000.0,
        average_consumption=10.0,
        status=VehicleStatus.AVAILABLE,
        maintenance_h=[],
        ports=4
    )
def test_car_creation(car):
    assert isinstance(car, Car)
    assert car.plate == "ABC-1D34"
    assert car.model == "Onix"
    assert car.brand == "Chevrolet"
    assert car.year == 2020
    assert car.mileage == 10000.0
    assert car.average_consumption == 10.0
    assert car.status == VehicleStatus.AVAILABLE
    assert car.maintenance_h == []
    assert car.ports == 4
    assert car.fuel == 0.0
    assert car.license_category == VehicleLicense.B

@pytest.fixture
def truck():
    return Truck(
        plate="XYZ-4E65",
        model="Accelo",
        brand="Mercedes-Benz",
        year=2024,
        mileage=4800.0,
        average_consumption=8.0,
        status=VehicleStatus.AVAILABLE,
        maintenance_h=[],
        max_weight=15.5
    )
def test_truck_creation(truck):
    assert isinstance(truck, Truck)
    assert truck.plate == "XYZ-4E65"
    assert truck.model == "Accelo"
    assert truck.brand == "Mercedes-Benz"
    assert truck.year == 2024
    assert truck.mileage == 4800.0
    assert truck.average_consumption == 8.0
    assert truck.status == VehicleStatus.AVAILABLE
    assert truck.maintenance_h == []
    assert truck.max_weight == 15.5
    assert truck.fuel == 0.0
    assert truck.license_category == VehicleLicense.D

@pytest.fixture
def motorcicle():
    return  Motorcicle(
        plate="OSU-1E23",
        model="Factor 150",
        brand="Yamaha",
        year=2016,
        mileage=423425.3125,
        average_consumption=20.5,
        status=VehicleStatus.AVAILABLE,
        maintenance_h=[],
        cc=150
    )
def test_motorcicle_creation(motorcicle):
    assert isinstance(motorcicle, Motorcicle)
    assert motorcicle.plate == "OSU-1E23"
    assert motorcicle.model == "Factor 150"
    assert motorcicle.brand == "Yamaha"
    assert motorcicle.year == 2016
    assert motorcicle.mileage == 423425.3125
    assert motorcicle.average_consumption == 20.5
    assert motorcicle.status == VehicleStatus.AVAILABLE
    assert motorcicle.maintenance_h == []
    assert motorcicle.cc == 150
    assert motorcicle.fuel == 0.0
    assert motorcicle.license_category == VehicleLicense.A

"""
Setters tests
"""
@pytest.mark.parametrize(
    "value, expected",
    [
        (20000.0, 20000.0),
        ("20000.0", 20000.0),
        (100, 100.0),
    ],
)
def test_mileage_setter_valid(car, value, expected):
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
def test_mileage_setter_invalid(car, value):
    with pytest.raises(ValueError):
        car.mileage = value
