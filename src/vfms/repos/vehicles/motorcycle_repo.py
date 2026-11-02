from typing import Any

# Project dependencies
from vfms.models.vehicles.motorcycle import Motorcycle
from vfms.repos.repo import Repo

class MotorcycleRepo():
    # Persist motorcycles and retrieve their stored records.
    def __init__(
        self    : MotorcycleRepo, 
        repo    : Repo
    ) -> None:
        self.repo = repo

    def save_motorcycle(
        self            : MotorcycleRepo, 
        vehicle_obj     : Motorcycle,
    ) -> str:
        self.repo.execute("SELECT * FROM motorcycles WHERE plate = ?", (vehicle_obj.plate,))
        search_result = self.repo._cursor.fetchone()
        
        if not search_result:
            self.repo.execute("INSERT INTO motorcycles (plate, model, brand, year, mileage, average_consumption, status, max_fuel, fuel, cc, license) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",(vehicle_obj.plate, vehicle_obj.model, vehicle_obj.brand, vehicle_obj.year, vehicle_obj.mileage, vehicle_obj.average_consumption, vehicle_obj.status.name, vehicle_obj.max_fuel, vehicle_obj.fuel, vehicle_obj.cc, vehicle_obj.license.name))
            self.repo.commit()

            return "Vehicle saved successfuly"
        
        return f"Already exists a Vehicle with the {vehicle_obj.plate} plate"

    def show_motorcycles(self) -> list[tuple[Any, ...]]:
        self.repo.execute(f"SELECT * from motorcycles")
        list_vehicles = self.repo._cursor.fetchall()

        return list_vehicles

    def update_motorcycle(
        self            : MotorcycleRepo, 
        vehicle_obj     : Motorcycle,
    ) -> str:
        self.repo.execute("SELECT * FROM motorcycles WHERE plate = ?", (vehicle_obj.plate,))
        search_result = self.repo._cursor.fetchone()

        if search_result:
            new_data = (vehicle_obj.plate, vehicle_obj.model, vehicle_obj.brand, vehicle_obj.year, vehicle_obj.mileage, vehicle_obj.average_consumption, vehicle_obj.status.name, vehicle_obj.max_fuel, vehicle_obj.fuel, vehicle_obj.cc, vehicle_obj.license.name, vehicle_obj.plate)
            
            self.repo.execute("""
UPDATE motorcycles 
SET plate = ?, model = ?, brand = ?, year = ?, mileage = ?, average_consumption = ?, status = ?, max_fuel = ?, fuel = ?, cc = ?, license = ?  
WHERE plate = ?;
""", new_data)
            self.repo.commit()

            return "Vehicle updated successfuly"

        return f"Does not exists a vehicle with this plate"

    def delete_motorcycle(self, plate: str) -> str:
        if not self.repo.delete_vehicle_records(plate, "motorcycles"):
            return f"Motorcycle does not exist with plate {plate}"
        return f"The motorcycle with plate {plate} was deleted."

    def get_by_plate(self, plate: str) -> tuple[Any, ...] | None:
        self.repo.execute(f"SELECT * from motorcycles WHERE plate = ?", (plate,))
        motorcycle = self.repo._cursor.fetchone()

        return motorcycle

    def vehicle_exists(self, search_plate: str) -> bool:
        self.repo.execute("SELECT * FROM motorcycles WHERE plate = ?", (search_plate,))
        search_result = self.repo._cursor.fetchone()

        if not search_result:
            return False

        return True

    def vehicle_is_available(self, search_plate: str) -> bool:
        self.repo.execute("SELECT * FROM motorcycles WHERE plate = ? AND status = ?", (search_plate, "AVAILABLE"))
        search_result = self.repo._cursor.fetchone()

        if not search_result:
            return False

        return True
