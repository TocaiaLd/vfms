# Report calculations and shared repository access.

from collections import Counter, defaultdict
from collections.abc import Callable
from statistics import fmean
from typing import Any, Iterable

from vfms.config.settings_validations import is_consumption_acceptable

ReportRenderer = Callable[[str, list[str], list[list[Any]]], None]


def build_maintenance_report(maintenances: Iterable[tuple[Any, ...]], vehicle_types: dict[str, str]) -> dict[str, Any]:
    costs: dict[str, list[float]] = defaultdict(list)
    total = 0.0
    for maintenance in maintenances:
        if maintenance[3] is None:
            continue
        cost = float(maintenance[3])
        total += cost
        vehicle_type = vehicle_types.get(maintenance[1])
        if vehicle_type is not None:
            costs[vehicle_type].append(cost)
    return {"total_cost": total, "average_cost_by_vehicle_type": {
        vehicle_type: fmean(values) for vehicle_type, values in costs.items()
    }}


def build_fuel_efficiency_report(vehicles: Iterable[tuple[str, Any]], settings: dict[str, Any]) -> dict[str, Any]:
    vehicles = list(vehicles)
    consumptions = [float(vehicle.average_consumption) for _, vehicle in vehicles]
    return {
        "average_consumption": fmean(consumptions) if consumptions else None,
        "ranking": sorted(vehicles, key=lambda item: item[1].average_consumption, reverse=True),
        "outside_standard": [(kind, vehicle) for kind, vehicle in vehicles
                             if not is_consumption_acceptable(settings, vehicle)],
    }


def build_trip_report(drivers: Iterable[tuple[Any, ...]], trips: Iterable[tuple[Any, ...]]) -> list[tuple[str, str, int]]:
    def cpf_key(value: Any) -> str:
        text = str(value)
        return text.zfill(11) if text.isdigit() else text
    counts = Counter(cpf_key(trip[1]) for trip in trips if trip[1] is not None)
    return [(driver[0], str(driver[1]), counts[cpf_key(driver[1])]) for driver in drivers]


def build_mileage_report(vehicles_by_type: dict[str, Iterable[Any]]) -> dict[str, float]:
    result = {}
    for vehicle_type, vehicles in vehicles_by_type.items():
        mileages = [float(vehicle.mileage) for vehicle in vehicles]
        if mileages:
            result[vehicle_type] = fmean(mileages)
    return result


def get_repositories() -> tuple[Any, ...]:
    from vfms.depedencies import MasterController
    return (
        MasterController.CAR_CONTROLLER.value, MasterController.MOTORCYCLE_CONTROLLER.value,
        MasterController.TRUCK_CONTROLLER.value, MasterController.DRIVER_CONTROLLER.value,
        MasterController.TRIP_CONTROLLER.value, MasterController.MAINTENANCE_CONTROLLER.value,
    )


def get_vehicles_by_type(controllers: tuple[Any, ...]) -> dict[str, list[Any]]:
    car, motorcycle, truck = controllers[:3]
    sources = {"car": (car, "show_cars"), "motorcycle": (motorcycle, "show_motorcycles"), "truck": (truck, "show_trucks")}
    result: dict[str, list[Any]] = {}
    for kind, (controller, method) in sources.items():
        result[kind] = [vehicle for row in getattr(controller.repo, method)()
                        if (vehicle := controller.get_by_plate(row[0]))]
    return result


def show_report(title: str, headers: list[str], rows: list[list[Any]]) -> None:
    import questionary as q
    from tabulate import tabulate
    print(f"|----- {title} -----|")
    print(tabulate(rows, headers=headers, tablefmt="fancy_grid"))
    q.text("Press any key to return to the reports menu").ask()
