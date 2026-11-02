# External libs
import questionary as q
from vfms.utilities.clear_screen import clear_screen

from vfms.view.reports.reports import page_reports

def menu_reports() -> None:
    while True:
        clear_screen()
        selection = q.select(
            message="|----- Reports Menu -----|",
            choices=[
                q.Choice(title="Vehicles reports", value=page_reports),
                q.Choice(title="Back to main menu", value=False),
            ],
        ).ask()

        if selection is None or selection is False:
            clear_screen()
            return

        selection()
        clear_screen()
