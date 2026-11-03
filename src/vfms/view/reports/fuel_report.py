from typing import Any

from vfms.view.reports.report_data import ReportRenderer, build_fuel_efficiency_report, get_vehicles_by_type, show_report


def page_fuel_report(
    controllers: tuple[Any, ...], render: ReportRenderer = show_report
) -> None:
    from vfms.depedencies import settings
    vehicles_by_type = get_vehicles_by_type(controllers)
    vehicles = [(kind, vehicle) for kind, items in vehicles_by_type.items() for vehicle in items]
    report = build_fuel_efficiency_report(vehicles, settings)
    average = report["average_consumption"]
    rows = [["Fleet average", "All vehicles", average if average is not None else "No data"]]
    rows.extend(["Ranking", f"{kind}: {vehicle.plate}", vehicle.average_consumption]
                for kind, vehicle in report["ranking"])
    rows.extend(["Outside configured range", f"{kind}: {vehicle.plate}", vehicle.average_consumption]
                for kind, vehicle in report["outside_standard"])
    render("Fuel efficiency", ["Measure", "Vehicle", "km/L"], rows)
