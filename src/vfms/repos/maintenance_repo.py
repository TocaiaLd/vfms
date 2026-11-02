from typing import Any

from datetime import datetime
from vfms.enums.vehicle_status import VehicleStatus
from vfms.repos.repo import Repo

class MaintenanceRepo:
    def __init__(
        self    : MaintenanceRepo,
        repo    : Repo
    ) -> None:
        self.repo = repo

    def save_maintenance(
        self        : MaintenanceRepo,
        maintenance : tuple[Any, ...]
    ) -> str:

        types = ["cars", "trucks", "motorcycles"]

        for n in types:
            self.repo._cursor.execute(f"SELECT * FROM {n} WHERE PLATE = ?", (maintenance[0],))
            result = self.repo._cursor.fetchall()

            if result:
                self.repo._cursor.execute(f"UPDATE {n} SET status = ? WHERE plate = ?;", (VehicleStatus.MAINTENANCE.name, maintenance[0]))
                self.repo._con.commit()
                break

        self.repo._cursor.execute("INSERT INTO maintenances (plate, type, price, description, date_init, date_end) VALUES (?, ?, ?, ?, ?, ?)", maintenance)
        self.repo._con.commit()

        return "Maintenance saved."

    def read_maintenances(self) -> list[tuple[Any, ...]]:
        self.repo._cursor.execute("SELECT * FROM maintenances")
        trips = self.repo._cursor.fetchall()

        return trips

    def get_maintenance_by_id(self, maintenance_id: str) -> list[tuple[Any, ...]] | bool:
        self.repo._cursor.execute("SELECT * FROM maintenances WHERE id = ?", (maintenance_id,))
        maintenance = self.repo._cursor.fetchall()

        if maintenance:
            return maintenance
        
        return False

    def finish_maintenance(
        self            : MaintenanceRepo, 
        vehicle_plate   : str,
        maintenance_id  : str, 
    ) -> str:
        int_maintenance_id = int(maintenance_id)

        types = ["cars", "trucks", "motorcycles"]

        for n in types:
            self.repo._cursor.execute(f"SELECT * FROM {n} WHERE PLATE = ?", (vehicle_plate,))
            result = self.repo._cursor.fetchall()

            if result:
                self.repo._cursor.execute(f"UPDATE {n} SET status = ? WHERE plate = ?;", (VehicleStatus.AVAILABLE.name, vehicle_plate))
                self.repo._con.commit()
                break
    
        self.repo._cursor.execute("UPDATE maintenances SET date_end = ? WHERE id = ?;", (datetime.now(), int_maintenance_id))
        self.repo._con.commit()

        return "maintenance finished."