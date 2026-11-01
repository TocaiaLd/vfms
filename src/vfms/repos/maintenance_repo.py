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
        self.repo._cursor.execute("INSERT INTO maintenances (plate, type, price, description, date) VALUES (?, ?, ?, ?, ?)", maintenance)
        self.repo._con.commit()

        return "Maintenance saved."