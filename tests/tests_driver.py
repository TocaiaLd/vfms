import pytest

from vfms.models.users.driver import Driver
from vfms.models.users.person import Person

from vfms.enums import DriverStatus
from vfms.enums import VehicleLicense

"""
Testing the Driver class
"""
@pytest.fixture
def driver():
    return Driver(
        name="José", 
        cpf="33344455566", 
        license=VehicleLicense.AB, 
        xp=20, 
        status=DriverStatus.AVAILABLE, 
        trip_history=[]
    )

def test_driver_creation(driver):
    assert driver.name == "José"
    assert driver.cpf == 33344455566
    assert driver.license == VehicleLicense.AB
    assert driver.xp == 20
    assert driver.status == DriverStatus.AVAILABLE
    assert driver.trip_history == []


"""
Testing the Person class
"""

def test_person_cannot_be_instantiated():
    with pytest.raises(TypeError):
        Person(
            "José",
            "33344455566"
        )


"""
Testing setters
"""
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
def test_name_setter_valid(driver, value):
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
def test_name_setter_invalid(driver, value):
    with pytest.raises(Exception):
        driver.name = value

# cpf
@pytest.mark.parametrize(
    "value, expected",
    [
        (80658405071, 80658405071),
        ("82592916067", 82592916067),
        ("677.813.100-47", 67781310047),
        ("677..813.100-47", 67781310047),
        ("677.813.100--47", 67781310047),
    ]
)
def test_cpf_setter_valid(driver, value, expected):
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
def test_cpf_setter_invalid(driver, value):
    with pytest.raises(Exception):
        driver.cpf = value

# license
@pytest.mark.parametrize(
    "value",
    [
        (VehicleLicense.A),
        (VehicleLicense.B),
        (VehicleLicense.D),
        (VehicleLicense.AB),
        (VehicleLicense.AD),
    ]
)
def test_license_setter_valid(driver, value):
    driver.license = value

    assert driver.license in VehicleLicense

@pytest.mark.parametrize(
    "value",
    [
        "A",
        "B",
        "D",
        "AB",
        "AD",
        "Car",
        "Motorcicle",
        "Truck",
    ]
)
def test_license_setter_invalid(driver, value):
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
def test_xp_setter_valid(driver, value, expected):
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
def test_xp_setter_invalid(driver, value):
    with pytest.raises(ValueError):

        driver.xp = value


# license
@pytest.mark.parametrize(
    "value",
    [
        (DriverStatus.AVAILABLE),
        (DriverStatus.ON_TRIP),
    ]
)
def test_status_setter_valid(driver, value):
    driver.status = value

    assert driver.status in DriverStatus

@pytest.mark.parametrize(
    "value",
    [
        "AVAILABLE",
        "ON_TRIP",
    ]
)
def test_status_setter_invalid(driver, value):
    with pytest.raises(TypeError):
        driver.status = value

