from datetime import datetime
import sqlite3
from typing import Any

from vfms.config.settings_validations import is_license_compatible
from vfms.enums.driver_status import DriverStatus
from vfms.enums.enum_trip import EnumTrip
from vfms.enums.vehicle_status import VehicleStatus
from vfms.exceptions import AlocacaoInvalidaError, PoliticaNaoAtendidaError, RepositorioError
from vfms.models.trip import Trip
from vfms.repos.repo import Repo


VEHICLE_TABLES = ("cars", "trucks", "motorcycles")


class TripRepo:
    # Persist trips and update the related driver and vehicle state.

    def __init__(self, repo: Repo, settings: dict[str, Any] | None = None) -> None:
        self.repo = repo
        self.settings = settings

    def _get_settings(self) -> dict[str, Any]:
        if self.settings is not None:
            return self.settings
        from vfms.depedencies import settings
        return settings

    def save_trip(self, trip: Trip) -> str:
        # Assign an available driver and vehicle, then store the trip.
        if trip.distance <= 0:
            raise AlocacaoInvalidaError("Trip distance must be greater than zero")

        driver = self.repo.execute(
            "SELECT status, license FROM drivers WHERE cpf = ?", (trip.driver_cpf,)
        ).fetchone()
        if driver is None:
            raise AlocacaoInvalidaError("Driver CPF does not exist")
        if driver[0] != DriverStatus.AVAILABLE.name:
            raise AlocacaoInvalidaError("Driver is not available")

        found_vehicle = None
        for table in VEHICLE_TABLES:
            row = self.repo.execute(
                f"SELECT status, license FROM {table} WHERE plate = ?",
                (trip.vehicle_plate,),
            ).fetchone()
            if row is not None:
                found_vehicle = (table, row)
                break
        if found_vehicle is None:
            raise AlocacaoInvalidaError("Vehicle plate does not exist")

        table, vehicle = found_vehicle
        if vehicle[0] != VehicleStatus.AVAILABLE.name:
            if vehicle[0] == VehicleStatus.MAINTENANCE.name:
                raise AlocacaoInvalidaError("Vehicle is under maintenance")
            if vehicle[0] == VehicleStatus.INACTIVE.name:
                raise AlocacaoInvalidaError("Vehicle is inactive")
            raise AlocacaoInvalidaError("Vehicle is not available")

        vehicle_type = {"cars": "car", "trucks": "truck", "motorcycles": "motorcycle"}[table]
        if not is_license_compatible(self._get_settings(), vehicle_type, driver[1]):
            raise PoliticaNaoAtendidaError("Driver license is not compatible with this vehicle")

        try:
            with self.repo._con:
                self.repo.execute(
                    f"UPDATE {table} SET status = ? WHERE plate = ?",
                    (VehicleStatus.ON_TRIP.name, trip.vehicle_plate),
                )
                self.repo.execute(
                    "UPDATE drivers SET status = ? WHERE cpf = ?",
                    (DriverStatus.ON_TRIP.name, trip.driver_cpf),
                )
                self.repo.execute(
                    "INSERT INTO trips (driver_cpf, vehicle_plate, origin, destiny, distance, status, date_init, date_end) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        trip.driver_cpf,
                        trip.vehicle_plate,
                        trip.origin,
                        trip.destiny,
                        trip.distance,
                        trip.status.value,
                        (trip.date_init or datetime.now()).isoformat(timespec="seconds"),
                        "...",
                    ),
                )
        except sqlite3.Error as exc:
            raise RepositorioError("Could not save trip") from exc

        return "Trip saved."

    def finish_trip(self, trip: Trip, trip_id: str) -> str:
        # Finish a trip and apply mileage and preventive-service rules.
        try:
            int_trip_id = int(trip_id)
        except (TypeError, ValueError) as exc:
            raise ValueError("Trip id must be an integer") from exc

        interval = self._get_settings()["maintenance"]["preventive_interval_km"]
        try:
            with self.repo._con:
                stored_trip = self.repo.execute(
                    "SELECT status FROM trips WHERE trip_id = ?", (int_trip_id,)
                ).fetchone()
                if stored_trip is None:
                    return "Trip does not exist."
                if stored_trip[0] == EnumTrip.ENDED.value:
                    return "Trip was already ended."

                found_vehicle = None
                for table in VEHICLE_TABLES:
                    vehicle = self.repo.execute(
                        f"SELECT mileage FROM {table} WHERE plate = ?",
                        (trip.vehicle_plate,),
                    ).fetchone()
                    if vehicle is not None:
                        found_vehicle = (table, float(vehicle[0] or 0))
                        break
                if found_vehicle is None:
                    raise AlocacaoInvalidaError("Trip vehicle no longer exists")

                table, mileage_before = found_vehicle
                mileage_after = mileage_before + trip.distance
                last_service = self.repo.execute(
                    "SELECT mileage FROM maintenances WHERE plate = ? AND type = ? AND date_end != ? AND mileage IS NOT NULL ORDER BY id DESC LIMIT 1",
                    (trip.vehicle_plate, "preventive", "..."),
                ).fetchone()
                mileage_at_last_service = float(last_service[0]) if last_service else 0.0
                next_service_at = mileage_at_last_service + interval
                vehicle_status = (
                    VehicleStatus.MAINTENANCE.name
                    if mileage_after >= next_service_at
                    else VehicleStatus.AVAILABLE.name
                )

                self.repo.execute(
                    f"UPDATE {table} SET status = ?, mileage = ? WHERE plate = ?",
                    (vehicle_status, mileage_after, trip.vehicle_plate),
                )
                self.repo.execute(
                    "UPDATE drivers SET status = ? WHERE cpf = ?",
                    (DriverStatus.AVAILABLE.name, trip.driver_cpf),
                )
                self.repo.execute(
                    "UPDATE trips SET status = ?, date_end = ? WHERE trip_id = ?",
                    (
                        EnumTrip.ENDED.value,
                        (trip.date_end or datetime.now()).isoformat(timespec="seconds"),
                        int_trip_id,
                    ),
                )
        except sqlite3.Error as exc:
            raise RepositorioError("Could not finish trip") from exc

        return "Trip finished."

    def get_trip_by_id(self, trip_id: str) -> list[tuple[Any, ...]] | bool:
        self.repo.execute("SELECT * FROM trips WHERE trip_id = ?", (trip_id,))
        trip = self.repo._cursor.fetchall()
        return trip if trip else False

    def read_trips(self) -> list[tuple[Any, ...]]:
        return self.repo.execute("SELECT * FROM trips").fetchall()
