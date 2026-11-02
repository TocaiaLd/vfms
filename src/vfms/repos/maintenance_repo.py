from datetime import datetime
import sqlite3
from typing import Any

from vfms.enums.vehicle_status import VehicleStatus
from vfms.exceptions import ManutencaoInvalidaError, RepositorioError
from vfms.repos.repo import Repo


VEHICLE_TABLES = ("cars", "trucks", "motorcycles")


class MaintenanceRepo:
    # Persist maintenance records and coordinate vehicle maintenance state.

    def __init__(self, repo: Repo) -> None:
        self.repo = repo

    def save_maintenance(self, maintenance: tuple[Any, ...]) -> str:
        # Save a maintenance record and mark its vehicle as under maintenance.
        plate = maintenance[0]
        try:
            with self.repo._con:
                found = None
                for table in VEHICLE_TABLES:
                    row = self.repo.execute(
                        f"SELECT status, mileage FROM {table} WHERE plate = ?",
                        (plate,),
                    ).fetchone()
                    if row is not None:
                        found = (table, row)
                        break
                if found is None:
                    raise ManutencaoInvalidaError("Vehicle plate does not exist")

                table, (status, mileage) = found
                if status != VehicleStatus.AVAILABLE.name:
                    raise ManutencaoInvalidaError("Vehicle must be available for maintenance")

                date_init = maintenance[4]
                if isinstance(date_init, datetime):
                    date_init = date_init.isoformat(timespec="seconds")
                mileage_snapshot = maintenance[6] if len(maintenance) > 6 else mileage

                self.repo.execute(
                    f"UPDATE {table} SET status = ? WHERE plate = ?",
                    (VehicleStatus.MAINTENANCE.name, plate),
                )
                self.repo.execute(
                    "INSERT INTO maintenances (plate, type, price, description, date_init, date_end, mileage) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (*maintenance[:4], date_init, maintenance[5], mileage_snapshot),
                )
        except sqlite3.Error as exc:
            raise RepositorioError("Could not save maintenance") from exc

        return "Maintenance saved."

    def read_maintenances(self) -> list[tuple[Any, ...]]:
        return self.repo.execute("SELECT * FROM maintenances").fetchall()

    def get_maintenance_by_id(self, maintenance_id: str) -> list[tuple[Any, ...]] | bool:
        maintenance = self.repo.execute(
            "SELECT * FROM maintenances WHERE id = ?", (maintenance_id,)
        ).fetchall()
        return maintenance if maintenance else False

    def finish_maintenance(self, vehicle_plate: str, maintenance_id: str) -> str:
        # Finish an open maintenance and return its vehicle to available state.
        try:
            int_maintenance_id = int(maintenance_id)
        except (TypeError, ValueError) as exc:
            raise ValueError("Maintenance id must be an integer") from exc

        try:
            with self.repo._con:
                record = self.repo.execute(
                    "SELECT plate, date_end FROM maintenances WHERE id = ?",
                    (int_maintenance_id,),
                ).fetchone()
                if record is None or record[0] != vehicle_plate:
                    return "Maintenance does not exist for this vehicle."
                if record[1] != "...":
                    return "Maintenance was already ended."

                found_table = next(
                    (
                        table
                        for table in VEHICLE_TABLES
                        if self.repo.execute(
                            f"SELECT 1 FROM {table} WHERE plate = ?", (vehicle_plate,)
                        ).fetchone()
                    ),
                    None,
                )
                if found_table is None:
                    raise ManutencaoInvalidaError("Maintenance vehicle does not exist")

                self.repo.execute(
                    f"UPDATE {found_table} SET status = ? WHERE plate = ?",
                    (VehicleStatus.AVAILABLE.name, vehicle_plate),
                )
                self.repo.execute(
                    "UPDATE maintenances SET date_end = ? WHERE id = ?",
                    (datetime.now().isoformat(timespec="seconds"), int_maintenance_id),
                )
        except sqlite3.Error as exc:
            raise RepositorioError("Could not finish maintenance") from exc

        return "Maintenance finished."
