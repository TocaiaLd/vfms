from typing import Any

from vfms.view.reports.report_data import build_trip_report, show_report


def page_trip_report(driver_controller: Any, trip_controller: Any, render=show_report) -> None:
    rows = build_trip_report(driver_controller.repo.read_drivers(), trip_controller.repo.read_trips())
    render("Trips by driver", ["Driver", "CPF", "Trips"], [list(row) for row in rows])
