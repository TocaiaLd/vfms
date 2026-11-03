# Reports submenu and backwards-compatible report entry points.

from typing import Any

import questionary as q

from vfms.view.reports.report_data import (
    build_fuel_efficiency_report,
    build_maintenance_report,
    build_mileage_report,
    build_trip_report,
    get_repositories,
    get_vehicles_by_type,
    show_report,
)
from vfms.view.reports.fuel_report import page_fuel_report
from vfms.view.reports.maintenance_report import page_maintenance_report
from vfms.view.reports.mileage_report import page_mileage_report
from vfms.view.reports.trip_report import page_trip_report


def _get_repositories() -> tuple[Any, ...]:
    return get_repositories()


def _get_vehicles_by_type(controllers: tuple[Any, ...]) -> dict[str, list[Any]]:
    return get_vehicles_by_type(controllers)


def _show_report(title: str, headers: list[str], rows: list[list[Any]]) -> None:
    show_report(title, headers, rows)


def page_vehicle_status_report() -> tuple[list[str], list[list[Any]]]:
    controllers = _get_repositories()
    vehicles = _get_vehicles_by_type(controllers)
    headers = ["Type", "Plate", "Model", "Brand", "Year", "Mileage", "Consumption", "Status", "Max fuel", "Fuel"]
    rows = [[kind, vehicle.plate, vehicle.model, vehicle.brand, vehicle.year,
             vehicle.mileage, vehicle.average_consumption, vehicle.status.name,
             vehicle.max_fuel, vehicle.fuel]
            for kind, items in vehicles.items() for vehicle in items]
    return headers, rows


def _maintenance_report(controllers: tuple[Any, ...]) -> None:
    page_maintenance_report(controllers, _show_report)


def _fuel_report(controllers: tuple[Any, ...]) -> None:
    page_fuel_report(controllers, _show_report)


def _trip_report(driver_controller: Any, trip_controller: Any) -> None:
    page_trip_report(driver_controller, trip_controller, _show_report)


def _mileage_report(controllers: tuple[Any, ...]) -> None:
    page_mileage_report(controllers, _show_report)


def _vehicle_report(controllers: tuple[Any, ...]) -> None:
    headers, rows = page_vehicle_status_report()
    _show_report("All vehicles", headers, rows)


def page_reports() -> None:
    controllers = _get_repositories()
    _, _, _, driver_controller, trip_controller, _ = controllers
    reports = {
        "maintenance": lambda: _maintenance_report(controllers),
        "fuel": lambda: _fuel_report(controllers),
        "trips": lambda: _trip_report(driver_controller, trip_controller),
        "mileage": lambda: _mileage_report(controllers),
        "vehicles": lambda: _vehicle_report(controllers),
    }
    selection = q.select(
        "Choose a report type:",
        choices=[
            q.Choice(title="Maintenance costs", value="maintenance"),
            q.Choice(title="Fuel efficiency", value="fuel"),
            q.Choice(title="Trips by driver", value="trips"),
            q.Choice(title="Average mileage by vehicle type", value="mileage"),
            q.Choice(title="All vehicles", value="vehicles"),
            q.Choice(title="Back to reports menu", value=None),
        ],
    ).ask()
    if selection in reports:
        reports[selection]()
