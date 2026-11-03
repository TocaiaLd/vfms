from typing import Any

from vfms.view.reports.report_data import ReportRenderer, build_maintenance_report, get_vehicles_by_type, show_report


def page_maintenance_report(
    controllers: tuple[Any, ...], render: ReportRenderer = show_report
) -> None:
    vehicles_by_type = get_vehicles_by_type(controllers)
    vehicle_types = {vehicle.plate: kind for kind, vehicles in vehicles_by_type.items() for vehicle in vehicles}
    report = build_maintenance_report(controllers[5].repo.read_maintenances(), vehicle_types)
    rows = [["Total cost", "All vehicles", report["total_cost"]]]
    rows.extend(["Average cost", kind, average]
                for kind, average in sorted(report["average_cost_by_vehicle_type"].items()))
    render("Maintenance costs", ["Measure", "Vehicle type", "Cost"], rows)
