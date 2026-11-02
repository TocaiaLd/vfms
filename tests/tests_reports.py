from typing import Any
import pytest

from vfms.controllers.vehicles.car_controller import CarController
from vfms.controllers.vehicles.motorcycle_controller import MotorcycleController
from vfms.controllers.vehicles.truck_controller import TruckController
from vfms.controllers.trip_controller import TripController
from vfms.controllers.maintenance_controller import MaintenanceController
from vfms.enums.driver_status import DriverStatus
from vfms.enums.enum_trip import EnumTrip
from vfms.enums.enum_maintenance import EnumMaintenance
from vfms.enums.vehicle_license import VehicleLicense
from vfms.enums.vehicle_status import VehicleStatus
from vfms.models.trip import Trip
from vfms.models.users.driver import Driver
from vfms.models.vehicles.car import Car
from vfms.models.vehicles.motorcycle import Motorcycle
from vfms.models.vehicles.truck import Truck
from vfms.repos.driver_repo import DriverRepo
from vfms.repos.maintenance_repo import MaintenanceRepo
from vfms.repos.repo import Repo
from vfms.repos.trip_repo import TripRepo
from vfms.repos.vehicles.car_repo import CarRepo
from vfms.repos.vehicles.motorcycle_repo import MotorcycleRepo
from vfms.repos.vehicles.truck_repo import TruckRepo
from vfms.view.reports.reports import (
    build_fuel_efficiency_report,
    build_maintenance_report,
    build_mileage_report,
    build_trip_report,
    page_vehicle_status_report,
)
import vfms.view.reports.reports as reports


class Prompt:
    def __init__(self, answer: Any) -> None:
        self.answer = answer

    def ask(self) -> Any:
        return self.answer


SETTINGS = {
    "maintenance": {"preventive_interval_km": 10000},
    "fuel": {
        "acceptable_consumption_km_per_l": {
            "car": {"min": 8, "max": 18},
            "motorcycle": {"min": 20, "max": 45},
            "truck": {"min": 2, "max": 8},
        }
    },
    "driver_license": {
        "minimum_category_by_vehicle_type": {
            "car": "B", "motorcycle": "A", "truck": "C"
        }
    },
}


@pytest.fixture
def database() -> Any:
    repo = Repo(":memory:")
    yield repo
    repo.close()


@pytest.fixture
def persisted_data(database: Any) -> Any:
    car_repo = CarRepo(database)
    motorcycle_repo = MotorcycleRepo(database)
    truck_repo = TruckRepo(database)
    driver_repo = DriverRepo(database)

    car_repo.save_car(Car("ABC-1D34", "Car", "Brand", 2022, 1000, 12, VehicleStatus.AVAILABLE, 60, 0, 4))
    motorcycle_repo.save_motorcycle(Motorcycle("MOT-1D34", "Bike", "Brand", 2020, 2000, 15, VehicleStatus.AVAILABLE, 20, 0, 150))
    truck_repo.save_truck(Truck("TRK-1D34", "Truck", "Brand", 2018, 3000, 6, VehicleStatus.AVAILABLE, 300, 0, 15))
    driver_repo.save_driver(Driver("Driver", "80658405071", VehicleLicense.AB, 5, DriverStatus.AVAILABLE))

    return database


def test_maintenance_report_calculates_total_and_average_by_vehicle_type(persisted_data: Any) -> None:
    maintenance_repo = MaintenanceRepo(persisted_data)
    maintenance_repo.save_maintenance(("ABC-1D34", "preventive", 100, "oil", "date", "...", 1000))
    maintenance_repo.finish_maintenance("ABC-1D34", "1")
    maintenance_repo.save_maintenance(("ABC-1D34", "corrective", 300, "repair", "date", "...", 1000))
    maintenance_repo.finish_maintenance("ABC-1D34", "2")
    maintenance_repo.save_maintenance(("TRK-1D34", "preventive", 800, "service", "date", "...", 3000))
    vehicle_types = {"ABC-1D34": "car", "TRK-1D34": "truck"}

    result = build_maintenance_report(maintenance_repo.read_maintenances(), vehicle_types)

    assert result["total_cost"] == 1200
    assert result["average_cost_by_vehicle_type"] == {"car": 200, "truck": 800}


