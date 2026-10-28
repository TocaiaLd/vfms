import sqlite3

class Repo():
    def __init__(self):        
        self._con   = sqlite3.connect("db/sqlite3.db")
        self._cursor    = self._con.cursor()
        self.create_cars_table()
        self.create_trucks_table()
        self.create_motorcycles_table()
        self._con.commit()

        self._cursor.execute("SELECT * from motorcycles")
        cars = self._cursor.fetchall()

        for car in cars:
            print(car)

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
        pass

    def create_trips_table(self):
        pass

    def create_maintenances_table(self):
        pass

    def create_refuels_table(self):
        pass
