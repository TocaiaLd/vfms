from typing import Any
import pytest
import sqlite3

from vfms.controllers.driver_controller import DriverController
from vfms.enums.driver_status import DriverStatus
from vfms.enums.enum_trip import EnumTrip
from vfms.enums.enum_maintenance import EnumMaintenance
from vfms.enums.vehicle_license import VehicleLicense
from vfms.enums.vehicle_status import VehicleStatus
from vfms.exceptions import AlocacaoInvalidaError, PoliticaNaoAtendidaError
from vfms.exceptions import RepositorioError
from vfms.models.trip import Trip
from vfms.models.users.driver import Driver
from vfms.models.vehicles.car import Car
from vfms.models.vehicles.motorcycle import Motorcycle
from vfms.models.vehicles.truck import Truck
from vfms.repos.driver_repo import DriverRepo
from vfms.repos.maintenance_repo import MaintenanceRepo
from vfms.repos.repo import Repo
from vfms.repos.refuel_repo import RefuelRepo
from vfms.repos.trip_repo import TripRepo
from vfms.repos.vehicles.car_repo import CarRepo
from vfms.repos.vehicles.motorcycle_repo import MotorcycleRepo
from vfms.repos.vehicles.truck_repo import TruckRepo


SETTINGS = {
    "maintenance": {"preventive_interval_km": 10000},
    "driver_license": {
        "minimum_category_by_vehicle_type": {
            "car": "B",
            "motorcycle": "A",
            "truck": "C",
        }
    },
}


@pytest.fixture
def repo() -> Any:
    database = Repo(":memory:")
    yield database
    database.close()


def make_driver(status: Any=DriverStatus.AVAILABLE, license: Any=VehicleLicense.AB) -> Any:
    return Driver("Test Driver", "80658405071", license, 5, status)


def make_vehicle(vehicle_type: Any="car", status: Any=VehicleStatus.AVAILABLE, mileage: Any=0) -> Any:
    values = dict(
        plate="ABC-1D34",
        model="Model",
        brand="Brand",
        year=2024,
        mileage=mileage,
        average_consumption=12,
        status=status,
        max_fuel=80,
        fuel=0,
    )
    if vehicle_type == "car":
        return Car(**values, ports=4)
    if vehicle_type == "motorcycle":
        values["plate"] = "MOT-1D34"
        return Motorcycle(**values, cc=150)
    values["plate"] = "TRK-1D34"
    return Truck(**values, max_weight=10)


def persist_vehicle(repo: Any, vehicle: Any) -> Any:
    if isinstance(vehicle, Car):
        vehicle_repo = CarRepo(repo)
        vehicle_repo.save_car(vehicle)
    elif isinstance(vehicle, Motorcycle):
        vehicle_repo = MotorcycleRepo(repo)
        vehicle_repo.save_motorcycle(vehicle)
    else:
        vehicle_repo = TruckRepo(repo)
        vehicle_repo.save_truck(vehicle)
    return vehicle_repo


@pytest.mark.parametrize(
    "vehicle_type",
    ["car", "motorcycle", "truck"],
)
def test_vehicle_deletion_removes_related_records_atomically(repo: Any, vehicle_type: Any) -> None:
    vehicle = make_vehicle(vehicle_type)
    vehicle_repo = persist_vehicle(repo, vehicle)
    DriverRepo(repo).save_driver(make_driver())
    repo._cursor.execute(
        "INSERT INTO trips (driver_cpf, vehicle_plate, origin, destiny, distance, status, date_init, date_end) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        ("80658405071", vehicle.plate, "A", "B", 10, "In progress", "now", "..."),
    )
    repo._cursor.execute(
        "INSERT INTO maintenances (plate, type, price, description, date_init, date_end, mileage) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (vehicle.plate, "preventive", 10, "service", "now", "...", 0),
    )
    repo._cursor.execute(
        "INSERT INTO refuels (plate, liters, price_per_liter, total_cost, date) VALUES (?, ?, ?, ?, ?)",
        (vehicle.plate, 10, 2, 20, "now"),
    )

    result = getattr(vehicle_repo, f"delete_{vehicle_type}")(vehicle.plate)

    assert "deleted" in result.lower()
    for table, column in (("trips", "vehicle_plate"), ("maintenances", "plate"), ("refuels", "plate"), ("vehicles", "plate")):
        assert repo._cursor.execute(
            f"SELECT COUNT(*) FROM {table} WHERE {column} = ?", (vehicle.plate,)
        ).fetchone()[0] == 0


