# Project dependencies
from vfms.models.vehicles.car import Car
from vfms.repos.repo import Repo

class CarRepo():
    def __init__(
        self    : CarRepo, 
        repo    : Repo
    ):
        self.repo = repo

    def save_car(
        self            : CarRepo, 
        vehicle_obj     : Car,
    ) -> str:
        self.repo._cursor.execute("SELECT * FROM cars WHERE plate = ?", (vehicle_obj.plate,))
        search_result = self.repo._cursor.fetchone()

        if not search_result:
            self.repo._cursor.execute("INSERT INTO cars (plate, model, brand, year, mileage, average_consumption, status, max_fuel, fuel, ports, license) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (vehicle_obj.plate, vehicle_obj.model, vehicle_obj.brand, vehicle_obj.year, vehicle_obj.mileage, vehicle_obj.average_consumption, vehicle_obj.status.name, vehicle_obj.max_fuel, vehicle_obj.fuel, vehicle_obj.ports, vehicle_obj.license.name))
            self.repo._con.commit()

            return "Vehicle saved successfuly"

        return f"Already exists a Vehicle with the {vehicle_obj.plate} plate"

    def show_cars(self) -> list:
        self.repo._cursor.execute(f"SELECT * from cars")
        list_vehicles = self.repo._cursor.fetchall()

        return list_vehicles

    def update_car(
        self            : CarRepo, 
        vehicle_obj     : Car,
    ) -> str:
        self.repo._cursor.execute("SELECT * FROM cars WHERE plate = ?", (vehicle_obj.plate,))
        search_result = self.repo._cursor.fetchone()

        if search_result:
            new_data = (vehicle_obj.plate, vehicle_obj.model, vehicle_obj.brand, vehicle_obj.year, vehicle_obj.mileage, vehicle_obj.average_consumption, vehicle_obj.status.name, vehicle_obj.max_fuel, vehicle_obj.fuel, vehicle_obj.ports, vehicle_obj.license.name, vehicle_obj.plate)
            
            self.repo._cursor.execute("""
UPDATE cars 
SET plate = ?, model = ?, brand = ?, year = ?, mileage = ?, average_consumption = ?, status = ?, max_fuel = ?, fuel = ?, ports = ?, license = ?  
WHERE plate = ?;
""", new_data)
            self.repo._con.commit()

            return "Vehicle updated successfuly"

        return f"Does not exists a vehicle with this plate"

    def delete_car(self, plate) -> str:
        self.repo._cursor.execute("SELECT * FROM cars WHERE plate = ?", (plate,))
        search_result = self.repo._cursor.fetchone()

        if not search_result:
            return "This car plate doesn't exists"

        self.repo._cursor.execute("DELETE FROM cars WHERE plate = ?", (plate,))
        self.repo._con.commit()

        return f"The car with plate {plate} was deleted"

    def get_by_plate(self, plate) -> dict:
        self.repo._cursor.execute(f"SELECT * from cars WHERE plate = ?", (plate,))
        car = self.repo._cursor.fetchone()

        return car