from traceback import print_tb
import sqlite3

class Repo():
    def __init__(self):        
        self._con   = sqlite3.connect("db/sqlite3.db")
        self._cursor    = self._con.cursor()

        self._cursor.execute("PRAGMA foreign_keys = ON;")
        self.create_cars_table()
        self.create_trucks_table()
        self.create_motorcycles_table()
        self.create_drivers_table()
        self.create_vehicles_table()
        self.create_vehicles_table_triggers()
        self.create_refuels_table()
        self._con.commit()

    def create_cars_table(self):
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

    def create_trucks_table(self):
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

    def create_motorcycles_table(self):
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

    def create_drivers_table(self):
        self._cursor.execute("""
CREATE TABLE IF NOT EXISTS drivers (
    name TEXT NOT NULL,
    cpf TEXT NOT NULL PRIMARY KEY,
    license TEXT NOT NULL,
    xp INTEGER,
    status TEXT NOT NULL
)
""")

    def create_trips_table(self):
        self._cursor.execute("""
CREATE TABLE IF NOT EXISTS trips (
    trip_id INTEGER PRIMARY KEY AUTOINCREMENT,
    driver_cpf INTEGER,
    vehicle_plate TEXT NOT NULL,
    origin TEXT NOT NULL,
    destiny TEXT NOT NULL,
    distance REAL,
    FOREIGN KEY (driver_cpf) REFERENCES drivers (cpf)
    FOREIGN KEY (vehicle_plate) REFERENCES vehicles (plate)
)
""")

    def create_vehicles_table(self):
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

    def create_vehicles_table_triggers(self):
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

    def create_maintenances_table(self):
        pass

    def create_refuels_table(self):
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