@pytest.mark.parametrize(
    "vehicle_type",
    ["car", "motorcycle", "truck"],
)
def test_vehicle_delete_of_missing_plate_is_consistent(repo: Any, vehicle_type: Any) -> None:
    vehicle_repo = persist_vehicle(repo, make_vehicle(vehicle_type))

    result = getattr(vehicle_repo, f"delete_{vehicle_type}")("NO-1D34")

    assert "does not exist" in result.lower()


def test_driver_availability_distinguishes_exists_from_available(repo: Any) -> None:
    driver_repo = DriverRepo(repo)
    controller = DriverController(driver_repo)
    driver_repo.save_driver(make_driver())

    assert controller.driver_exists("80658405071") is True
    assert controller.driver_is_available("80658405071") is True
    assert controller.driver_exists("00000000000") is False
    assert controller.driver_is_available("00000000000") is False

    driver_repo.update_driver(make_driver(DriverStatus.ON_TRIP))
    assert controller.driver_exists("80658405071") is True
    assert controller.driver_is_available("80658405071") is False


def test_driver_with_trip_history_cannot_be_deleted(repo: Any) -> None:
    driver_repo = DriverRepo(repo)
    driver_repo.save_driver(make_driver())
    vehicle = make_vehicle()
    persist_vehicle(repo, vehicle)
    repo._cursor.execute(
        "INSERT INTO trips (driver_cpf, vehicle_plate, origin, destiny, distance, status, date_init, date_end) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        ("80658405071", vehicle.plate, "A", "B", 10, "In progress", "now", "..."),
    )

    assert "with recorded trips" in driver_repo.delete_driver("80658405071")


def test_repository_errors_are_reported_as_repository_errors(repo: Any) -> None:
    repo.close()

    with pytest.raises(RepositorioError, match="SQLite query failed"):
        repo.execute("SELECT 1")


def test_repository_migrates_legacy_maintenance_schema(tmp_path: Any) -> None:
    database_path = tmp_path / "legacy.sqlite3"
    connection = sqlite3.connect(database_path)
    connection.execute(
        "CREATE TABLE drivers (name TEXT NOT NULL, cpf TEXT NOT NULL PRIMARY KEY, license TEXT NOT NULL, xp INTEGER, status TEXT NOT NULL)"
    )
    connection.execute(
        "INSERT INTO drivers VALUES (?, ?, ?, ?, ?)",
        ("Driver", "04472757001", "B", 2, "AVAILABLE"),
    )
    connection.execute(
        "CREATE TABLE vehicles (plate TEXT PRIMARY KEY, model TEXT NOT NULL, brand TEXT NOT NULL, year INTEGER, mileage REAL, average_consumption REAL, status TEXT NOT NULL, max_fuel REAL, fuel REAL, license TEXT NOT NULL)"
    )
    connection.execute(
        "INSERT INTO vehicles VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        ("ABC-1D34", "Car", "Brand", 2024, 10, 10, "AVAILABLE", 50, 0, "B"),
    )
    connection.execute(
        "CREATE TABLE trips (trip_id INTEGER PRIMARY KEY AUTOINCREMENT, driver_cpf INTEGER, vehicle_plate TEXT NOT NULL, origin TEXT NOT NULL, destiny TEXT NOT NULL, distance REAL, status TEXT NOT NULL, date_init TEXT NOT NULL, date_end TEXT NOT NULL, FOREIGN KEY (driver_cpf) REFERENCES drivers (cpf), FOREIGN KEY (vehicle_plate) REFERENCES vehicles (plate))"
    )
    connection.execute(
        "INSERT INTO trips VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (1, 4472757001, "ABC-1D34", "A", "B", 5, "Ended", "start", "end"),
    )
    connection.execute(
        "CREATE TABLE maintenances (id INTEGER PRIMARY KEY, plate TEXT, type TEXT, price REAL, description TEXT, date_init TEXT, date_end TEXT)"
    )
    connection.execute(
        "INSERT INTO maintenances VALUES (?, ?, ?, ?, ?, ?, ?)",
        (1, "ABC-1D34", "preventive", 100, "legacy service", "2025-01-01", "2025-01-02"),
    )
    connection.commit()
    connection.close()

    migrated = Repo(database_path)
    columns = {row[1] for row in migrated.execute("PRAGMA table_info(maintenances)").fetchall()}
    trip_columns = {row[1]: row[2] for row in migrated.execute("PRAGMA table_info(trips)").fetchall()}
    migrated_trip = migrated.execute("SELECT driver_cpf FROM trips WHERE trip_id = 1").fetchone()
    migrated_maintenance = migrated.execute(
        "SELECT mileage FROM maintenances WHERE id = 1"
    ).fetchone()

    assert "mileage" in columns
    assert trip_columns["driver_cpf"] == "TEXT"
    assert migrated_trip == ("04472757001",)
    assert migrated_maintenance == (10.0,)
    migrated.close()


