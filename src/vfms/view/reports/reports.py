from collections import Counter, defaultdict
from statistics import fmean
from typing import Any, Iterable

import questionary as q
from tabulate import tabulate

from vfms.config.settings_validations import is_consumption_acceptable


def build_maintenance_report(
    maintenances: Iterable[tuple[Any, ...]],
    vehicle_types: dict[str, str],
) -> dict[str, Any]:
    # Calculate total and per-vehicle-type mean maintenance costs.
    costs: dict[str, list[float]] = defaultdict(list)
    total = 0.0
    for maintenance in maintenances:
        if maintenance[3] is None:
            continue
        cost = float(maintenance[3])
        total += cost
        vehicle_type = vehicle_types.get(maintenance[1])
        if vehicle_type is None:
            continue
        costs[vehicle_type].append(cost)

    return {
        "total_cost": total,
        "average_cost_by_vehicle_type": {
            vehicle_type: fmean(values) for vehicle_type, values in costs.items()
        },
    }


def build_fuel_efficiency_report(
    vehicles: Iterable[tuple[str, Any]], settings: dict[str, Any]
) -> dict[str, Any]:
    # Calculate average consumption, efficiency ranking, and policy violations.
    vehicles = list(vehicles)
    consumptions = [float(vehicle.average_consumption) for _, vehicle in vehicles]
    ranking = sorted(vehicles, key=lambda item: item[1].average_consumption, reverse=True)
    outside_standard = [
        (vehicle_type, vehicle)
        for vehicle_type, vehicle in vehicles
        if not is_consumption_acceptable(settings, vehicle)
    ]
    return {
        "average_consumption": fmean(consumptions) if consumptions else None,
        "ranking": ranking,
        "outside_standard": outside_standard,
    }


def build_trip_report(
    drivers: Iterable[tuple[Any, ...]], trips: Iterable[tuple[Any, ...]]
) -> list[tuple[str, str, int]]:
    # Count persisted trips for each driver, including drivers with no trips.
    def cpf_key(value: Any) -> str:
        text = str(value)
        return text.zfill(11) if text.isdigit() else text

    counts = Counter(cpf_key(trip[1]) for trip in trips if trip[1] is not None)
    return [
        (driver[0], str(driver[1]), counts[cpf_key(driver[1])])
        for driver in drivers
    ]


def build_mileage_report(
    vehicles_by_type: dict[str, Iterable[Any]],
) -> dict[str, float]:
    # Calculate the persisted mean odometer reading for each vehicle type.
    result = {}
    for vehicle_type, vehicles in vehicles_by_type.items():
        mileages = [float(vehicle.mileage) for vehicle in vehicles]
        if mileages:
            result[vehicle_type] = fmean(mileages)
    return result


def _get_repositories() -> tuple[Any, ...]:
    # Import the application registry only when the user opens a report.
    from vfms.depedencies import MasterController

    return (
        MasterController.CAR_CONTROLLER.value,
        MasterController.MOTORCYCLE_CONTROLLER.value,
        MasterController.TRUCK_CONTROLLER.value,
        MasterController.DRIVER_CONTROLLER.value,
        MasterController.TRIP_CONTROLLER.value,
        MasterController.MAINTENANCE_CONTROLLER.value,
    )


def _get_vehicles_by_type(controllers: tuple[Any, ...]) -> dict[str, list[Any]]:
    car, motorcycle, truck = controllers[:3]
    sources = {
        "car": (car, "show_cars"),
        "motorcycle": (motorcycle, "show_motorcycles"),
        "truck": (truck, "show_trucks"),
    }
    result: dict[str, list[Any]] = {}
    for vehicle_type, (controller, method_name) in sources.items():
        rows = getattr(controller.repo, method_name)()
        result[vehicle_type] = [
            vehicle
            for row in rows
            if (vehicle := controller.get_by_plate(row[0]))
        ]
    return result


def _show_report(title: str, headers: list[str], rows: list[list[Any]]) -> None:
    print(f"|----- {title} -----|")
    print(tabulate(rows, headers=headers, tablefmt="fancy_grid"))
    q.text("Press any key to return to the reports menu").ask()


def page_vehicle_status_report() -> tuple[list[str], list[list[Any]]]:
    # Return a report of all persisted vehicles and their current values.
    controllers = _get_repositories()
    vehicles = _get_vehicles_by_type(controllers)
    headers = ["Type", "Plate", "Model", "Brand", "Year", "Mileage", "Consumption", "Status", "Max fuel", "Fuel"]
    rows = [
        [vehicle_type, vehicle.plate, vehicle.model, vehicle.brand, vehicle.year,
         vehicle.mileage, vehicle.average_consumption, vehicle.status.name,
         vehicle.max_fuel, vehicle.fuel]
        for vehicle_type, items in vehicles.items()
        for vehicle in items
    ]
    return headers, rows


def page_reports() -> None:
    # Display a selected report using the current persisted database records.
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
    if selection not in reports:
        return
    reports[selection]()


def _maintenance_report(controllers: tuple[Any, ...]) -> None:
    vehicles_by_type = _get_vehicles_by_type(controllers)
    vehicle_types = {
        vehicle.plate: vehicle_type
        for vehicle_type, vehicles in vehicles_by_type.items()
        for vehicle in vehicles
    }
    records = controllers[5].repo.read_maintenances()
    report = build_maintenance_report(records, vehicle_types)
    rows = [["Total cost", "All vehicles", report["total_cost"]]]
    rows.extend(
        ["Average cost", vehicle_type, average]
        for vehicle_type, average in sorted(report["average_cost_by_vehicle_type"].items())
    )
    _show_report("Maintenance costs", ["Measure", "Vehicle type", "Cost"], rows)


def _fuel_report(controllers: tuple[Any, ...]) -> None:
    from vfms.depedencies import settings

    vehicles_by_type = _get_vehicles_by_type(controllers)
    vehicles = [
        (vehicle_type, vehicle)
        for vehicle_type, items in vehicles_by_type.items()
        for vehicle in items
    ]
    report = build_fuel_efficiency_report(vehicles, settings)
    average = report["average_consumption"]
    rows = [["Fleet average", "All vehicles", average if average is not None else "No data"]]
    rows.extend(
        ["Ranking", f"{vehicle_type}: {vehicle.plate}", vehicle.average_consumption]
        for vehicle_type, vehicle in report["ranking"]
    )
    rows.extend(
        ["Outside configured range", f"{vehicle_type}: {vehicle.plate}", vehicle.average_consumption]
        for vehicle_type, vehicle in report["outside_standard"]
    )
    _show_report("Fuel efficiency", ["Measure", "Vehicle", "km/L"], rows)


def _trip_report(driver_controller: Any, trip_controller: Any) -> None:
    rows = build_trip_report(
        driver_controller.repo.read_drivers(), trip_controller.repo.read_trips()
    )
    _show_report("Trips by driver", ["Driver", "CPF", "Trips"], [list(row) for row in rows])


def _mileage_report(controllers: tuple[Any, ...]) -> None:
    vehicles_by_type = _get_vehicles_by_type(controllers)
    report = build_mileage_report(vehicles_by_type)
    rows = [[vehicle_type, mileage] for vehicle_type, mileage in sorted(report.items())]
    _show_report("Average mileage", ["Vehicle type", "Average km"], rows)


def _vehicle_report(controllers: tuple[Any, ...]) -> None:
    headers, rows = page_vehicle_status_report()
    _show_report("All vehicles", headers, rows)
