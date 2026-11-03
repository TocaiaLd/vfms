from typing import Any

from vfms.view.reports.report_data import ReportRenderer, get_vehicles_by_type, show_report


def page_vehicle_status_report() -> tuple[list[str], list[list[Any]]]:
    from vfms.view.reports.report_data import get_repositories
    vehicles = get_vehicles_by_type(get_repositories())
    headers = ["Type", "Plate", "Model", "Brand", "Year", "Mileage", "Consumption", "Status", "Max fuel", "Fuel"]
    rows = [[kind, vehicle.plate, vehicle.model, vehicle.brand, vehicle.year,
             vehicle.mileage, vehicle.average_consumption, vehicle.status.name,
             vehicle.max_fuel, vehicle.fuel]
            for kind, items in vehicles.items() for vehicle in items]
    return headers, rows


def page_all_vehicles_report(
    controllers: tuple[Any, ...], render: ReportRenderer = show_report
) -> None:
    vehicles = get_vehicles_by_type(controllers)
    headers = ["Type", "Plate", "Model", "Brand", "Year", "Mileage", "Consumption", "Status", "Max fuel", "Fuel"]
    rows = [[kind, vehicle.plate, vehicle.model, vehicle.brand, vehicle.year,
             vehicle.mileage, vehicle.average_consumption, vehicle.status.name,
             vehicle.max_fuel, vehicle.fuel]
            for kind, items in vehicles.items() for vehicle in items]
    render("All vehicles", headers, rows)