def test_driver_crud_and_missing_delete(repo: Any) -> None:
    controller = DriverController(DriverRepo(repo))
    request = {
        "name": "Test Driver",
        "cpf": "80658405071",
        "license": VehicleLicense.AB,
        "xp": 5,
        "status": DriverStatus.AVAILABLE,
    }

    assert "saved" in controller.new_driver(request).lower()
    assert controller.get_by_cpf("80658405071").name == "Test Driver"
    assert "Test Driver" in controller.show_drivers()
    request.update({"name": "Updated Driver", "status": DriverStatus.INACTIVE})
    assert "updated" in controller.update_driver(
        request["name"], request["cpf"], request["license"], request["xp"], request["status"]
    ).lower()
    updated = controller.get_by_cpf("80658405071")
    assert updated.name == "Updated Driver"
    assert updated.status == DriverStatus.INACTIVE
    assert "deleted" in controller.delete_driver("80658405071").lower()
    assert "does not exist" in controller.delete_driver("80658405071").lower()


def test_trip_allocation_updates_driver_and_vehicle(repo: Any) -> None:
    DriverRepo(repo).save_driver(make_driver())
    persist_vehicle(repo, make_vehicle("car"))
    trip_repo = TripRepo(repo, SETTINGS)
    trip = Trip("80658405071", "ABC-1D34", "A", "B", 20, EnumTrip.IN_PROGRESS)
    trip.set_date_init()

    assert trip_repo.save_trip(trip) == "Trip saved."
    assert repo._cursor.execute("SELECT status FROM drivers").fetchone()[0] == "ON_TRIP"
    assert repo._cursor.execute("SELECT status FROM cars").fetchone()[0] == "ON_TRIP"
    assert repo._cursor.execute("SELECT COUNT(*) FROM trips").fetchone()[0] == 1


@pytest.mark.parametrize(
    "driver, vehicle, message",
    [
        (None, "car", "Driver CPF does not exist"),
        (DriverStatus.ON_TRIP, "car", "Driver is not available"),
        (DriverStatus.AVAILABLE, "maintenance", "Vehicle is under maintenance"),
        (DriverStatus.AVAILABLE, "inactive", "Vehicle is inactive"),
    ],
)
def test_trip_allocation_blocks_missing_or_unavailable_resources(repo: Any, driver: Any, vehicle: Any, message: Any) -> None:
    if driver is not None:
        DriverRepo(repo).save_driver(make_driver(driver))
    vehicle_status = {
        "maintenance": VehicleStatus.MAINTENANCE,
        "inactive": VehicleStatus.INACTIVE,
    }.get(vehicle, VehicleStatus.AVAILABLE)
    persist_vehicle(repo, make_vehicle("car", vehicle_status))
    trip = Trip("80658405071", "ABC-1D34", "A", "B", 20, EnumTrip.IN_PROGRESS)

    with pytest.raises(AlocacaoInvalidaError, match=message):
        TripRepo(repo, SETTINGS).save_trip(trip)


def test_trip_allocation_enforces_configured_license_hierarchy(repo: Any) -> None:
    DriverRepo(repo).save_driver(make_driver(license=VehicleLicense.B))
    persist_vehicle(repo, make_vehicle("truck"))
    trip = Trip("80658405071", "TRK-1D34", "A", "B", 20, EnumTrip.IN_PROGRESS)

    with pytest.raises(PoliticaNaoAtendidaError):
        TripRepo(repo, SETTINGS).save_trip(trip)

    DriverRepo(repo).update_driver(make_driver(license=VehicleLicense.C))
    assert TripRepo(repo, SETTINGS).save_trip(trip) == "Trip saved."


