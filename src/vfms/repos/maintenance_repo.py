from vfms.enums.vehicle_status import VehicleStatus
from vfms.repos.repo import Repo

class MaintenanceRepo:
    def __init__(
        self    : MaintenanceRepo,
        repo    : Repo
    ):
        self.repo = repo

    def save_maintenance(
        self        : MaintenanceRepo,
        maintenance : tuple
    ) -> str:

        types = ["cars", "trucks", "motorcycles"]

        for n in types:
            self.repo._cursor.execute(f"SELECT * FROM {n} WHERE PLATE = ?", (maintenance[0],))
            result = self.repo._cursor.fetchall()

            if result:
                self.repo._cursor.execute(f"UPDATE {n} SET status = ? WHERE plate = ?;", (VehicleStatus.MAINTENANCE.name, maintenance.plate))
                self.repo._con.commit()
                break

        self.repo._cursor.execute("INSERT INTO maintenances (plate, type, price, description, date) VALUES (?, ?, ?, ?, ?)", maintenance)
        self.repo._con.commit()

        return "Maintenance saved."