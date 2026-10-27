# External libs
import questionary as q

from vfms.view.reports.reports import page_reports

def menu_reports():
    input = q.select(
        message = "|----- Reports Menu -----|",
        choices = [
            q.Choice(
                title   = "Vehicles reports",
                value   = page_reports
            ), 
            q.Choice(
                title   = "Back to main menu", 
                value   = False
            ), 
        ]
    ).ask()

    if input:
        input()