def test_finishing_trip_updates_mileage_and_schedules_preventive_service(repo: Any) -> None:
    DriverRepo(repo).save_driver(make_driver())
    persist_vehicle(repo, make_vehicle("car", mileage=9990))
    trip_repo = TripRepo(repo, SETTINGS)
    trip = Trip("80658405071", "ABC-1D34", "A", "B", 10, EnumTrip.IN_PROGRESS)
    trip.set_date_init()
    trip_repo.save_trip(trip)
    trip.set_date_end()

    assert trip_repo.finish_trip(trip, "1") == "Trip finished."
    assert repo._cursor.execute("SELECT mileage, status FROM cars").fetchone() == (10000.0, "MAINTENANCE")
    assert repo._cursor.execute("SELECT status FROM drivers").fetchone()[0] == "AVAILABLE"


def test_finishing_trip_uses_last_preventive_service_mileage(repo: Any) -> None:
    DriverRepo(repo).save_driver(make_driver())
    persist_vehicle(repo, make_vehicle("car", mileage=20000))
    maintenance_repo = MaintenanceRepo(repo)
    maintenance_repo.save_maintenance(
        ("ABC-1D34", "preventive", 50, "service", "2026-01-01", "...", 20000)
    )
    maintenance_repo.finish_maintenance("ABC-1D34", "1")
    trip_repo = TripRepo(repo, SETTINGS)
    trip = Trip("80658405071", "ABC-1D34", "A", "B", 9999, EnumTrip.IN_PROGRESS)
    trip.set_date_init()
    trip_repo.save_trip(trip)
    trip.set_date_end()
    trip_repo.finish_trip(trip, "1")
    assert repo._cursor.execute("SELECT status FROM cars").fetchone()[0] == "AVAILABLE"

    # The vehicle has passed 10 km beyond the saved 20,000 km service snapshot.
    repo._cursor.execute("UPDATE cars SET status = 'AVAILABLE' WHERE plate = ?", ("ABC-1D34",))
    second_trip = Trip("80658405071", "ABC-1D34", "A", "B", 1, EnumTrip.IN_PROGRESS)
    second_trip.set_date_init()
    trip_repo.save_trip(second_trip)
    second_trip.set_date_end()
    trip_repo.finish_trip(second_trip, "2")
    assert repo._cursor.execute("SELECT status FROM cars").fetchone()[0] == "MAINTENANCE"


@pytest.mark.parametrize("vehicle_type", ["car", "motorcycle", "truck"])
def test_vehicle_update_persists_subclass_values(repo: Any, vehicle_type: Any) -> None:
    vehicle = make_vehicle(vehicle_type)
    vehicle_repo = persist_vehicle(repo, vehicle)
    vehicle.model = "Updated"
    assert "updated" in getattr(vehicle_repo, f"update_{vehicle_type}")(vehicle).lower()
    assert getattr(vehicle_repo, f"get_by_plate")(vehicle.plate)[1] == "Updated"


def test_maintenance_registration_and_finish_updates_vehicle_state(repo: Any) -> None:
    vehicle = make_vehicle("car")
    vehicle_repo = persist_vehicle(repo, vehicle)
    maintenance_repo = MaintenanceRepo(repo)
    record = vehicle.new_maintenance(EnumMaintenance.PREVENTIVE, 100, "service")

    assert maintenance_repo.save_maintenance(record) == "Maintenance saved."
    assert vehicle_repo.get_by_plate("ABC-1D34")[6] == "MAINTENANCE"
    assert maintenance_repo.finish_maintenance("ABC-1D34", "1") == "Maintenance finished."
    assert vehicle_repo.get_by_plate("ABC-1D34")[6] == "AVAILABLE"
    assert maintenance_repo.read_maintenances()[0][7] == 0


def test_refuel_record_is_persisted_in_database_compatible_format(repo: Any) -> None:
    persist_vehicle(repo, make_vehicle("car"))
    from vfms.controllers.vehicles.car_controller import CarController

    car = CarController(CarRepo(repo)).get_by_plate("ABC-1D34")
    record = car.refuel(5, 2.5)
    RefuelRepo(repo).save_refuel(record)

    stored = repo._cursor.execute(
        "SELECT plate, liters, price_per_liter, total_cost, date FROM refuels"
    ).fetchone()
    assert stored[:4] == ("ABC-1D34", 5.0, 2.5, 12.5)
    assert isinstance(stored[4], str)
