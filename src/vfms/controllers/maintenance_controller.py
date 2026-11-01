from vfms.repos.maintenance_repo import MaintenanceRepo

class MaintenanceController():
    def __init__(
        self : MaintenanceController,
        repo : MaintenanceRepo,
    ):
        self.repo = repo

    def save_maintenance(
        self        : MaintenanceController,
        maintenance : tuple
    ) -> str:
        return self.repo.save_maintenance(maintenance)