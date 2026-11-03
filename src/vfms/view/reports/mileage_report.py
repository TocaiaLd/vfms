from typing import Any

from vfms.view.reports.report_data import build_mileage_report, get_vehicles_by_type, show_report


def page_mileage_report(controllers: tuple[Any, ...], render=show_report) -> None:
    report = build_mileage_report(get_vehicles_by_type(controllers))
    rows = [[kind, mileage] for kind, mileage in sorted(report.items())]
    render("Average mileage", ["Vehicle type", "Average km"], rows)
