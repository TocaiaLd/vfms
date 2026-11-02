from datetime import datetime
from tabulate import tabulate

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

    def show_maintenances(self) -> str:
        response = self.repo.read_maintenances()

        collumns = ["id", "plate", "type", "price", "description", "date_init", "date_end"]
        data = []

        for d in response:
            data.append([d[0], d[1], d[2], d[3], d[4], d[5], d[6]])
    
        response = tabulate(data, headers=collumns, tablefmt="fancy_grid")

        return response

    def get_maintenance_by_id(self, maintenance_id):
        maintenance = self.repo.get_maintenance_by_id(maintenance_id)
        
        if maintenance:
            return maintenance
        
        return False

    def finish_maintenance(self, maintenance_id):
        maintenance = self.get_maintenance_by_id(maintenance_id)
        
        if maintenance:
            if maintenance[0][6] != "...":
                return "This maintenance was already ended"

            return self.repo.finish_maintenance(maintenance[0][1], maintenance[0][0])

        return "this trip doenst exists"