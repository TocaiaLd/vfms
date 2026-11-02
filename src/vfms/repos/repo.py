import sqlite3
import os
from pathlib import Path
from vfms.exceptions import RepositorioError

class Repo():
    # Own the SQLite connection and initialize the application's schema.

    def __init__(self, database_path: str | Path | None = None) -> None:
        database_path = database_path or os.environ.get(
            "VFMS_DATABASE_PATH", "db/sqlite3.db"
        )
        try:
            self._con = sqlite3.connect(database_path)
        except sqlite3.Error as exc:
            raise RepositorioError("Could not open the SQLite database") from exc
        self._cursor    = self._con.cursor()

        try:
            self._cursor.execute("PRAGMA foreign_keys = ON;")
            self.create_cars_table()
            self.create_trucks_table()
            self.create_motorcycles_table()
            self.create_drivers_table()
            self.create_vehicles_table()
            self.create_vehicles_table_triggers()
            self.create_refuels_table()
            self.create_trips_table()
            self._ensure_trip_driver_cpf_text()
            self.create_maintenances_table()
            self._ensure_maintenance_mileage_column()
            self._con.commit()
        except sqlite3.Error as exc:
            self._con.close()
            raise RepositorioError("Could not initialize the SQLite schema") from exc

    def close(self) -> None:
        # Close the SQLite connection owned by this repository.
        self._con.close()

    def execute(self, sql: str, parameters: tuple[Any, ...] = ()) -> sqlite3.Cursor:
        # Execute a repository query and expose SQLite failures consistently.
        try:
            return self._cursor.execute(sql, parameters)
        except sqlite3.Error as exc:
            raise RepositorioError("SQLite query failed") from exc

    def commit(self) -> None:
        # Commit a repository write and identify persistence failures.
        try:
            self._con.commit()
        except sqlite3.Error as exc:
            raise RepositorioError("Could not commit database changes") from exc

    def create_cars_table(self) -> None:
        self._cursor.execute("""
CREATE TABLE IF NOT EXISTS cars (
    plate TEXT NOT NULL PRIMARY KEY,
    model TEXT NOT NULL,
    brand TEXT NOT NULL,
    year INTEGER,
    mileage REAL,
    average_consumption REAL,
    status TEXT NOT NULL,
    max_fuel REAL,
    fuel REAL,
    ports INTEGER,
    license TEXT NOT NULL
)
""")

    def create_trucks_table(self) -> None:
        self._cursor.execute("""
CREATE TABLE IF NOT EXISTS trucks (
    plate TEXT NOT NULL PRIMARY KEY,
    model TEXT NOT NULL,
    brand TEXT NOT NULL,
    year INTEGER,
    mileage REAL,
    average_consumption REAL,
    status TEXT NOT NULL,
    max_fuel REAL,
    fuel REAL,
    max_weight REAL,
    license TEXT NOT NULL
)
""")

    def create_motorcycles_table(self) -> None:
        self._cursor.execute("""
CREATE TABLE IF NOT EXISTS motorcycles (
    plate TEXT NOT NULL PRIMARY KEY,
    model TEXT NOT NULL,
    brand TEXT NOT NULL,
    year INTEGER,
    mileage REAL,
    average_consumption REAL,
    status TEXT NOT NULL,
    max_fuel REAL,
    fuel REAL,
    cc REAL,
    license TEXT NOT NULL
)
""")

    def create_drivers_table(self) -> None:
        self._cursor.execute("""
CREATE TABLE IF NOT EXISTS drivers (
    name TEXT NOT NULL,
    cpf TEXT NOT NULL PRIMARY KEY,
    license TEXT NOT NULL,
    xp INTEGER,
    status TEXT NOT NULL
)
""")

    def create_trips_table(self) -> None:
        self._cursor.execute("""
CREATE TABLE IF NOT EXISTS trips (
    trip_id INTEGER PRIMARY KEY AUTOINCREMENT,
    driver_cpf TEXT,
    vehicle_plate TEXT NOT NULL,
    origin TEXT NOT NULL,
    destiny TEXT NOT NULL,
    distance REAL,
    status TEXT NOT NULL,
    date_init TEXT NOT NULL,
    date_end TEXT NOT NULL,
    FOREIGN KEY (driver_cpf) REFERENCES drivers (cpf),
    FOREIGN KEY (vehicle_plate) REFERENCES vehicles (plate)
)
""")

    def create_vehicles_table(self) -> None:
        self._cursor.execute("""
CREATE TABLE IF NOT EXISTS vehicles (
    plate TEXT NOT NULL PRIMARY KEY,
    model TEXT NOT NULL,
    brand TEXT NOT NULL,
    year INTEGER,
    mileage REAL,
    average_consumption REAL,
    status TEXT NOT NULL,
    max_fuel REAL,
    fuel REAL,
    license TEXT NOT NULL
)
""")

    def create_vehicles_table_triggers(self) -> None:
        list_of_vehicles = ["cars", "trucks", "motorcycles"]

        for type_vehicle in list_of_vehicles:        
            self._cursor.execute(f"""
            CREATE TRIGGER IF NOT EXISTS {type_vehicle}_trigger_insert
            AFTER INSERT ON {type_vehicle}
            BEGIN
                INSERT INTO vehicles (plate, model, brand, year, mileage, average_consumption, status, max_fuel, fuel, license)
                VALUES (NEW.plate, NEW.model, NEW.brand, NEW.year, NEW.mileage, NEW.average_consumption, NEW.status, NEW.max_fuel, NEW.fuel, NEW.license);
            END;"""
            )

            self._cursor.execute(f"""
            CREATE TRIGGER IF NOT EXISTS {type_vehicle}_trigger_update
            AFTER UPDATE ON {type_vehicle}
            BEGIN
                UPDATE vehicles
                SET plate = NEW.plate, model = NEW.model, brand = NEW.brand, year = NEW.year, mileage = NEW.mileage, average_consumption = NEW.average_consumption, status = NEW.status, max_fuel = NEW.max_fuel, fuel = NEW.fuel, license = NEW.license
                WHERE plate = OLD.plate;
            END;""")

            self._cursor.execute(f"""
            CREATE TRIGGER IF NOT EXISTS {type_vehicle}_trigger_delete
            AFTER DELETE ON {type_vehicle}
            BEGIN
                DELETE FROM vehicles
                WHERE plate = OLD.plate;
            END;""")

    def create_maintenances_table(self) -> None:
        self._cursor.execute("""
CREATE TABLE IF NOT EXISTS maintenances (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    plate TEXT NOT NULL,
    type TEXT NOT NULL,
    price REAL,
    description TEXT NOT NULL,
    date_init TEXT NOT NULL,
    date_end TEXT NOT NULL,
    mileage REAL,
    FOREIGN KEY (plate) REFERENCES vehicles (plate)
)
""")

    def _ensure_maintenance_mileage_column(self) -> None:
        # Add the odometer snapshot needed for preventive-service intervals.
        columns = self._cursor.execute("PRAGMA table_info(maintenances)").fetchall()
        if "mileage" not in {column[1] for column in columns}:
            self._cursor.execute("ALTER TABLE maintenances ADD COLUMN mileage REAL")
        self._cursor.execute(
            """
UPDATE maintenances
SET mileage = COALESCE((
    SELECT MAX(0, vehicles.mileage - COALESCE((
        SELECT SUM(trips.distance)
        FROM trips
        WHERE trips.vehicle_plate = maintenances.plate
          AND trips.status = 'Ended'
          AND julianday(trips.date_init) > julianday(
              CASE WHEN maintenances.date_end = '...'
                   THEN maintenances.date_init ELSE maintenances.date_end END
          )
    ), 0))
    FROM vehicles WHERE vehicles.plate = maintenances.plate
), 0)
WHERE mileage IS NULL
"""
        )

    def _ensure_trip_driver_cpf_text(self) -> None:
        # Migrate legacy integer trip CPFs while restoring stored driver strings.
        columns = self._cursor.execute("PRAGMA table_info(trips)").fetchall()
        cpf_column = next(column for column in columns if column[1] == "driver_cpf")
        if cpf_column[2].upper() == "TEXT":
            return

        self._cursor.execute("ALTER TABLE trips RENAME TO trips_legacy")
        self.create_trips_table()
        self._cursor.execute(
            """
INSERT INTO trips (trip_id, driver_cpf, vehicle_plate, origin, destiny, distance, status, date_init, date_end)
SELECT legacy.trip_id, drivers.cpf, legacy.vehicle_plate, legacy.origin, legacy.destiny,
       legacy.distance, legacy.status, legacy.date_init, legacy.date_end
FROM trips_legacy AS legacy
JOIN vehicles ON vehicles.plate = legacy.vehicle_plate
LEFT JOIN drivers ON CAST(drivers.cpf AS INTEGER) = legacy.driver_cpf
"""
        )
        self._cursor.execute("DROP TABLE trips_legacy")

    def create_refuels_table(self) -> None:
        self._cursor.execute("""
CREATE TABLE IF NOT EXISTS refuels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    plate TEXT NOT NULL,
    liters REAL,
    price_per_liter REAL,
    total_cost REAL,
    date TEXT NOT NULL,
    FOREIGN KEY (plate) REFERENCES vehicles (plate)
)
""")

    def delete_vehicle_records(self, plate: str, vehicle_table: str) -> bool:
        # Delete a vehicle and all records referencing it in one transaction.
        vehicle_tables = {"cars", "trucks", "motorcycles"}
        if vehicle_table not in vehicle_tables:
            raise ValueError("Unknown vehicle table")

        try:
            with self._con:
                vehicle = self._cursor.execute(
                    f"SELECT 1 FROM {vehicle_table} WHERE plate = ?", (plate,)
                ).fetchone()
                if vehicle is None:
                    return False

                self._cursor.execute(
                    "DELETE FROM trips WHERE vehicle_plate = ?", (plate,)
                )
                self._cursor.execute(
                    "DELETE FROM maintenances WHERE plate = ?", (plate,)
                )
                self._cursor.execute("DELETE FROM refuels WHERE plate = ?", (plate,))
                self._cursor.execute(
                    f"DELETE FROM {vehicle_table} WHERE plate = ?", (plate,)
                )
            return True
        except sqlite3.Error as exc:
            raise RepositorioError("Could not delete vehicle and related records") from exc
