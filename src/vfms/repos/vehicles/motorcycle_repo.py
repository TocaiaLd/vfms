# Project dependencies
from vfms.models.vehicles.truck import Truck
from vfms.repos.repo import Repo

class MotorcycleRepo():
    def __init__(
        self    : MotorcycleRepo, 
        repo    : Repo
    ):
        self.repo = repo

    def save_motorcycle(
        self            : MotorcycleRepo, 
        vehicle_obj     : Truck,
    ) -> str:
        self.repo._cursor.execute("SELECT * FROM trucks WHERE plate = ?", (vehicle_obj.plate,))
        search_result = self.repo._cursor.fetchone()
        
        if not search_result:
            self.repo._cursor.execute("INSERT INTO motorcycles (plate, model, brand, year, mileage, average_consumption, status, max_fuel, fuel, cc, license) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",(vehicle_obj.plate, vehicle_obj.model, vehicle_obj.brand, vehicle_obj.year, vehicle_obj.mileage, vehicle_obj.average_consumption, vehicle_obj.status.name, vehicle_obj.max_fuel, vehicle_obj.fuel, vehicle_obj.cc, vehicle_obj.license.name))
            self.repo._con.commit()

            return "Vehicle saved successfuly"
        
        return f"Already exists a Vehicle with the {vehicle_obj.plate} plate"

    def show_motorcycles(self) -> list:
        self.repo._cursor.execute(f"SELECT * from motorcycles")
        list_vehicles = self.repo._cursor.fetchall()

        return list_vehicles

    def delete_motorcycle(self, plate) -> str:
        self.repo._cursor.execute("SELECT * FROM motorcycles WHERE plate = ?", (plate,))
        search_result = self.repo._cursor.fetchone()

        if not search_result:
            return "This motorcycle plate doesn't exists"

        self.repo._cursor.execute("DELETE FROM motorcycles WHERE plate = ?", (plate,))
        self.repo._con.commit()

        return f"The motorcycle with plate {plate} was deleted."