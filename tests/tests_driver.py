from typing import Any
import pytest

from vfms.models.users.driver import Driver
from vfms.models.users.person import Person

from vfms.enums.driver_status import DriverStatus
from vfms.enums.vehicle_license import VehicleLicense

# Tests for the Driver class
@pytest.fixture
def driver() -> Any:
    return Driver(
        name="José",
        cpf="80658405071",
        license=VehicleLicense.AB,
        xp=20,
        status=DriverStatus.AVAILABLE,
    )

def test_driver_creation(driver: Any) -> None:
    assert driver.name == "José"
    assert driver.cpf == "80658405071"
    assert driver.license == VehicleLicense.AB
    assert driver.xp == 20
    assert driver.status == DriverStatus.AVAILABLE
    assert driver.trip_history == []
    assert list(driver) == []


def test_driver_trip_history_is_independent(driver: Any) -> None:
    first = driver
    second = Driver("Ana", "80658405071", VehicleLicense.AB, 10, DriverStatus.AVAILABLE)
    first.trip_history.append("trip")

    assert list(first) == ["trip"]
    assert list(second) == []
    assert "trip_history: ['trip']" in str(first)
    assert "trip_history: []" in str(second)

# Tests for the Person class

def test_person_cannot_be_instantiated() -> None:
    with pytest.raises(TypeError):
        Person(
            "José",
            "33344455566"
        )


# Setter tests
# Name
@pytest.mark.parametrize(
    "value",
    [
        "Wesley",
        "José",
        "Pedim",
        "Antonio José de Lima Alves"
    ]
)
def test_name_setter_valid(driver: Any, value: Any) -> None:
    driver.name = value
    
    assert driver.name == value

@pytest.mark.parametrize(
    "value",
    [
        "Wesley2",
        "123",
        "Zé",
        "Pedro de Alcântara João Carlos Leopoldo Salvador Bibiano Francisco Xavier de Paula Leocádio Miguel Gabriel Rafael Gonzaga de Bragança e Bourbon",
    ]
)
def test_name_setter_invalid(driver: Any, value: Any) -> None:
    with pytest.raises(Exception):
        driver.name = value

# cpf
@pytest.mark.parametrize(
    "value, expected",
    [
        (80658405071, "80658405071"),
        ("82592916067", "82592916067"),
        ("677.813.100-47", "67781310047"),
        ("677..813.100-47", "67781310047"),
        ("677.813.100--47", "67781310047"),
    ]
)
def test_cpf_setter_valid(driver: Any, value: Any, expected: Any) -> None:
    driver.cpf = value

    assert driver.cpf == expected

@pytest.mark.parametrize(
    "value",
    [
        806584050711,
        "806584050711",
        8259291606,
        "8259291606",
        123,
        1,
        -500
    ]
)
def test_cpf_setter_invalid(driver: Any, value: Any) -> None:
    with pytest.raises(Exception):
        driver.cpf = value

# license
@pytest.mark.parametrize(
    "value",
    [
        (VehicleLicense.A),
        (VehicleLicense.B),
        (VehicleLicense.C),
        (VehicleLicense.D),
        (VehicleLicense.E),
        (VehicleLicense.AB),
        (VehicleLicense.AD),
        "A",
        "B",
        "C",
        "D",
        "E",
        "AB",
        "AD",
    ]
)
def test_license_setter_valid(driver: Any, value: Any) -> None:
    driver.license = value

    assert driver.license in VehicleLicense

@pytest.mark.parametrize(
    "value",
    [
        "Car",
        "Motorcicle",
        "Truck",
    ]
)
def test_license_setter_invalid(driver: Any, value: Any) -> None:
    with pytest.raises(TypeError):
        driver.license = value


# experience
@pytest.mark.parametrize(
    "value, expected",
    [
        (5, 5),
        (0, 0),
        (5.0, 5)
    ]
)
def test_xp_setter_valid(driver: Any, value: Any, expected: Any) -> None:
    driver.xp = value

    assert driver.xp == expected

@pytest.mark.parametrize(
    "value",
    [
        5.2,
        "vinte anos",
        "D",
        -10,
    ]
)
def test_xp_setter_invalid(driver: Any, value: Any) -> None:
    with pytest.raises(ValueError):

        driver.xp = value


# license
@pytest.mark.parametrize(
    "value",
    [
        DriverStatus.AVAILABLE,
        DriverStatus.ON_TRIP,
        "AVAILABLE",
        "ON_TRIP",
    ]
)
def test_status_setter_valid(driver: Any, value: Any) -> None:
    driver.status = value

    assert driver.status in DriverStatus

@pytest.mark.parametrize(
    "value",
    [
        "1",
        "Teste",
        2.5,
        2,
    ]
)
def test_status_setter_invalid(driver: Any, value: Any) -> None:
    with pytest.raises(TypeError):
        driver.status = value