def test_fuel_efficiency_report_uses_stored_consumption_and_config(persisted_data: Any) -> None:
    controllers = [
        ("car", CarController(CarRepo(persisted_data)).get_by_plate("ABC-1D34")),
        ("motorcycle", MotorcycleController(MotorcycleRepo(persisted_data)).get_by_plate("MOT-1D34")),
        ("truck", TruckController(TruckRepo(persisted_data)).get_by_plate("TRK-1D34")),
    ]

    result = build_fuel_efficiency_report(controllers, SETTINGS)

    assert result["average_consumption"] == pytest.approx(11)
    assert [(kind, vehicle.plate) for kind, vehicle in result["ranking"]] == [
        ("motorcycle", "MOT-1D34"), ("car", "ABC-1D34"), ("truck", "TRK-1D34")
    ]
    assert [(kind, vehicle.plate) for kind, vehicle in result["outside_standard"]] == [
        ("motorcycle", "MOT-1D34")
    ]


def test_trip_report_counts_persisted_trips_by_driver(persisted_data: Any) -> None:
    trip_repo = TripRepo(persisted_data, SETTINGS)
    trip = Trip("80658405071", "ABC-1D34", "A", "B", 10, EnumTrip.IN_PROGRESS)
    trip.set_date_init()
    trip_repo.save_trip(trip)

    result = build_trip_report(
        DriverRepo(persisted_data).read_drivers(), trip_repo.read_trips()
    )

    assert result == [("Driver", "80658405071", 1)]


def test_mileage_report_calculates_mean_for_types(persisted_data: Any) -> None:
    car_controller = CarController(CarRepo(persisted_data))
    truck_controller = TruckController(TruckRepo(persisted_data))
    result = build_mileage_report({
        "car": [car_controller.get_by_plate("ABC-1D34")],
        "truck": [truck_controller.get_by_plate("TRK-1D34")],
        "motorcycle": [],
    })

    assert result == {"car": 1000, "truck": 3000}


def test_vehicle_report_reads_persisted_repository_rows(monkeypatch: Any, persisted_data: Any) -> None:
    controllers = (
        CarController(CarRepo(persisted_data)),
        MotorcycleController(MotorcycleRepo(persisted_data)),
        TruckController(TruckRepo(persisted_data)),
        None,
        None,
        None,
    )
    monkeypatch.setattr(reports, "_get_repositories", lambda: controllers)

    headers, rows = page_vehicle_status_report()

    assert len(headers) == 10
    assert {row[1] for row in rows} == {"ABC-1D34", "MOT-1D34", "TRK-1D34"}


@pytest.mark.parametrize(
    "selection, method_name",
    [
        ("maintenance", "_maintenance_report"),
        ("fuel", "_fuel_report"),
        ("trips", "_trip_report"),
        ("mileage", "_mileage_report"),
        ("vehicles", "_vehicle_report"),
    ],
)
def test_report_menu_routes_each_report(monkeypatch: Any, persisted_data: Any, selection: Any, method_name: Any) -> None:
    controllers = (
        CarController(CarRepo(persisted_data)),
        MotorcycleController(MotorcycleRepo(persisted_data)),
        TruckController(TruckRepo(persisted_data)),
        None,
        None,
        None,
    )
    called = []
    monkeypatch.setattr(reports, "_get_repositories", lambda: controllers)
    monkeypatch.setattr(reports.q, "select", lambda *args, **kwargs: Prompt(selection))
    monkeypatch.setattr(reports, method_name, lambda *args: called.append(selection))

    reports.page_reports()

    assert called == [selection]


def test_empty_vehicle_inventory_report_returns_headers_and_no_rows(monkeypatch: Any, database: Any) -> None:
    controllers = (
        CarController(CarRepo(database)),
        MotorcycleController(MotorcycleRepo(database)),
        TruckController(TruckRepo(database)),
        None,
        None,
        None,
    )
    monkeypatch.setattr(reports, "_get_repositories", lambda: controllers)

    headers, rows = reports.page_vehicle_status_report()

    assert headers
    assert rows == []


@pytest.mark.parametrize("selection", ["maintenance", "fuel", "trips", "mileage", "vehicles"])
def test_each_report_runs_with_empty_database(monkeypatch: Any, database: Any, selection: Any) -> None:
    controllers = (
        CarController(CarRepo(database)),
        MotorcycleController(MotorcycleRepo(database)),
        TruckController(TruckRepo(database)),
        type("DriverControllerStub", (), {"repo": DriverRepo(database)})(),
        TripController(TripRepo(database, SETTINGS)),
        MaintenanceController(MaintenanceRepo(database)),
    )
    monkeypatch.setattr(reports, "_get_repositories", lambda: controllers)
    monkeypatch.setattr(reports.q, "select", lambda *args, **kwargs: Prompt(selection))
    monkeypatch.setattr(reports, "_show_report", lambda *args: None)

    reports.page_reports()
